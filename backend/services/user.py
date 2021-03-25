from bson import ObjectId

from db import Database


class User():

    def __init__(self) -> None:
        self.db = Database()
        self.data = {}

    @staticmethod
    def set_data(user: dict) -> dict:
        return {"_id": str(user["_id"]),
                "name": user['name'],
                "email": user['email'],
                "age": user['age'],
                "company": user['company'],
                "join_date": user['join_date'],
                "job_title": user['job_title'],
                "gender": user['gender'],
                "salary": user['salary']}

    async def add(self, user: dict):
        db_user = await self.db.user_collection.insert_one(user)
        user = await self.db.user_collection.find_one(
            {"_id": db_user.inserted_id})
        self.data = self.set_data(user)

    async def delete(self) -> bool:
        if self.data['_id'] and await self.db.user_collection.find_one(
                {'_id': ObjectId(self.data['_id'])}):
            await self.db.user_collection.delete_one(
                {'_id': ObjectId(self.data['_id'])})
            self.data = {}
            return True
        return False

    @staticmethod
    async def get_all() -> list:
        db = Database()
        users = []
        async for user in db.user_collection.find():
            users.append(User.set_data(user))
        return users

    @staticmethod
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

    @staticmethod
    async def get_by_parameters(query: dict) -> 'list[dict]':
        db = Database()
        result = []
        for key, value in query.items():
            if value:
                async for user in db.user_collection.find(
                        {key: {'$in': value.split(';')}}):
                    result.append(User.set_data(user))

        return result
