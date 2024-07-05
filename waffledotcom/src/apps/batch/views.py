from fastapi import APIRouter

from waffledotcom.src.batch.scheduler import get_job_name, scheduler

from .schemas import ForceRunResponse, ForceRunResult, JobDto, ScheduleResponse

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


@v1_router.post("/force-run", response_model_exclude_none=True)
def force_run_job(
    name: str | None = None,
    tag: str | None = None,
) -> ForceRunResponse:
    if not ((name is None) ^ (tag is None)):
        raise ValueError("Either name or tag should be provided")
    jobs = scheduler.get_jobs(tag)
    if name is not None:
        jobs = [job for job in jobs if get_job_name(job) == name]

    results: list[ForceRunResult] = []
    for job in jobs:
        try:
            job.run()
            results.append(
                ForceRunResult(
                    name=get_job_name(job),
                    tags=list(map(str, job.tags)),
                    success=True,
                )
            )
        except Exception as e:
            results.append(
                ForceRunResult(
                    name=get_job_name(job),
                    tags=list(map(str, job.tags)),
                    success=False,
                    reason=str(e),
                )
            )
    return ForceRunResponse(results=results)
