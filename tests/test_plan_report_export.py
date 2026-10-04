"""中文 PDF 内容、长文本分页及用户标记隔离验收。"""
from io import BytesIO

import pytest
from pypdf import PdfReader

from services.plan_report_export import render_plan_report


def test_pdf_chinese_steps_group_and_untrusted_text():
    payload = dict(id="PDF-软件验收", planName="回归计划", status="completed", summary='<img src="file:///秘密"/> & 原样文字',
        report=dict(total=1, counts=dict(passed=1), passRate=100, passThreshold=90, outcome="passed",
                    cases=[dict(caseId="c", caseName="中文用例", result="passed", notes="中文实际结果", stepResults=[dict(result="passed", actual="实际返回成功")])]),
        caseSnapshot=[dict(id="c", steps=[dict(action="输入参数", expected="成功")])],
        plans=[dict(planName="子计划", status="completed", report=dict(total=1, passRate=100))])
    data = render_plan_report(payload)
    assert data.startswith(b"%PDF-")
    reader = PdfReader(BytesIO(data))
    text = "\n".join(page.extract_text() for page in reader.pages)
    for expected in ["回归计划", "中文用例", "子计划", "输入参数", "实际返回成功", '<img src="file:///秘密"/> & 原样文字']:
        assert expected in text
    assert not reader.get_fields()


def test_pdf_long_report_paginates_without_losing_last_case():
    cases = [dict(caseId=str(i), caseName=f"分页用例{i}", result="failed", notes="较长的实际结果说明。" * 120) for i in range(12)]
    data = render_plan_report(dict(id="长报告", planName="分页回归", report=dict(total=12, counts=dict(failed=12), cases=cases)))
    reader = PdfReader(BytesIO(data))
    assert len(reader.pages) > 2
    text = "\n".join(page.extract_text() for page in reader.pages)
    assert "分页用例11" in text
    assert all("ATS 自动化测试平台" in page.extract_text() for page in reader.pages)


def test_pdf_requires_explicit_report():
    with pytest.raises(ValueError, match="report"):
        render_plan_report({"id": "无报告"})


def test_pdf_partial_step_uses_recorded_index_and_group_defects():
    data = render_plan_report(dict(id="部分步骤", groupName="版本回归组", summary={"conclusion":"已复核"},
        report=dict(total=1, cases=[dict(caseId="c", caseName="分步用例", result="failed",
            snapshot={"steps":[{"action":"第一步"},{"action":"第二步操作","expected":"第二步预期"}]},
            stepResults=[dict(index=1,result="failed",actual="第二步实际结果")])],
            bugs=[dict(title="界面缺陷",status="open",description="显示异常")]),
        children=[dict(planName="子计划",status="failed",report={"total":1,"passRate":0})]))
    extracted = "\n".join(p.extract_text() for p in PdfReader(BytesIO(data)).pages)
    assert all(value in extracted for value in ["第二步操作","第二步预期","第二步实际结果","界面缺陷","显示异常","已复核"])
    assert "操作：第一步" not in extracted
