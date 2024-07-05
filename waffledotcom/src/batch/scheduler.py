"""
TODO : 추후 배치잡이 많아지거나 부하가 심하다고 판단되면 pod를 분리한다.
"""

import asyncio
from collections.abc import Callable
from functools import wraps

from loguru import logger
from schedule import Scheduler

from waffledotcom.src.batch.slack.main import create_users_from_slack
from waffledotcom.src.settings import settings
from waffledotcom.src.utils.dependency_solver import solver


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


def setup_job_schedule(scheduler: Scheduler):
    if settings.is_dev:
        scheduler.every().saturday.at("00:00", "Asia/Seoul").do(
            job_wrapper(create_users_from_slack)
        )
    if settings.is_prod:
        scheduler.every().sunday.at("00:00", "Asia/Seoul").do(
            job_wrapper(create_users_from_slack)
        )

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
    scheduler = Scheduler()
    setup_job_schedule(scheduler)
    while True:
        # 최소 주기를 60초로 설정
        await asyncio.sleep(60)
        scheduler.run_pending()
