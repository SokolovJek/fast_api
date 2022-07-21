from fastapi import FastAPI
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router


def include_router(my_app):
    my_app.include_router(general_pages_router)


def start_applications():
    my_app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(my_app)
    return my_app


app = start_applications()

# @app.get("/")
# def hello_api():
#     return {"msg": "Hello API"}
