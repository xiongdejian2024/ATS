"""高级筛选组合与视图更新的隔离回归，不执行台架。"""

from datetime import datetime, timezone, timedelta
import pytest
from fastapi import HTTPException
from test_case_governance import governance  # noqa: F401
from services.case_query import parse_filters, matches, query_cases
from models.case_governance import CaseVersion


def test_blank_defaults_do_not_broaden_or_and_zero_false_are_kept():
    conditions, logic = parse_filters(
        {
            "logic": "or",
            "conditions": [
                {"field": "name", "operator": "contains", "value": ""},
                {"field": "moduleId", "operator": "belongs_to"},
                {"field": "tags", "operator": "count_gt", "value": 0},
                {"field": "isAutomated", "operator": "equals", "value": False},
            ],
        }
    )
    assert logic == "or"
    assert [c["value"] for c in conditions] == [0, False]
    assert matches([], "count_lt", 1)
    assert not matches(None, "count_gt", 0)
    assert matches(["冒烟"], "count_gt", 0)


def test_dates_compare_instants_and_plain_text_keeps_literal_semantics():
    actual = datetime(2026, 10, 5, 8, tzinfo=timezone(timedelta(hours=8)))
    assert matches(actual, "between", ["2026-10-05T00:00:00Z", "2026-10-05T01:00:00Z"])
    assert matches(actual, "gt", "2026-10-04T23:59:59Z")
    assert matches(actual, "equals", 1791158400000)
    assert not matches("2026-10-05T08:00:00+08:00", "equals", "2026-10-05T00:00:00Z")
    assert matches(
        "2026-10-05T08:00:00+08:00",
        "between",
        ["2026-10-05T00:00:00Z", "2026-10-05T01:00:00Z"],
    )
    for value in [["2026-10-06", "2026-10-05"], ["错误日期", "2026-10-05"]]:
        with pytest.raises(HTTPException) as exc:
            matches(actual, "between", value)
        assert exc.value.status_code == 422


@pytest.mark.parametrize(
    "condition",
    [
        {"field": "tags", "operator": "count_gt", "value": True},
        {"field": "tags", "operator": "count_lt", "value": -1},
        {"field": "createdAt", "operator": "between", "value": ["2026-10-05"]},
        {"field": "name", "operator": "未知", "value": "a"},
    ],
)
def test_invalid_conditions_are_rejected(condition):
    with pytest.raises(HTTPException) as exc:
        parse_filters({"conditions": [condition]})
    assert exc.value.status_code == 422


def test_view_update_preserves_id_owner_and_versions(governance):
    g = governance
    client, url = g["client"], g["base"] + "/views"
    versions = g["db"].query(CaseVersion).count()
    first = client.post(
        url, json={"name": "原视图", "filters": {"search": "旧值"}}
    ).json()["data"]
    filters = {
        "filterLogic": "or",
        "filterConditions": [{"field": "tags", "operator": "count_lt", "value": 1}],
    }
    response = client.put(
        url + "/" + first["id"], json={"name": "长" * 255, "filters": filters}
    )
    assert response.status_code == 200, response.text
    updated = response.json()["data"]
    assert updated["id"] == first["id"] and updated["filters"] == filters
    assert len(updated["name"]) == 255
    assert (
        client.put(url + "/" + first["id"], json={"name": "仅改名"}).json()["data"][
            "filters"
        ]
        == filters
    )
    copy = client.post(url, json={"name": "另存", "filters": filters}).json()["data"]
    assert copy["id"] != first["id"] and copy["filters"] == filters
    for invalid in [
        None,
        {"filterLogic": "错"},
        {"filterConditions": [{"field": "name", "operator": "错"}]},
    ]:
        assert (
            client.put(
                url + "/" + first["id"], json={"name": "无效", "filters": invalid}
            ).status_code
            == 422
        )
    assert (
        client.put(
            url + "/" + first["id"], json={"name": "另存", "filters": {}}
        ).status_code
        == 409
    )
    assert client.get(url).json()["data"][-1]["filters"] == filters
    g["state"]["user"] = g["users"][1]
    assert (
        client.put(
            url + "/" + first["id"], json={"name": "越权", "filters": {}}
        ).status_code
        == 404
    )
    assert g["db"].query(CaseVersion).count() == versions


def test_query_empty_defaults_do_not_broaden_or_scope(governance):
    g = governance
    result = query_cases(
        g["db"],
        g["project"].id,
        filters={
            "logic": "or",
            "conditions": [
                {"field": "name", "operator": "contains", "value": "用例0"},
                {"field": "id", "operator": "contains", "value": ""},
                {"field": "moduleId", "operator": "belongs_to", "value": []},
            ],
        },
    )
    assert result["total"] == 1 and result["items"][0].id == g["cases"][0].id
