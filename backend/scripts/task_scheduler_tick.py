"""独立到期检查：只入队一次，实际 Agent 派发由 ATS 后端生命周期负责。"""

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.logger import logger
from database import SessionLocal
from services.task_scheduler import enqueue_due


async def main():
    try:
        with SessionLocal() as db:
            count = await enqueue_due(db)
        logger.info("独立到期检查完成，新建触发次数={}", count)
    except Exception:
        logger.exception("独立到期检查失败")
        raise


if __name__ == "__main__":
    asyncio.run(main())
