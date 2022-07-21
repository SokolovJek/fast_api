from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings
from apis.general_pages.route_homepage import general_pages_router



def include_router(my_app):
    my_app.include_router(general_pages_router)


def configure_static(my_app):
    """Сообщаем FastAPI что статика хранится в директории 'static' """
    # name='static' для того чтоб Jinja2 мог найти его
    my_app.mount('/static', StaticFiles(directory='static'), name='static')


def start_applications():
    my_app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(my_app)
    configure_static(my_app)
    return my_app


app = start_applications()
