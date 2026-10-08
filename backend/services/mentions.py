"""Bounded structured mentions in existing immutable collaboration records.

Plain @ text is never interpreted as an identity. Notifications deliberately
contain no project names or comment excerpts; opening one rechecks access.
"""
from html import escape
from html.parser import HTMLParser
import re
from fastapi import HTTPException
from sqlalchemy import or_
from models import User, ProjectMember, Notification
from core.project_access import require_project_access

MAX_RECIPIENTS = 20
KINDS = {'case_comment', 'review_event', 'case_execution', 'run_comment'}


def member_query(db, project):
    membership = db.query(ProjectMember.id).filter(
        ProjectMember.project_id == project.id, ProjectMember.user_id == User.id
    ).exists()
    return db.query(User).filter(User.status.is_(True), or_(
        User.id.in_([project.owner_id, project.created_by]), membership))


def members(db, user, project_id, context, search='', page=1):
    project = require_project_access(db, user, project_id, f'test_{context}:read')
    query = member_query(db, project)
    if search:
        # Escaped LIKE gives literal user input, including % and _.
        value = '%' + search.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'
        query = query.filter(or_(User.username.like(value, escape='\\'), User.full_name.like(value, escape='\\')))
    total = query.count()
    rows = query.order_by(User.username, User.id).offset((page-1)*20).limit(20).all()
    return dict(items=[dict(id=r.id, label=r.full_name or r.username, username=r.username) for r in rows], total=total, page=page, size=20)


class MentionParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts, self.ids, self.inside = [], set(), False

    def handle_starttag(self, tag, attrs):
        if self.inside:
            raise HTTPException(422, '提及节点不能包含嵌套格式')
        values = dict(attrs)
        if 'data-mention-id' in values:
            identifier = values['data-mention-id'] or ''
            if tag != 'span' or not re.fullmatch(r'[A-Za-z0-9_-]{1,36}', identifier):
                raise HTTPException(422, '提及标识无效')
            if len([a for a, _ in attrs if a == 'data-mention-id']) != 1:
                raise HTTPException(422, '提及标识不能重复')
            self.ids.add(identifier)
            if len(self.ids) > MAX_RECIPIENTS:
                raise HTTPException(422, '一次最多提及20位成员')
            self.parts.append(('mention', identifier))
            self.inside = True
        else:
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if self.inside or any(name == 'data-mention-id' for name, _ in attrs):
            raise HTTPException(422, '提及节点格式无效')
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.inside:
            if tag != 'span':
                raise HTTPException(422, '提及节点格式无效')
            self.inside = False
        else:
            self.parts.append(f'</{tag}>')

    def handle_data(self, value):
        if not self.inside:
            self.parts.append(value)

    def handle_entityref(self, name):
        self.handle_data(f'&{name};')

    def handle_charref(self, name):
        self.handle_data(f'&#{name};')

    def handle_comment(self, value):
        if self.inside:
            raise HTTPException(422, '提及节点格式无效')
        self.parts.append(f'<!--{value}-->')

    def handle_decl(self, value):
        self.parts.append(f'<!{value}>')


def prepare(db, actor, project_id, content, *, context='case', max_length=10000):
    parser = MentionParser()
    parser.feed(content)
    parser.close()
    if parser.inside:
        raise HTTPException(422, '提及节点未闭合')
    if not parser.ids:
        return content, []
    # Current locking reads avoid accepting a revoked/disabled cached recipient.
    project = require_project_access(db, actor, project_id, f'test_{context}:read', current_read=True)
    # Shared state locks are compatible with authors' FK checks and other
    # current identity reads. Exclusive user locks cause reciprocal mentions
    # in different projects to wait on each other's author foreign keys.
    identities = db.query(User).filter(User.id.in_(sorted(parser.ids | {str(actor.id)}))).order_by(User.id).populate_existing().with_for_update(read=True).all()
    current_actor = next((r for r in identities if r.id == str(actor.id)),None)
    if not current_actor or not current_actor.status:
        raise HTTPException(403,'用户不存在或已停用')
    recipients = [r for r in identities if r.id in parser.ids]
    membership = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id.in_(sorted(parser.ids))).order_by(ProjectMember.user_id, ProjectMember.id).populate_existing().with_for_update().all()
    eligible = {r.user_id for r in membership} | {project.owner_id, project.created_by}
    if {r.id for r in recipients} != parser.ids or any(not r.status or r.id not in eligible for r in recipients):
        raise HTTPException(422, '提及成员已停用或不属于当前项目，请重新选择')
    labels = {r.id: r.full_name or r.username for r in recipients}
    result = ''.join(
        f'<span data-mention-id="{part[1]}" data-mention-label="{escape(labels[part[1]], quote=True)}">@{escape(labels[part[1]])}</span>'
        if isinstance(part, tuple) else part for part in parser.parts
    )
    if len(result) > max_length:
        raise HTTPException(422, '提及后的内容超出长度限制')
    return result, sorted(parser.ids)


def notify(db, actor, recipients, kind, entity_id):
    if kind not in KINDS:
        raise ValueError('unknown mention source')
    for identifier in sorted(set(recipients) - {str(actor.id)}):
        db.add(Notification(user_id=identifier, type='mention_'+kind, title='有人提及了你',
            content='协作内容中有一条与你有关的提及，打开后查看。', related_id=entity_id))


def source(db, recipient, notification):
    """Resolve only server-owned entity IDs; never trust a client supplied URL."""
    from models.case_features import CaseComment
    from models.case_governance import CaseReviewEvent, CaseReview
    from models.plan_case_execution import PlanCaseExecution
    from models.plan_workspace import PlanRunComment
    from models import TestPlan, TestCase
    from api.v1.plan_orchestration import require_plan, require_run
    from services.plan_report_workspace import ensure_visible
    from services.plan_collaboration import require_association
    kind, identifier = notification.type.removeprefix('mention_'), notification.related_id
    def payload(row, route, content, content_format='rich'):
        return dict(content=content, contentFormat=content_format, sourceId=row.id, kind=kind, route=route, createdAt=row.created_at)
    if notification.user_id != str(recipient.id) or kind not in KINDS:
        raise HTTPException(404, '提及来源不存在')
    if kind == 'case_comment':
        row = db.get(CaseComment, identifier)
        case = db.get(TestCase, row.case_id) if row else None
        if not case or case.deleted_at:
            raise HTTPException(404, '提及来源已不可用')
        require_project_access(db, recipient, case.project_id, 'test_case:read')
        return payload(row,dict(path='/test-cases', query=dict(projectId=case.project_id, caseId=case.id)),row.content)
    if kind == 'review_event':
        row = db.get(CaseReviewEvent, identifier)
        review = db.get(CaseReview, row.review_id) if row else None
        if not review:
            raise HTTPException(404, '提及来源已不可用')
        require_project_access(db, recipient, review.project_id, 'test_case:read')
        return payload(row,dict(path='/case-reviews/reading', query=dict(projectId=review.project_id, reviewId=review.id, itemId=row.item_id)),row.detail.get('comment',''))
    if kind == 'case_execution':
        row = db.get(PlanCaseExecution, identifier)
        if not row:
            raise HTTPException(404, '提及来源已不可用')
        plan = require_plan(db, recipient, row.plan_id)
        require_project_access(db,recipient,plan.project_id,'test_case:read')
        parts = row.association_key.split(':')
        if len(parts) != 3:
            raise HTTPException(404, '提及来源已不可用')
        return payload(row,dict(path=f'/test-plans/{plan.id}/functional-execution', query=dict(projectId=plan.project_id, source=parts[0], associationId=parts[1], caseId=parts[2])),row.description)
    row = db.get(PlanRunComment, identifier)
    if not row:
        raise HTTPException(404, '提及来源已不可用')
    run = require_run(db, recipient, row.run_id)
    ensure_visible(db, 'PLAN', run.id)
    require_association(run, row.association_id)
    plan = db.get(TestPlan, run.plan_id)
    return payload(row,dict(name='TestPlanReportDetail', params=dict(runId=run.id), query=dict(projectId=plan.project_id, kind='PLAN', associationId=row.association_id)),row.content,row.content_format)
