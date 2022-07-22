"""Главный машрутизатор в котором будут хранится все маршруты"""

from fastapi import APIRouter

from apis.version1 import route_users, route_jobs, route_login, route_general_pages

api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router, prefix='', tags=['general_pages'])
api_router.include_router(route_users.router, prefix='/users', tags=['users'])
api_router.include_router(route_jobs.router, prefix='/jobs', tags=['jobs'])
api_router.include_router(route_login.router, prefix='/login', tags=['login'])
