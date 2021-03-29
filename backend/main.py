#!venv/bin/python3
# -*- coding: utf-8 -*-

import uvicorn

from typing import List
from fastapi import FastAPI

from services import create_all_users
from services.user import User
from db import schema


api = FastAPI()


@api.on_event('startup')
async def load_users_from_file():
    await create_all_users()


@api.get('/')
async def index():
    return 'Documentation available on /docs  or /redoc urls.'


@api.get('/users', response_model=List[schema.User])
async def get_all_or_by_parameters(_id: str = None,
                                   name: str = None,
                                   email: str = None,
                                   age: str = None,
                                   company: str = None,
                                   join_date: str = None,
                                   job_title: str = None,
                                   gender: str = None,
                                   salary: str = None):
    query = {'_id': _id,
             'name': name,
             'email': email,
             'age': age,
             'company': company,
             'join_date': join_date,
             'job_title': job_title,
             'gender': gender,
             'salary': salary}

    for value in query.items():
        if value:
            resp = await User.get_by_parameters(query)
            return resp

    resp = await User.get_all()
    return resp


if __name__ == '__main__':
    uvicorn.run(api, host='localhost', port=8000)
