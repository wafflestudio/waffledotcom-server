"""
TODO : 추후 배치잡이 많아지거나 부하가 심하다고 판단되면 pod를 분리한다.
"""

import asyncio

from schedule import Scheduler

from waffledotcom.src.batch.slack.main import main as slack_main
from waffledotcom.src.settings import settings


async def schedule_tasks():
    scheduler = Scheduler()
    if settings.is_dev:
        scheduler.every().day.at("00:00", "Asia/Seoul").do(slack_main)
    if settings.is_prod:
        scheduler.every().sunday.at("00:00", "Asia/Seoul").do(slack_main)
    while True:
        # 최소 주기를 60초로 설정
        await asyncio.sleep(10)
        scheduler.run_pending()
