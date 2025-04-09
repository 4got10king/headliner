from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status

from app.api.router import router
from config.app import app_config
from database.db import database_accessor


def bind_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )


def bind_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def set_engine():
        await database_accessor.check_connection()

    @app.on_event("shutdown")
    async def close_engine():
        await database_accessor.stop()


def get_app() -> FastAPI:
    app = FastAPI(**app_config.swagger_conf)
    bind_events(app)
    bind_exceptions(app)
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods="*",
        allow_headers="*",
    )
    return app


app = get_app()
