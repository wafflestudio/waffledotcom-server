"""
TODO : 추후 배치잡이 많아지거나 부하가 심하다고 판단되면 pod를 분리한다.
"""

import asyncio
from collections.abc import Callable
from datetime import datetime
from functools import wraps

from loguru import logger
from schedule import Scheduler

from waffledotcom.src.batch.slack.main import create_users_from_slack
from waffledotcom.src.settings import settings
from waffledotcom.src.utils.dependency_solver import solver

scheduler = Scheduler()


def job_wrapper(job_func: Callable):
    job_name = job_func.__qualname__

    async def run_with_dependencies():
        try:
            logger.info(f"Start scheduled job [{job_name}]")
            await solver.run(job_func)
            logger.info(f"End scheduled job [{job_name}]")
        except Exception as e:
            logger.opt(exception=e).error(f"Error occurred in job [{job_name}]")

    @wraps(job_func)
    def run_in_loop():
        try:
            asyncio.create_task(run_with_dependencies())
        except RuntimeError:
            asyncio.run(run_with_dependencies())

    return run_in_loop


def setup_job_schedule():
    if settings.is_dev:
        scheduler.every().saturday.at("12:00", "Asia/Seoul").do(
            job_wrapper(create_users_from_slack)
        ).tag("slack")
    if settings.is_prod:
        scheduler.every().sunday.at("00:00", "Asia/Seoul").do(
            job_wrapper(create_users_from_slack)
        ).tag("slack")

    for job in scheduler.get_jobs():
        job_name = getattr(job.job_func, "__qualname__", "Unknown")

        logger.info(
            "Job [{job_name}] is scheduled every {interval} {unit}. Next run at"
            " {next_run}",
            job_name=job_name,
            interval=job.interval,
            unit=job.unit,
            next_run=job.next_run,
        )


async def run_scheduling_service():
    setup_job_schedule()
    while True:
        next_run = scheduler.get_next_run()

        # 앞으로 더 이상 스케줄된 작업이 없다면 스케줄링 서비스를 종료한다.
        if next_run is None:
            logger.info("No jobs scheduled. Exiting scheduling service")
            break

        # 다음 작업이 실행되기까지 대기해야할 시간을 계산한다.
        now = datetime.now()
        delay = max((next_run - now).total_seconds(), 1)
        await asyncio.sleep(delay)
        scheduler.run_pending()
