from typing import Any

from fastapi import APIRouter as FastAPIRouter


def _get_alternative_path(path: str) -> str:
    return path[:-1] if path.endswith("/") else f"{path}/"


class APIRouter(FastAPIRouter):
    def add_api_route(self, path: str, *args: Any, include_in_schema: bool = True, **kwargs: Any) -> None:
        super().add_api_route(_get_alternative_path(path), *args, include_in_schema=False, **kwargs)
        super().add_api_route(path, *args, include_in_schema=include_in_schema, **kwargs)
