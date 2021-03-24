__all__ = ['user']

import json

from services.user import User


async def create_all_users():
    with open('../employees.json') as json_file:
        data = json.load(json_file)

    if not await User.get_all():
        for item in data:
            user = User()
            await user.add(item)
