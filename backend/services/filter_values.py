"""筛选时间比较统一到UTC，复用标准库，不依赖数据库JSON方言。"""

from datetime import date, datetime, time, timezone
import re
from fastapi import HTTPException


def temporal(value):
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, date):
        result = datetime.combine(value, time.min)
    elif isinstance(value, str):
        result = datetime.fromisoformat(value)
    elif type(value) in {int, float}:
        result = datetime.fromtimestamp(value / 1000, timezone.utc)
    else:
        raise ValueError("筛选时间类型不合法")
    return (
        result.replace(tzinfo=timezone.utc)
        if result.tzinfo is None
        else result.astimezone(timezone.utc)
    )


def comparable(actual, expected, *, date_text=False):
    if isinstance(actual, (date, datetime)):
        try:
            return temporal(actual), temporal(expected)
        except (ValueError, TypeError, OverflowError, OSError) as exc:
            raise HTTPException(422, "筛选时间不是有效ISO时间或毫秒时间戳") from exc
    # 自定义日期以ISO文本存储；只在两侧都可解析为时间时进行时间比较。
    if (
        date_text
        and isinstance(actual, str)
        and isinstance(expected, str)
        and all(
            re.match(r"^\d{4}-\d{2}-\d{2}(?:$|[T ])", v) for v in [actual, expected]
        )
    ):
        try:
            return temporal(actual), temporal(expected)
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, "筛选日期文本不是有效ISO时间") from exc
    return actual, expected
