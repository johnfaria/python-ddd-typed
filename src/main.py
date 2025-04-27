from core.infra.database.database_connect import close_database, initialize_database
from fastapi import FastAPI
from modules.user.module import UserModule


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_event_handler("startup", initialize_database)
    app.add_event_handler("shutdown", close_database)

    UserModule.register(app)

    return app


app = create_app()
