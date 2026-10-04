"""将计划或计划组的报告快照排版为中文 PDF，不访问外部资源。"""
from io import BytesIO
from pathlib import Path
from threading import Lock
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from core.logger import logger


STATUS_NAMES = {
    "pending": "未执行", "queued": "排队中", "waiting": "等待中", "running": "执行中",
    "completed": "已通过", "passed": "通过", "failed": "失败", "error": "错误",
    "blocked": "阻塞", "skipped": "跳过", "cancelled": "已取消", "cancelling": "取消中",
    "needs_confirmation": "等待核对节点",
}
FONT_NAME = "ATS-NotoSansSC"
_FONT_LOCK = Lock()


def _register_font():
    # 嵌入开源中文字体，离线阅读无需依赖操作系统或 PDF 阅读器语言包。
    with _FONT_LOCK:
        if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(FONT_NAME, str(Path(__file__).parent / "fonts" / "NotoSansSC-Regular.ttf")))


def render_plan_report(payload: dict) -> bytes:
    """输入已授权、已序列化的报告；保持快照中的结果，不重新计算执行结果。"""
    try:
        return _render(payload)
    except Exception:
        logger.exception("计划报告 PDF 生成失败：批次={}", payload.get("id", "未指定") if isinstance(payload, dict) else "无效输入")
        raise


def _render(payload: dict) -> bytes:
    if not isinstance(payload, dict) or not isinstance(payload.get("report"), dict):
        raise ValueError("报告必须包含已序列化的 report 对象")
    _register_font()
    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName = FONT_NAME
        style.wordWrap = "CJK"
    styles.add(ParagraphStyle("ATS标题", parent=styles["Title"], fontSize=20, leading=28,
                              textColor=colors.HexColor("#17365D"), spaceAfter=14))
    styles.add(ParagraphStyle("ATS正文", fontName=FONT_NAME, fontSize=9, leading=14,
                              wordWrap="CJK", spaceAfter=5))
    styles.add(ParagraphStyle("ATS小字", parent=styles["ATS正文"], fontSize=8, leading=12))
    styles.add(ParagraphStyle("ATS小标题", parent=styles["Heading2"], fontSize=12, leading=18,
                              spaceBefore=10, spaceAfter=8, keepWithNext=True, textColor=colors.HexColor("#17365D")))

    def p(text, style="ATS正文"):
        # 报告内容只作为纯文本，阻止用户输入变成 ReportLab 标记或外部图片地址。
        value = str(text if text is not None else "—")
        return Paragraph(escape(value).replace("\n", "<br/>"), styles[style])

    def table(rows, widths):
        result = Table([[p(cell, "ATS小字") for cell in row] for row in rows],
                       colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1,
                       splitInRow=1)
        result.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EFF8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("LINEBELOW", (0, 0), (-1, 0), .5, colors.HexColor("#A8B7CD")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return result

    report = payload["report"]
    title = payload.get("groupName") or payload.get("planName") or payload.get("name") or "测试计划"
    status = report.get("outcome") or payload.get("status", "pending")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm, title=f"ATS 测试报告 - {title}",
                            author="ATS 自动化测试平台")
    width = A4[0] - 36 * mm
    story = [p("ATS 测试报告", "ATS标题"), p(title, "ATS小标题"),
             p(f"批次：{payload.get('id', '未指定')}"),
             p(f"状态：{STATUS_NAMES.get(status, status)}　开始：{payload.get('startedAt') or '—'}　完成：{payload.get('completedAt') or '—'}")]
    counts = report.get("counts") or {}
    story += [table([
        ["执行项", "通过", "失败 / 错误", "通过率", "通过阈值"],
        [report.get("total", 0), counts.get("passed", 0),
         f"{counts.get('failed', 0)} / {counts.get('error', 0)}",
         f"{report.get('passRate', 0)}%", f"{report.get('passThreshold', '—')}%"],
    ], [width / 5] * 5), Spacer(1, 8)]
    summary = payload.get("summary") or report.get("summary") or payload.get("notes")
    if isinstance(summary, dict):
        summary = "\n".join(f"{label}：{summary.get(key) or '—'}" for key, label in
                            [("conclusion", "结论"), ("risk", "风险"), ("notes", "说明")])
    story += [p("报告总结", "ATS小标题"), p(summary or "尚未填写总结。")]

    plans = payload.get("children") or payload.get("plans") or report.get("plans") or []
    if plans:
        rows = [["计划", "状态", "执行项", "通过率"]]
        for plan in plans:
            detail = plan.get("report") or {}
            value = plan.get("status", "pending")
            rows.append([plan.get("planName") or plan.get("name") or plan.get("planId"),
                         STATUS_NAMES.get(value, value), detail.get("total", plan.get("total", 0)),
                         f"{detail.get('passRate', plan.get('passRate', 0))}%"])
        story += [p("计划组明细", "ATS小标题"), table(rows, [width * .5, width * .2, width * .15, width * .15])]

    cases = report.get("cases") or []
    if cases:
        rows = [["用例 / 测试点", "测试套", "执行结果", "实际结果 / 说明"]]
        for case in cases:
            value = case.get("result", "pending")
            name = case.get("caseName") or case.get("name") or case.get("caseId")
            point = case.get("pointName") or case.get("testPointName")
            rows.append([f"{name}\n{point}" if point else name, case.get("suiteName", "手工测试"),
                         STATUS_NAMES.get(value, value), case.get("notes") or "—"])
        story += [p("用例执行明细", "ATS小标题"), table(rows, [width * .3, width * .18, width * .14, width * .38])]

    snapshots = {c.get("id"): c for c in payload.get("caseSnapshot", [])}
    manual = payload.get("manualResults") or {}
    for case in cases:
        snapshot = case.get("snapshot") or snapshots.get(case.get("caseId"), {})
        steps = case.get("stepResults") or (manual.get(case.get("caseId")) or {}).get("stepResults") or []
        if not steps:
            continue
        story.append(p(f"步骤明细：{case.get('caseName') or snapshot.get('name') or case.get('caseId')}", "ATS小标题"))
        rows = [["步骤", "操作与预期", "结果", "实际结果"]]
        original = snapshot.get("steps") or []
        for i, step in enumerate(steps):
            index = step.get("index", i)
            source = original[index] if 0 <= index < len(original) and isinstance(original[index], dict) else {}
            value = step.get("result", "pending")
            rows.append([index + 1,
                         f"操作：{step.get('action', source.get('action', '—'))}\n预期：{step.get('expected', source.get('expected', '—'))}",
                         STATUS_NAMES.get(value, value), step.get("actual") or step.get("actualResult") or step.get("notes") or "—"])
        story.append(table(rows, [width * .08, width * .45, width * .13, width * .34]))

    bugs = payload.get("bugs") or report.get("bugs") or []
    if bugs:
        story += [p("关联缺陷", "ATS小标题"), table([["缺陷", "状态", "说明"]] + [
            [bug.get("title") or bug.get("name") or bug.get("id"), bug.get("status", "—"), bug.get("description", "—")]
            for bug in bugs], [width * .4, width * .2, width * .4])]

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(FONT_NAME, 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(18 * mm, 10 * mm, "ATS 自动化测试平台")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"第 {document.page} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    data = buffer.getvalue()
    logger.info("计划报告 PDF 已生成：批次={}，用例项={}，字节数={}", payload.get("id", "未指定"), len(cases), len(data))
    return data
