__all__ = ['user']

import json

from services.user import User, get_datetime_obj


async def create_all_users():
    with open('../employees.json') as json_file:
        data = json.load(json_file)

    if not await User.get_all():
        for item in data:
            item['join_date'] = get_datetime_obj(item['join_date'])
            user = User()
            await user.add(item)
