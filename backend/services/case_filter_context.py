"""按项目批量加载高级筛选关联值及日期类型，不触发逐条查询或写入。"""

from collections import defaultdict
from copy import deepcopy
from fastapi import HTTPException
from services.filter_values import temporal
from core.logger import logger

MEMBER_FIELDS = {"createdBy", "updatedBy", "executorId"}
DATE_OPERATORS = {"between", "gt", "gte", "lt", "lte", "equals", "not_equals"}


def filter_time(value):
    try:
        return temporal(value)
    except (ValueError, TypeError, OverflowError, OSError) as exc:
        logger.exception("高级筛选时间解析失败")
        raise HTTPException(422, "筛选时间不是有效ISO时间或毫秒时间戳") from exc


def date_expected(condition):
    value = condition.get("value")
    return (
        [filter_time(v) for v in value]
        if condition["operator"] == "between"
        else filter_time(value)
    )


class CaseFilterContext:
    def __init__(self, db, project_id, conditions, user_id, *, current_read=False, include_recycled=False):
        from models.test_case import TestCase, CaseAttachment
        from models.case_features import CaseTemplate, CaseIssue, CaseIssueLink

        self.attachments = defaultdict(list)
        self.requirements = defaultdict(list)
        self.template_types = {}
        fields = {c["field"] for c in conditions}
        def read(query):
            if current_read:
                query = query.populate_existing().with_for_update()
            return query.all()

        if any(field.startswith("customFields.") for field in fields):
            self.template_types = {
                t.id: {f["key"]: f["type"] for f in t.fields}
                for t in read(db.query(CaseTemplate).filter_by(project_id=project_id))
            }
        if "attachment" in fields:
            rows = read(
                db.query(CaseAttachment.case_id, CaseAttachment.file_name)
                .join(TestCase, TestCase.id == CaseAttachment.case_id)
                .filter(
                    TestCase.project_id == project_id,
                    True if include_recycled else TestCase.deleted_at.is_(None),
                )
            )
            for case_id, name in rows:
                if name:
                    self.attachments[case_id].append(name)
        if "requirementRef" in fields:
            rows = read(
                db.query(CaseIssueLink.case_id, CaseIssue.title)
                .join(CaseIssue, CaseIssue.id == CaseIssueLink.issue_id)
                .join(TestCase, TestCase.id == CaseIssueLink.case_id)
                .filter(
                    TestCase.project_id == project_id,
                    True if include_recycled else TestCase.deleted_at.is_(None),
                    CaseIssue.project_id == project_id,
                    CaseIssue.kind == "requirement",
                )
            )
            for case_id, name in rows:
                if name:
                    self.requirements[case_id].append(name)
        # 不改动输入条件、个人视图JSON或用例自定义值。
        self.conditions = deepcopy(conditions)
        for condition in self.conditions:
            field, operator = condition["field"], condition["operator"]
            if field in MEMBER_FIELDS:

                def resolve(value):
                    if value != "CURRENT_USER":
                        return value
                    if not user_id:
                        raise HTTPException(422, "当前用户筛选需要登录用户上下文")
                    return str(user_id)

                value = condition.get("value")
                condition["value"] = (
                    [resolve(v) for v in value]
                    if isinstance(value, list)
                    else resolve(value)
                )
            if operator in DATE_OPERATORS:
                kinds = {
                    t[field.split(".", 1)[1]]
                    for t in self.template_types.values()
                    if field.startswith("customFields.") and field.split(".", 1)[1] in t
                }
                if field in {"createdAt", "updatedAt"} or kinds == {"date"}:
                    condition["value"] = date_expected(condition)

        if conditions:
            logger.debug(
                "高级筛选关联值已准备 project_id={} 附件用例数={} 需求用例数={} 模板数={}",
                project_id,
                len(self.attachments),
                len(self.requirements),
                len(self.template_types),
            )

    def custom_value(self, case, condition):
        key = condition["field"].split(".", 1)[1]
        value = (case.custom_fields or {}).get(key)
        expected = condition.get("value")
        if (
            self.template_types.get(case.template_id, {}).get(key) == "date"
            and condition["operator"] in DATE_OPERATORS
        ):
            value = filter_time(value) if value not in (None, "") else None
            expected = date_expected(condition)
        return value, expected
