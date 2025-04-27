from fastapi import FastAPI
from src.main import app as main_app

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     # Perform startup actions here if needed
#     pass


# @app.on_event("shutdown")
# async def shutdown_event():
#     # Perform shutdown actions here if needed
#     pass


app.mount("/", main_app)
