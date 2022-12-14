from fastapi import FastAPI

from fastapi_example.router import router 


def create_application() -> FastAPI:

    app = FastAPI()
    app.include_router(router)

    return app
