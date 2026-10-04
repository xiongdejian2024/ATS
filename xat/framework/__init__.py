"""XAT 公共接口，按需导入，导入包时不创建日志或结果文件。"""

from importlib import import_module

_EXPORTS = {
    "TestConfig": ".config",
    "get_test_config": ".config",
    "get_logger": ".logger",
    "log_debug": ".logger",
    "log_info": ".logger",
    "log_warning": ".logger",
    "log_error": ".logger",
    "log_critical": ".logger",
    "pytest_configure": ".hooks",
    "pytest_sessionstart": ".hooks",
    "pytest_sessionfinish": ".hooks",
    "pytest_collection_modifyitems": ".hooks",
    "pytest_runtest_setup": ".hooks",
    "pytest_runtest_teardown": ".hooks",
    "pytest_runtest_logreport": ".hooks",
    "get_hook_registry": ".hooks",
    "assert_response_success": ".utils",
    "assert_response_error": ".utils",
    "create_test_user": ".utils",
    "create_test_project": ".utils",
    "attach_screenshot": ".utils",
    "attach_text": ".utils",
    "attach_json": ".utils",
    "attach_html": ".utils",
    "step": ".utils",
    "label": ".utils",
    "description": ".utils",
    "severity": ".utils",
}
__all__ = list(_EXPORTS)


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(name)
    value = getattr(import_module(_EXPORTS[name], __name__), name)
    globals()[name] = value
    return value
