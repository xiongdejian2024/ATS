"""可注入报告接收器；库只依赖此接口，默认使用标准日志。"""
import logging
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

logger = logging.getLogger(__name__)


class LoggingAttachments:
    def __call__(self, body, name=None, attachment_type=None, extension=None):
        # 通信内容可包含凭证，不把原内容输出到日志。
        logger.info("库报告附件：%s，类型：%s", name or "未命名", attachment_type or "文本")

    def file(self, source, name=None, attachment_type=None, extension=None):
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(path)
        self(None, name or path.name, attachment_type, extension)


class LoggingReporter:
    attach = LoggingAttachments()
    attachment_type = SimpleNamespace(URI_LIST="text/uri-list", TEXT="text/plain", JSON="application/json", HTML="text/html")

    @contextmanager
    def step(self, title):
        logger.info("库操作步骤开始：%s", title)
        try:
            yield
        except Exception:
            logger.exception("库操作步骤失败：%s", title)
            raise
        else:
            logger.info("库操作步骤完成：%s", title)


_reporter = LoggingReporter()


def set_reporter(reporter=None):
    """由调用方注入 Allure 等报告接收器，返回旧接收器便于恢复。"""
    global _reporter
    previous = _reporter
    _reporter = reporter if reporter is not None else LoggingReporter()
    return previous


def __getattr__(name):
    if name in {"step", "attach", "attachment_type"}:
        return getattr(_reporter, name)
    raise AttributeError(name)
