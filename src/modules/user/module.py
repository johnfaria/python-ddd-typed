from fastapi import APIRouter, FastAPI

from modules.user.routes import user_router


class UserModule:
    router: APIRouter = user_router

    @classmethod
    def register(cls, app: FastAPI) -> None:
        app.include_router(cls.router)
