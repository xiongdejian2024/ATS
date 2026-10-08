"""评审首页高级过滤使用真实聚合查询，保持只读和项目边界。"""
import pytest
from fastapi import HTTPException
from test_case_governance import governance, request_review
from models.case_governance import CaseReview, CaseReviewItem, CaseReviewEvent
from models.review_workspace import ReviewWorkspace
from services.review_workspace import summary_query
from services.review_index_filter import apply, parse


def condition(field, value=None, operator="equals"):
    return dict(field=field, value=value, operator=operator)


def matches(g, conditions, logic="and"):
    query, state, rate = summary_query(g["db"], g["cases"][0].project_id)
    filtered = apply(g["db"], query, state, rate, dict(conditions=conditions,logic=logic), str(g["state"]["user"].id))
    return [row[0].id for row in filtered.all()]


def test_review_conditions_match_summary_members_tags_and_empty_rows_without_writes(governance):
    g=governance; db=g["db"]
    first=request_review(g,reviewers=[g["users"][2].id])
    second=request_review(g,reviewers=[g["users"][1].id])
    a=db.get(CaseReview,first["id"]);b=db.get(CaseReview,second["id"])
    a.name="Literal_%";b.name="Other";b.created_by=g["users"][1].id
    infos=db.query(ReviewWorkspace).filter(ReviewWorkspace.review_id.in_([a.id,b.id])).all()
    for info in infos:info.tags=["回归", "诊断"] if info.review_id==a.id else []
    item=db.query(CaseReviewItem).filter_by(review_id=a.id).first();item.reviewer_ids=[g["users"][1].id]
    db.commit();before=db.query(CaseReviewEvent).count()
    assert matches(g,[condition("name","_%","contains")])==[a.id]
    assert set(matches(g,[condition("tags","回归","contains"),condition("name","Other")],"or"))=={a.id,b.id}
    assert matches(g,[condition("createdBy","CURRENT_USER")])==[a.id]
    assert set(matches(g,[condition("reviewerId",g["users"][1].id,"belongs_to")]))=={a.id,b.id}
    assert matches(g,[condition("tags",1,"count_gt")])==[a.id]
    assert matches(g,[condition("tags",None,"is_empty")])==[b.id]
    assert len(matches(g,[condition("caseCount",1,"gte"),condition("passRate",0)]))==2
    db.query(ReviewWorkspace).filter_by(review_id=b.id).delete();db.commit()
    assert matches(g,[condition("moduleId",["default"],"belongs_to"),condition("tags",None,"is_empty")])==[b.id]
    assert db.query(CaseReviewEvent).count()==before


def test_precise_and_legacy_periods_accept_offsets_and_apply_real_bounds(governance):
    from datetime import datetime, date
    g=governance;db=g["db"];review=request_review(g)
    row=db.get(CaseReview,review["id"]);row.start_date=date(2026,10,8)
    info=db.query(ReviewWorkspace).filter_by(review_id=row.id).one();info.start_time=datetime(2026,10,8,8,30)
    db.commit()
    assert matches(g,[condition("startTime",["2026-10-08T00:00:00Z","2026-10-08T01:00:00Z"],"between")])==[row.id]
    info.start_time=None;db.commit()
    assert matches(g,[condition("startTime",["2026-10-07T23:59:00+08:00","2026-10-08T00:01:00+08:00"],"between")])==[row.id]
    midnight="2026-10-08T00:00:00+08:00"
    for operator, expected in (("gte",[row.id]),("lte",[row.id]),("gt",[]),("lt",[])):
        assert matches(g,[condition("startTime",midnight,operator)])==expected
    assert matches(g,[condition("startTime",[midnight,midnight],"between")])==[row.id]


def test_index_endpoint_count_paging_archives_and_private_view_namespace(governance):
    import json
    from test_review_workspace import endpoint
    from models.plan_case_view import PlanCaseSavedView
    g=governance;client,db,url=g["client"],g["db"],endpoint(g)
    first=request_review(g,reviewers=[g["users"][2].id]);second=request_review(g,reviewers=[g["users"][1].id])
    db.get(CaseReview,first["id"]).name="Literal_%"
    db.query(ReviewWorkspace).filter_by(review_id=second["id"]).one().archived=True;db.commit()
    before=db.query(CaseReviewEvent).count()
    assert client.get(url).json()["data"]["total"]==1
    raw=dict(conditions=[condition("name","_%","contains"),condition("lifecycle",["archived"],"belongs_to")],logic="or")
    pages=[client.get(url,params=dict(filters=json.dumps(raw),size=1,page=i)).json()["data"] for i in (1,2)]
    assert all(page["total"]==2 for page in pages)
    assert {item["id"] for page in pages for item in page["items"]}=={first["id"],second["id"]}
    filters=dict(filterConditions=raw["conditions"],filterLogic="or",scope="reviewByMe")
    saved=client.post(url+"/views",json=dict(name="首页视图",filters=filters))
    assert saved.status_code==200,saved.text
    row=saved.json()["data"];assert db.get(PlanCaseSavedView,row["id"]).category=="review-index"
    assert client.get(url+"/candidate-views").json()["data"]==[]
    assert client.delete(url+"/candidate-views/"+row["id"]).status_code==404
    assert client.put(url+"/views/"+row["id"],json={"name":"Rename"}).json()["data"]["filters"]==filters
    assert client.post(url+"/views",json=dict(name="Rename",filters=filters)).status_code==409
    for i in range(9):assert client.post(url+"/views",json=dict(name=f"首页{i}",filters=filters)).status_code==200
    assert client.post(url+"/views",json=dict(name="超额",filters=filters)).status_code==409
    g["state"]["user"]=g["users"][1]
    assert client.get(url+"/views").json()["data"]==[]
    assert client.put(url+"/views/"+row["id"],json={"name":"越权"}).status_code==404
    assert client.delete(url+"/views/"+row["id"]).status_code==404
    g["state"]["user"]=g["users"][0]
    assert client.get(url.replace(g["cases"][0].project_id,g["foreign"].project_id)+"/views").status_code==403
    for invalid in (dict(filterConditions=[condition("priority","P0")]),{**filters,"scope":[]},{**filters,"mine":True},dict(filterConditions=[condition("caseCount",9223372036854775808)])):
        assert client.post(url+"/views",json=dict(name="非法",filters=invalid)).status_code==422
    assert client.get(url,params={"filters":json.dumps(dict(conditions=[condition("caseCount",9223372036854775808)]))}).status_code==422
    assert db.query(CaseReviewEvent).count()==before


@pytest.mark.parametrize("raw",["{",[],{"conditions":[condition("priority","P0")]},
    {"conditions":[condition("name","x","gt")]},{"conditions":[condition("passRate",True)]},
    {"conditions":[condition("tags",-1,"count_gt")]},{"conditions":[condition("startTime",["bad","worse"],"between")]},
    {"conditions":[condition("caseCount",[10,1],"between")]},{"conditions":[condition("createdAt","bad","gt")]},
    {"conditions":[condition("mode",{"secret":"x"})]},
    {"conditions":[condition("caseCount",9223372036854775808)]},
    {"conditions":[condition("mode",["bogus"],"belongs_to")]},
    {"conditions":[condition("lifecycle",["bogus"],"belongs_to")]}])
def test_invalid_review_filters_are_explicitly_rejected(raw):
    with pytest.raises(HTTPException) as exc:parse(raw)
    assert exc.value.status_code==422
