"""将已盘点的功能源码迁入 XAT，记录来源和凭证替换，不运行迁入代码。"""

import argparse
import ast
import hashlib
import json
import logging
import re
import shutil
import io
import tokenize
from pathlib import Path

logger = logging.getLogger("xat.migration")
ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    "automotive_sdk": "xat_ecu",
    "ecu_simulator": "xat_ecu.legacy",
    "sdk_interface": "xat_ecu.api",
    "sat_framework": "framework.automotive",
    "test_case_dp2": "xat_cases.dp2",
    "test_case": "xat_cases.legacy",
}
SECRET_NAME = re.compile(r"(?:pass(?:word|wd)?|secret|token|api_key|app_key|access_key|authorization|private_key)", re.I)
IGNORED = {"__pycache__", ".git", ".idea", ".pytest_cache", "graphify-out", "venv", ".venv", "logs"}


def rewrite_names(source):
    for old, new in NAMES.items():
        # 只改变绝对导入与模块路径字符串，同名参数/变量不改名。
        source = re.sub(r"(?m)^(\s*from\s+)" + old + r"(?=\.|\s)", r"\g<1>" + new, source)
        def replace_import(match):
            indent, suffix, alias = match.group(1), match.group(2) or "", match.group(3)
            if alias:
                return indent + "import " + new + suffix + alias
            if not suffix:
                return indent + "import " + new + " as " + old
            return indent + "import " + new + " as " + old + "\n" + indent + "import " + new + suffix
        source = re.sub(r"(?m)^(\s*)import " + old + r"(\.[A-Za-z0-9_.]+)?(\s+as\s+\w+)?(?=\s*(?:#|$))", replace_import, source)
        for quote in ['"', "'"]:
            source = source.replace(quote + old + ".", quote + new + ".")
        source = source.replace("/" + old + "/", "/" + new.replace(".", "/") + "/")
    # 原模块化库的兼容模块含有错误转义的三引号，修正为 Python 文档字符串。
    source = re.sub(r'^\\"\\"\\"\s*$', '"""', source, flags=re.M)
    source = source.replace("xat_cases.legacy.soa.case_helper.ConfigCenter.configfile_utils", "xat_ecu.api.config_center.configfile_utils")
    source = source.replace("xat_cases.legacy.soa.case_helper.ConfigCenter.ConfigMasterV2T_pb2", "xat_ecu.api.config_center.ConfigMasterV2T_pb2")
    source = source.replace("xat_cases.legacy.soa.case_helper.ConfigCenter.VehicleCloud_pb2", "xat_ecu.api.config_center.VehicleCloud_pb2")
    source = source.replace("xat_cases.legacy.bgm.s2s.case_helper.contants", "xat_ecu.legacy.soa_partner.src.state")
    return source


def redact_config(raw, logical_path, suffix):
    """结构化资源中只替换凭证字段，保留协议和车型数据。"""
    import yaml
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        logger.exception("资源编码不是 UTF-8，按 GB18030 转换：%s", logical_path)
        text = raw.decode("gb18030")
    try:
        documents = [json.loads(text)] if suffix == ".json" else list(yaml.safe_load_all(text))
    except (ValueError, yaml.YAMLError):
        logger.exception("资源不符合配置语法，保留待审计：%s", logical_path)
        return raw, []
    recorded = []

    def walk(value, path):
        if isinstance(value, dict):
            for key, item in value.items():
                if SECRET_NAME.search(str(key)) and isinstance(item, str) and len(item) >= 5 and not item.startswith("${"):
                    name = "XAT_CREDENTIAL_" + re.sub(r"[^A-Za-z0-9]", "_", logical_path + "_" + path + "_" + str(key)).upper()
                    value[key] = "${" + name + "}"
                    recorded.append({"名称": str(key), "环境变量": name})
                else:
                    walk(item, path + "_" + str(key))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, path + "_" + str(index))

    for document in documents:
        walk(document, "")
    if not recorded:
        return raw, recorded
    result = json.dumps(documents[0], ensure_ascii=False, indent=2) if suffix == ".json" else yaml.safe_dump_all(documents, allow_unicode=True, sort_keys=False)
    return result.encode(), recorded


def redact_python(source, logical_path):
    """保留调用与接口，将带敏感名称的常量替换为环境变量注入。"""
    if len(source) > 512_000:
        return source, []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        logger.exception("迁移源码存在语法问题，交由编译审计处理：%s", logical_path)
        return source, []
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    changes, recorded = {}, []

    def replace_value(value, name):
        if not SECRET_NAME.search(name):
            return
        if isinstance(value, ast.Constant):
            literals = [value]
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr in {"b64decode", "b64encode", "encode", "decode"}:
            literals = list(ast.walk(value))
        else:
            return
        for node in literals:
            if not isinstance(node, ast.Constant) or not isinstance(node.value, (str, bytes)) or len(node.value) < 5:
                continue
            if isinstance(node.value, str) and (node.value.startswith("XAT_") or "{" in node.value or node.value.lower() in {"password", "utf-8", "ascii", "latin-1"}):
                continue
            key = "XAT_CREDENTIAL_" + re.sub(r"[^A-Za-z0-9]", "_", logical_path + "_" + name).upper()
            # AST 列号使用 UTF-8 字节；转换为字符串位置，避免中文前缀错位。
            start = offsets[node.lineno - 1] + len(lines[node.lineno - 1].encode()[:node.col_offset].decode())
            end = offsets[node.end_lineno - 1] + len(lines[node.end_lineno - 1].encode()[:node.end_col_offset].decode())
            expression = f'__import__("os").environ.get({key!r}, "")'
            if isinstance(node.value, bytes):
                expression += ".encode()"
            changes[(start, end)] = expression
            recorded.append({"名称": name, "环境变量": key, "行": node.lineno})

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, (ast.Name, ast.Attribute)):
                    replace_value(node.value, target.id if isinstance(target, ast.Name) else target.attr)
        elif isinstance(node, ast.AnnAssign) and node.value and isinstance(node.target, ast.Name):
            replace_value(node.value, node.target.id)
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    replace_value(value, key.value)
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg:
                    replace_value(keyword.value, keyword.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for argument, value in zip(node.args.args[-len(node.args.defaults):] if node.args.defaults else [], node.args.defaults):
                replace_value(value, argument.arg)
    for (start, end), value in sorted(changes.items(), reverse=True):
        source = source[:start] + value + source[end:]
    return source, recorded


def migrate_tree(source, destination, label, manifest):
    copied = 0
    for path in sorted(source.rglob("*")):
        if not path.is_file() or any(part in IGNORED for part in path.relative_to(source).parts):
            continue
        relative = path.relative_to(source)
        if path.suffix in {".pyc", ".pyo", ".log", ".out"} or path.name in {".DS_Store", ".env", ".env.test"}:
            continue
        if path.suffix in {".pem", ".key"} and b"PRIVATE KEY" in path.read_bytes():
            manifest.append({"组": label, "来源": str(relative), "状态": "用户提供私钥，不纳入源码"})
            continue
        if label == "ECU库" and relative.parts[0] in {"test", "testsdk"}:
            target = ROOT / "xat/cases/src/xat_cases/library_archive" / relative
        else:
            target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = path.read_bytes()
        credentials = []
        if path.suffix == ".py":
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            value = raw.decode(encoding)
            value = rewrite_names(value)
            if label in {"ECU库", "库接口"} and relative.parts[0] not in {"test", "testsdk"}:
                value = re.sub(r"^import allure\s*,\s*(.+)$", r"from xat_ecu import reporting as allure\nimport \1", value, flags=re.M)
                value = re.sub(r"^import allure\s*$", "from xat_ecu import reporting as allure", value, flags=re.M)
            value, credentials = redact_python(value, label + "/" + str(relative))
            target.write_text(value, encoding="utf-8")
        elif path.suffix in {".json", ".yaml", ".yml"}:
            value, credentials = redact_config(raw, label + "/" + str(relative), path.suffix)
            target.write_bytes(value)
        else:
            shutil.copy2(path, target)
        manifest.append({"组": label, "来源": str(relative), "目标": str(target.relative_to(ROOT)), "源SHA256": hashlib.sha256(raw).hexdigest(), "目标SHA256": hashlib.sha256(target.read_bytes()).hexdigest(), "凭证替换": credentials, "状态": "已迁入，待功能验证"})
        copied += 1
    logger.info("迁入完成：%s，文件数=%s", label, copied)


def main():
    parser = argparse.ArgumentParser(description="XAT 功能源码迁移，不运行台架")
    parser.add_argument("--sat-root", type=Path, default=ROOT.parent / "sat")
    parser.add_argument("--ecu-root", type=Path, default=ROOT.parent / "ecu-simulator")
    parser.add_argument("--part", choices=["modern", "framework", "interfaces", "legacy", "cases", "tools", "resources", "all"], required=True)
    options = parser.parse_args()
    library = ROOT / "xat/packages/ecu/src/xat_ecu"
    plans = {
        "modern": [(options.ecu_root / "src/automotive_sdk", library, "模块化ECU库")],
        "framework": [(options.sat_root / "sat_framework", ROOT / "xat/framework/automotive", "pytest框架")],
        "interfaces": [(options.sat_root / "sdk_interface", library / "api", "库接口")],
        "legacy": [(options.ecu_root / "ecu_simulator", library / "legacy", "ECU库")],
        "cases": [(options.sat_root / "test_case", ROOT / "xat/cases/src/xat_cases/legacy", "用例"), (options.sat_root / "test_case_dp2", ROOT / "xat/cases/src/xat_cases/dp2", "DP2用例")],
        "tools": [(options.sat_root / "tools", ROOT / "xat/tools", "工具")],
        "resources": [(options.sat_root / "bench_config", ROOT / "xat/bench_config", "台架配置"), (options.sat_root / "test_case/soa/case_helper/ConfigCenter", library / "api/config_center", "共享配置协议")],
    }
    selected = [entry for entries in plans.values() for entry in entries] if options.part == "all" else plans[options.part]
    manifest_path = ROOT / "docs/migration/迁移清单.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    labels = {entry[2] for entry in selected}
    manifest = [entry for entry in manifest if entry["组"] not in labels]
    for source, destination, label in selected:
        migrate_tree(source, destination, label, manifest)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    try:
        main()
    except Exception:
        logger.exception("XAT 源码迁移失败")
        raise
