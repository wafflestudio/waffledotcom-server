from fastapi import APIRouter

from waffledotcom.src.batch.scheduler import scheduler

from .schemas import JobDto, ScheduleResponse

v1_router = APIRouter(prefix="/v1/batch", tags=["batch"])


@v1_router.get("/schedule", response_model_exclude_none=True)
def get_schedule(
    tag: str | None = None,
) -> ScheduleResponse:
    job_dtos = [
        JobDto(
            name=getattr(job.job_func, "__qualname__", "Unknown"),
            interval=job.interval,
            unit=job.unit,  # type: ignore
            start_day=job.start_day,
            at_time=job.at_time,
            next_run=job.next_run,
            last_run=job.last_run,
        )
        for job in scheduler.get_jobs(tag)
    ]
    return ScheduleResponse(jobs=job_dtos)
