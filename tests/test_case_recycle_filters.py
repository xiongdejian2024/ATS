"""回收站共享高级筛选语义和项目隔离，保留恢复/历史引用删除保护。"""
import json
from test_case_features import features
from test_case_governance import governance
from models.test_case import TestCase as Case


def test_recycle_filters_search_paging_dates_relations_and_custom_fields(features):
    g=features;c=g['client'];base=g['features'];first,second=g['cases']
    template=c.post(base+'/templates',json={'name':'回收筛选模板','fields':[{'key':'platform','name':'平台','type':'text'}]}).json()['data']
    updated=c.put(f'/api/v1/test-cases/{first.id}',json={'name':'100% 回收测试','priority':'P0','tags':['特殊标签'],'template_id':template['id'],'custom_fields':{'platform':'synthetic'}})
    assert updated.status_code==200,updated.text
    c.post(base+f'/cases/{first.id}/attachments',files={'file':('recycled.pdf',b'synthetic','application/pdf')})
    for case in (first,second):assert c.delete(f'/api/v1/test-cases/{case.id}').status_code==200
    g['foreign'].deleted_at=first.deleted_at;g['db'].commit()
    url=base+'/recycle-bin'
    assert c.get(url,params={'search':first.case_code}).json()['data']['total']==1
    assert c.get(url,params={'search':'%'}).json()['data']['total']==1
    criteria=[{'field':'priority','operator':'belongs_to','value':['P0']},{'field':'tags','operator':'contains','value':['特殊标签']},{'field':'attachment','operator':'contains','value':'recycled.pdf'},{'field':'customFields.platform','operator':'equals','value':'synthetic'},{'field':'createdBy','operator':'belongs_to','value':['CURRENT_USER']},{'field':'deletedAt','operator':'between','value':['2020-01-01T00:00:00Z','2030-01-01T00:00:00Z']}]
    data=c.get(url,params={'filters':json.dumps({'conditions':criteria,'logic':'and'})}).json()['data']
    assert data['total']==1 and data['items'][0]['id']==first.id
    criteria=[{'field':'priority','operator':'equals','value':'P0'},{'field':'name','operator':'equals','value':second.name}]
    data=c.get(url,params={'size':1,'page':2,'sort_by':'caseCode','sort_order':'asc','filters':json.dumps({'conditions':criteria,'logic':'or'})}).json()['data']
    assert data['total']==2 and len(data['items'])==1 and data['items'][0]['projectId']==g['project'].id
    assert c.get('/api/v1/test-cases',params={'project_id':g['project'].id}).json()['data']['total']==0
    assert g['db'].get(Case,first.id).deleted_at is not None


def test_recycle_rejects_invalid_filters_sort_and_outsiders(features):
    g=features;c=g['client'];url=g['features']+'/recycle-bin'
    for query in ({'filters':'invalid'},{'filters':json.dumps({'conditions':[{'field':'unknown','operator':'equals','value':'x'}]})},{'sort_by':'description'},{'filters':json.dumps({'conditions':[{'field':'deletedAt','operator':'between','value':['2030-01-01','2020-01-01']}]})}):
        response=c.get(url,params=query);assert response.status_code==422,response.text
    g['state']['user']=g['users'][3]
    assert c.get(url).status_code==403


def test_default_recycle_uses_sql_page_without_review_history_scan(features,monkeypatch):
    from sqlalchemy import event
    import services.case_governance as service
    g=features;c=g['client']
    for case in g['cases']:assert c.delete(f'/api/v1/test-cases/{case.id}').status_code==200
    def unexpected(*args,**kwargs):raise AssertionError('default recycle must not scan review history')
    monkeypatch.setattr(service,'current_review_statuses',unexpected)
    statements=[];engine=g['db'].get_bind()
    def capture(conn,cursor,statement,parameters,context,executemany):statements.append(statement.lower())
    event.listen(engine,'before_cursor_execute',capture)
    try:response=c.get(g['features']+'/recycle-bin',params={'page':2,'size':1})
    finally:event.remove(engine,'before_cursor_execute',capture)
    assert response.status_code==200,response.text
    assert response.json()['data']['total']==2 and len(response.json()['data']['items'])==1
    item_queries=[s for s in statements if 'from test_cases' in s and 'count(' not in s]
    assert item_queries and all('limit' in s and 'offset' in s for s in item_queries)
