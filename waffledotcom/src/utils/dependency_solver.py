import inspect
from contextlib import AsyncExitStack
from typing import Callable

from fastapi import Request
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant, solve_dependencies
from pydantic import ValidationError


class DependencySolver:
    async def solve_command(self, request: Request, dependant: Dependant):
        values, errors, _1, _2, _3 = await solve_dependencies(
            request=request, dependant=dependant
        )
        if errors:
            raise ValidationError(errors, None)  # type: ignore
        if inspect.iscoroutinefunction(dependant.call):
            result = await dependant.call(**values)
        else:
            result = dependant.call(**values)  # type: ignore

        return result

    async def run(self, command: Callable):
        async with AsyncExitStack() as cm:
            request = Request(
                {
                    "type": "http",
                    "headers": [],
                    "query_string": "",
                    "fastapi_astack": cm,
                }
            )

            dependant = get_dependant(path=f"command:{command.__name__}", call=command)

            return await self.solve_command(request, dependant)


solver = DependencySolver()
