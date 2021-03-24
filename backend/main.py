#!venv/bin/python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from services import create_all_users
from services.user import User


api = FastAPI()


@api.get('/')
async def index():
    return 'Documentation available on /docs  or /redoc urls.'


@api.get('/users')
async def get_all():
    await create_all_users()
    resp = await User.get_all()
    return resp
