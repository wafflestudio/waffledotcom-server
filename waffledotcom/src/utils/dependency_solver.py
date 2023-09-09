import argparse
from contextlib import AsyncExitStack
import inspect
from typing import Callable

from fastapi import Request
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies
from pydantic import ValidationError


class DependencySolver:
    """
    A utility class to solve FastAPI dependencies in an ad-hoc manner.
    """

    def __init__(self, name: str | None = None, namespace=None):
        self.name = name or self.__class__.__name__
        self.parser = self.make_parser()
        self.args = self.parser.parse_args(namespace=namespace)

    # override to add command-line arguments
    def make_parser(self) -> argparse.ArgumentParser:
        return argparse.ArgumentParser(prog=self.name)

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

            dependant = get_dependant(path=f"command:{self.name}", call=command)

            return await self.solve_command(request, dependant)
