from bson import ObjectId
from datetime import datetime

from db import Database


def get_datetime_obj(date: str) -> datetime:
    return datetime.fromisoformat(date)


def get_query_string(query: dict):
    query_str = {}
    for key, value in query.items():
        if value:
            if key == '_id':
                query_str.update(
                    {key: {'$in': [ObjectId(id) for id in value.split('::')]}})
            elif key == 'join_date':
                value = value.split('::')
                if (len(value) == 1
                        or get_datetime_obj(value[0])
                        > get_datetime_obj(value[1])):
                    query_str.update(
                        {key: {'$eq': get_datetime_obj(value[0])}})
                else:
                    query_str.update(
                        {key: {'$gte': get_datetime_obj(value[0]),
                               '$lte': get_datetime_obj(value[1])}})
            elif key in ['age', 'salary']:
                value = [int(i) for i in value.split('::')]
                if len(value) == 1 or value[0] > value[1]:
                    query_str.update(
                        {key: {'$eq': value[0]}})
                else:
                    query_str.update(
                        {key: {'$gte': value[0], '$lte': value[1]}})
            else:
                query_str.update({key: {'$in': value.split('::')}})
    return query_str


class User():

    def __init__(self) -> None:
        self.db = Database()
        self.data = {}

    @ staticmethod
    def set_data(user: dict) -> dict:
        return {"_id": str(user["_id"]),
                "name": user['name'],
                "email": user['email'],
                "age": user['age'],
                "company": user['company'],
                "join_date": user['join_date'].isoformat(),
                "job_title": user['job_title'],
                "gender": user['gender'],
                "salary": user['salary']}

    async def add(self, user: dict):
        db_user = await self.db.user_collection.insert_one(user)
        if user := await self.db.user_collection.find_one(
                {"_id": db_user.inserted_id}):
            self.data = self.set_data(user)
            return True
        else:
            False

    async def delete(self) -> bool:
        if self.data['_id'] and await self.db.user_collection.find_one(
                {'_id': ObjectId(self.data['_id'])}):
            await self.db.user_collection.delete_one(
                {'_id': ObjectId(self.data['_id'])})
            self.data = {}
            return True
        return False

    @ staticmethod
    async def get_all() -> list:
        db = Database()
        users = []
        async for user in db.user_collection.find():
            users.append(User.set_data(user))
        return users

    @ staticmethod
    async def delete_all(users: 'list[dict]') -> 'list[bool]':
        db = Database()
        result = []
        for user in users:
            if await db.user_collection.find_one(
                    {'_id': ObjectId(user['_id'])}):
                await db.user_collection.delete_one(
                    {'_id': ObjectId(user['_id'])})
                result.append(True)
        return result

    @ staticmethod
    async def get_by_parameters(query: dict) -> 'list[dict]':
        db = Database()
        result = []
        async for user in db.user_collection.find(
                get_query_string(query)):
            result.append(User.set_data(user))

        return result
