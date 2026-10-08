"""脑图模块写入口权限/层级，全部使用合成隔离数据。"""
from test_case_governance import governance
from models.module import Module
from models.test_case import TestCase as Case
import pytest


def test_module_create_update_delete_have_project_permissions_and_parent_isolation(governance):
    g=governance;c=g['client'];base=f"/api/v1/projects/{g['project'].id}/modules"
    foreign=Module(project_id=g['foreign'].project_id,name='外部模块');g['db'].add(foreign);g['db'].commit()
    for parent in (foreign.id,'missing'):
        response=c.post(base,json={'name':'禁止跨项目父级','parentId':parent});assert response.status_code==422,response.text
    assert g['db'].query(Module).filter_by(project_id=g['project'].id).count()==0
    created=c.post(base,json={'name':'根模块','sortOrder':2});assert created.status_code==200,created.text
    module=created.json()['data'];g['state']['user']=g['users'][1]
    assert c.get(base).status_code==200
    assert c.post(base,json={'name':'只读创建'}).status_code==403
    assert c.put(base+'/'+module['id'],json={'name':'只读重命名'}).status_code==403
    assert c.delete(base+'/'+module['id']).status_code==403
    g['state']['user']=g['users'][0]
    assert c.put(base+'/'+foreign.id,json={'name':'外部篡改'}).status_code==404
    assert c.delete(base+'/'+foreign.id).status_code==404
    assert g['db'].get(Module,foreign.id).name=='外部模块'


def test_module_move_cycle_and_delete_promotes_subtree_without_deleting_cases(governance):
    g=governance;c=g['client'];base=f"/api/v1/projects/{g['project'].id}/modules"
    def create(name,parent=None):return c.post(base,json={'name':name,'parentId':parent}).json()['data']['id']
    root=create('根');child=create('子',root);grand=create('孙',child);leaf=create('叶',grand)
    response=c.put(base+'/'+root,json={'parentId':grand});assert response.status_code==422,response.text
    assert g['db'].get(Module,root).parent_id is None
    case=g['cases'][0];case.module_id=child;case.module_path='根/子';g['db'].commit()
    assert c.delete(base+'/'+child).status_code==200
    g['db'].expire_all()
    assert g['db'].get(Module,grand).parent_id==root and g['db'].get(Module,grand).level==2
    assert g['db'].get(Module,leaf).level==3
    assert g['db'].get(Case,case.id).module_id is None and g['db'].get(Case,case.id).module_path is None
    assert g['db'].get(Case,case.id).deleted_at is None
    assert c.put(base+'/'+grand,json={'parentId':None}).status_code==200
    assert g['db'].get(Module,grand).level==1 and g['db'].get(Module,leaf).level==2


def test_disabled_actor_is_rechecked_even_when_request_session_holds_stale_user(governance):
    from sqlalchemy.orm import Session
    from models import User
    g=governance;actor=g['users'][0];assert actor.status
    with Session(g['db'].get_bind()) as separate:
        separate.query(User).filter_by(id=actor.id).update({'status':False});separate.commit()
    assert actor.status
    response=g['client'].post(f"/api/v1/projects/{g['project'].id}/modules",json={'name':'禁止禁用用户写入'})
    assert response.status_code==403,response.text
    assert g['db'].query(Module).count()==0


def test_module_rename_move_and_parent_delete_refresh_all_local_case_paths(governance):
    g=governance;c=g['client'];db=g['db'];base=f"/api/v1/projects/{g['project'].id}/modules"
    def create(name,parent=None):return c.post(base,json={'name':name,'parentId':parent}).json()['data']['id']
    root=create('根');child=create('子',root);leaf=create('叶',child);target=create('目标')
    a,b=g['cases'][:2];a.module_id=child;a.module_path='旧子路径';b.module_id=leaf;b.module_path='旧叶路径';db.commit()
    original_ids=(a.id,b.id)
    assert c.put(base+'/'+root,json={'name':'新根'}).status_code==200
    db.expire_all();assert db.get(Case,a.id).module_path=='新根/子';assert db.get(Case,b.id).module_path=='新根/子/叶'
    assert c.put(base+'/'+child,json={'parentId':target}).status_code==200
    db.expire_all();assert db.get(Case,a.id).module_path=='目标/子';assert db.get(Case,b.id).module_path=='目标/子/叶'
    assert c.delete(base+'/'+child).status_code==200
    db.expire_all();assert db.get(Case,a.id).module_path is None;assert db.get(Case,b.id).module_path=='目标/叶'
    assert (a.id,b.id)==original_ids and db.get(Case,b.id).deleted_at is None


def test_module_path_overflow_rejects_and_rolls_back_move(governance):
    g=governance;c=g['client'];db=g['db'];base=f"/api/v1/projects/{g['project'].id}/modules"
    def create(name,parent=None):return c.post(base,json={'name':name,'parentId':parent}).json()['data']['id']
    source=create('原模块');target=None
    for _ in range(5):target=create('测'*100,target)
    case=g['cases'][0];case.module_id=source;case.module_path='原模块';db.commit()
    response=c.put(base+'/'+source,json={'parentId':target});assert response.status_code==422,response.text
    db.expire_all();assert db.get(Module,source).parent_id is None;assert db.get(Case,case.id).module_path=='原模块'


def test_module_path_refresh_preserves_review_snapshot_and_marks_current_content_changed(governance):
    from test_case_governance import request_review
    from models import CaseVersion
    from services.case_governance import current_review_statuses
    g=governance;c=g['client'];db=g['db'];base=f"/api/v1/projects/{g['project'].id}/modules"
    module=c.post(base,json={'name':'旧模块'}).json()['data']['id'];case=g['cases'][0]
    assert c.post(g['base']+'/batch',json={'caseIds':[case.id],'moduleId':module}).status_code==200
    review=request_review(g,reviewers=[g['users'][0].id]);item=next(i for i in review['items'] if i['caseId']==case.id)
    voted=c.post(g['base']+f"/reviews/{review['id']}/items/{item['id']}/decision",json={'decision':'approved','comment':'合成验收'})
    assert voted.status_code==200,voted.text
    before=[(v.id,dict(v.snapshot)) for v in db.query(CaseVersion).filter_by(case_id=case.id).all()]
    assert current_review_statuses(db,[case])[case.id]=='passed'
    assert c.put(base+'/'+module,json={'name':'新模块'}).status_code==200
    db.expire_all();fresh=db.get(Case,case.id);assert fresh.module_path=='新模块'
    assert [(v.id,dict(v.snapshot)) for v in db.query(CaseVersion).filter_by(case_id=case.id).all()]==before
    fetched=c.get(g['base']+f"/reviews/{review['id']}").json()['data']
    old=next(i for i in fetched['items'] if i['caseId']==case.id)
    assert old['snapshot']['module_path']=='旧模块' and old['outdated'] is True
    assert current_review_statuses(db,[fresh])[fresh.id]=='resubmit'


def test_case_move_copy_and_create_use_full_nested_target_path(governance):
    g=governance;c=g['client'];db=g['db'];base=f"/api/v1/projects/{g['project'].id}/modules"
    root=c.post(base,json={'name':'根'}).json()['data']['id'];leaf=c.post(base,json={'name':'叶','parentId':root}).json()['data']['id'];case=g['cases'][0]
    moved=c.post(g['base']+'/batch',json={'caseIds':[case.id],'moduleId':leaf});assert moved.status_code==200,moved.text
    db.expire_all();assert db.get(Case,case.id).module_path=='根/叶'
    copied=c.post(g['base']+'/batch-copy',json={'caseIds':[case.id],'moduleId':leaf});assert copied.status_code==200,copied.text
    copy=db.get(Case,copied.json()['data']['caseIds'][0]);assert copy.module_path=='根/叶' and copy.id!=case.id
    created=c.post("/api/v1/test-cases",json={'project_id':g['project'].id,'name':'脑图复制普通内容','type':'functional','module_id':leaf,'module_path':'伪造路径'})
    assert created.status_code==200,created.text
    assert db.get(Case,created.json()['data']['id']).module_path=='根/叶'


@pytest.mark.parametrize('reference',['module','case'])
def test_delete_refuses_legacy_cross_project_references_instead_of_rewriting_them(governance,reference):
    g=governance;db=g['db'];source=Module(project_id=g['project'].id,name='旧关联来源');db.add(source);db.flush()
    if reference=='module':
        foreign=Module(project_id=g['foreign'].project_id,name='外部旧子模块',parent_id=source.id);db.add(foreign)
    else:
        foreign=g['foreign'];foreign.module_id=source.id;foreign.module_path='保留外部旧路径'
    db.commit();response=g['client'].delete(f"/api/v1/projects/{g['project'].id}/modules/{source.id}")
    assert response.status_code==409,response.text
    db.expire_all();assert db.get(Module,source.id) is not None
    if reference=='module':assert db.get(Module,foreign.id).parent_id==source.id
    else:assert db.get(Case,foreign.id).module_id==source.id and db.get(Case,foreign.id).module_path=='保留外部旧路径'


def test_postgres_reciprocal_module_moves_serialize_before_cycle_validation(governance):
    from database import engine,SessionLocal
    if engine.dialect.name!='postgresql':pytest.skip('requires disposable PostgreSQL CI')
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from sqlalchemy import text
    from models import User
    from api.v1.projects import update_module
    from schemas.module import ModuleUpdate
    from fastapi import HTTPException
    import asyncio
    g=governance;p=g['project'].id;actor_id=g['users'][0].id
    first=Module(project_id=p,name='并发A');second=Module(project_id=p,name='并发B');g['db'].add_all([first,second]);g['db'].commit();a,b=first.id,second.id;barrier=Barrier(2)
    def move(source,target):
        with SessionLocal() as db:
            db.execute(text("SET LOCAL lock_timeout = '3s'"));actor=db.get(User,actor_id);barrier.wait(timeout=5)
            try:
                asyncio.run(update_module(project_id=p,module_id=source,module_data=ModuleUpdate(parentId=target),db=db,current_user=actor));return 200
            except HTTPException as error:return error.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=[pool.submit(move,a,b),pool.submit(move,b,a)]
        assert sorted(f.result(timeout=10) for f in results)==[200,422]
    g['db'].expire_all()
    assert not(g['db'].get(Module,a).parent_id==b and g['db'].get(Module,b).parent_id==a)


def test_case_update_uses_full_target_path_and_clears_path_on_unassignment(governance):
    g=governance;c=g['client'];db=g['db'];base=f"/api/v1/projects/{g['project'].id}/modules"
    root=c.post(base,json={'name':'根'}).json()['data']['id'];leaf=c.post(base,json={'name':'叶','parentId':root}).json()['data']['id'];case=g['cases'][0]
    target=f"/api/v1/test-cases/{case.id}"
    changed=c.put(target,json={'module_id':leaf,'module_path':'伪造路径'});assert changed.status_code==200,changed.text
    db.expire_all();assert db.get(Case,case.id).module_path=='根/叶'
    changed=c.put(target,json={'module_path':'再次伪造'});assert changed.status_code==200,changed.text
    db.expire_all();assert db.get(Case,case.id).module_path=='根/叶'
    changed=c.put(target,json={'module_id':None});assert changed.status_code==200,changed.text
    db.expire_all();assert db.get(Case,case.id).module_id is None and db.get(Case,case.id).module_path is None
