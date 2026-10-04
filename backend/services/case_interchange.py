"""XMind 标准 ZIP/JSON/XML 互操作；只读取内存，不解压任意路径。"""

import io
import json
import uuid
import zipfile
from fastapi import HTTPException
from defusedxml import ElementTree
from core.logger import logger

MAX_ARCHIVE = 10 * 1024 * 1024
MAX_EXPANDED = 20 * 1024 * 1024


def topic(title, children=None, **extra):
    row = {"id": str(uuid.uuid4()), "class": "topic", "title": title, **extra}
    if children:
        row["children"] = {"attached": children}
    return row


def export_xmind(cases, module_paths=None):
    branches = []
    groups = {(): branches}
    for case in cases:
        steps = [
            topic(
                str(step.get("action", "")),
                [topic("预期结果", [topic(str(step.get("expected", "")))])],
            )
            for step in (case.steps or [])
        ]
        fields = [
            topic("前置条件", [topic(case.precondition or "")]),
            topic("步骤", steps),
            *([topic("文本描述", [topic(case.text_description or "")]), topic("预期结果", [topic(case.expected_result or "")])] if case.case_edit_type == "TEXT" else []),
            topic("备注", [topic(case.description or "")]),
            topic("需求关联", [topic(case.requirement_ref or "")]),
        ]
        # 核心用例名、前置、步骤和预期为普通标准节点；ATS 属性只用于无损补充。
        metadata = {
            key: getattr(case, key)
            for key in [
                "case_code",
                "type",
                "priority",
                "tags",
                "is_automated",
                "requirement_ref",
                "module_path",
                "template_id",
                "custom_fields",
                "steps",
                "case_edit_type",
                "text_description",
                "expected_result",
                "description",
            ]
        }
        parts = tuple(
            part
            for part in (module_paths or {})
            .get(case.module_id, case.module_path or "")
            .split("/")
            if part
        )
        for index in range(1, len(parts) + 1):
            key = parts[:index]
            if key not in groups:
                node = topic(parts[index - 1], [])
                node["children"] = {"attached": []}
                groups[key[:-1]].append(node)
                groups[key] = node["children"]["attached"]
        groups[parts].append(
            topic(
                case.name,
                fields,
                labels=["用例"],
                markers=[{"markerId": "priority-" + str(int(case.priority[1]) + 1)}],
                atsCase=metadata,
            )
        )
    sheet = {
        "id": str(uuid.uuid4()),
        "class": "sheet",
        "title": "测试用例",
        "rootTopic": topic("测试用例", branches),
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", json.dumps([sheet], ensure_ascii=False))
        archive.writestr(
            "metadata.json", json.dumps({"creator": {"name": "ATS", "version": "1"}})
        )
        archive.writestr(
            "manifest.json",
            json.dumps({"file-entries": {"content.json": {}, "metadata.json": {}}}),
        )
    return output.getvalue()


def children(node):
    value = node.get("children", {})
    return value.get("attached", []) if isinstance(value, dict) else []


def read_xmind(content):
    if len(content) > MAX_ARCHIVE:
        raise HTTPException(413, "XMind 文件超过10MiB")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            infos = archive.infolist()
            if len(infos) > 5000 or sum(i.file_size for i in infos) > MAX_EXPANDED:
                raise HTTPException(413, "XMind 解压内容超过限制")
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise HTTPException(422, "XMind 包含重复文件名")
            if "content.json" in names:
                sheets = json.loads(archive.read("content.json"))
                roots = [sheet["rootTopic"] for sheet in sheets]
            elif "content.xml" in names:
                root = ElementTree.fromstring(archive.read("content.xml"))

                def xml_topic(node, depth=0):
                    if depth > 100:
                        raise HTTPException(422, "XMind 节点层级过深")
                    title = node.find("{*}title")
                    attached = node.findall("{*}children/{*}topics/{*}topic")
                    return topic(
                        title.text or "" if title is not None else "",
                        [xml_topic(child, depth + 1) for child in attached],
                    )

                roots = [xml_topic(node) for node in root.findall("{*}sheet/{*}topic")]
            else:
                raise HTTPException(422, "XMind 缺少 content.json/content.xml")
        rows = []
        visited = 0
        reserved = {
            "前置条件",
            "前提条件",
            "步骤",
            "测试步骤",
            "步骤描述",
            "预期结果",
            "期望结果",
            "需求关联",
            "文本描述",
            "备注",
        }

        def flatten(node):
            return "\n".join(
                [str(node.get("title", ""))] + [flatten(c) for c in children(node)]
            )

        def walk(node, path, depth=0):
            nonlocal visited
            visited += 1
            if visited > 10000 or depth > 100:
                raise HTTPException(422, "XMind 节点数量或层级过大")
            if not isinstance(node, dict) or not isinstance(node.get("title"), str):
                raise HTTPException(422, "XMind 节点格式不合法")
            nested = children(node)
            by_title = {child.get("title"): child for child in nested}
            is_case = (
                bool(set(by_title) & reserved)
                or "用例" in node.get("labels", [])
                or isinstance(node.get("atsCase"), dict)
            )
            if is_case or (not nested and depth > 0):
                metadata = node.get("atsCase", {})
                steps = []
                step_node = next(
                    (
                        by_title[k]
                        for k in ["步骤", "测试步骤", "步骤描述"]
                        if k in by_title
                    ),
                    None,
                )
                if step_node:
                    for index, step in enumerate(children(step_node), 1):
                        expected = []
                        for child in children(step):
                            (
                                expected.extend(flatten(c) for c in children(child))
                                if child.get("title") in {"预期结果", "期望结果"}
                                else expected.append(flatten(child))
                            )
                        steps.append(
                            {
                                "step": index,
                                "action": step.get("title", ""),
                                "expected": "\n".join(expected),
                            }
                        )
                pre = by_title.get("前置条件", by_title.get("前提条件"))
                req = by_title.get("需求关联")
                priority = metadata.get("priority", "P2")
                for marker in node.get("markers", []):
                    value = marker.get("markerId", "")
                    if value in {
                        "priority-1",
                        "priority-2",
                        "priority-3",
                        "priority-4",
                    }:
                        priority = "P" + str(int(value[-1]) - 1)
                rows.append(
                    {
                        "ID": metadata.get("case_code"),
                        "用例名称": node["title"],
                        "用例等级": priority,
                        "用例类型": metadata.get("type", "functional"),
                        "前置条件": (
                            "\n".join(flatten(c) for c in children(pre)) if pre else ""
                        ),
                        "测试步骤": json.dumps(steps, ensure_ascii=False),
                        "需求关联": metadata.get("requirement_ref")
                        or (
                            "\n".join(flatten(c) for c in children(req)) if req else ""
                        ),
                        "标签": ",".join(metadata.get("tags") or []),
                        "是否自动化": "是" if metadata.get("is_automated") else "否",
                        "描述方式": metadata.get("case_edit_type", "TEXT" if "文本描述" in by_title else "STEP"),
                        "文本描述": metadata.get("text_description") or ("\n".join(flatten(c) for c in children(by_title["文本描述"])) if "文本描述" in by_title else ""),
                        "文本预期结果": metadata.get("expected_result") or ("\n".join(flatten(c) for c in children(by_title["预期结果"])) if "预期结果" in by_title else ""),
                        "备注": metadata.get("description") or ("\n".join(flatten(c) for c in children(by_title["备注"])) if "备注" in by_title else ""),
                        "模板ID": metadata.get("template_id"),
                        "自定义字段": json.dumps(
                            metadata.get("custom_fields") or {}, ensure_ascii=False
                        ),
                    }
                )
                rows[-1]["所属模块"] = "/".join(path[1:])
            else:
                for child in nested:
                    walk(child, path + [node["title"]], depth + 1)

        for root in roots:
            walk(root, [])
        if not rows:
            raise HTTPException(422, "XMind 中没有可导入的用例")
        return rows
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("XMind 文件解析失败")
        raise HTTPException(422, "XMind 格式错误或包含不安全内容") from exc
