from datetime import datetime, time

from pydantic import BaseModel


class JobDto(BaseModel):
    name: str
    interval: int
    unit: str
    start_day: str | None
    at_time: time | None
    next_run: datetime | None
    last_run: datetime | None


class ScheduleResponse(BaseModel):
    jobs: list[JobDto]


class ForceRunResult(BaseModel):
    name: str
    tags: list[str]
    success: bool
    reason: str | None = None


class ForceRunResponse(BaseModel):
    results: list[ForceRunResult]
