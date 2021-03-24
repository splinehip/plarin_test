from unittest import IsolatedAsyncioTestCase

from services import create_all_users
from services.user import User


test_user1 = {
    "name": "Flynn Vang",
    "email": "turpis.non@Nunc.edu",
    "age": 69,
    "company": "Twitter",
    "join_date": "2003-12-28T18:18:10-08:00",
    "job_title": "janitor",
    "gender": "female",
    "salary": 9632
}

test_user2 = {
    "name": "Cedric Page",
    "email": "a.facilisis.non@cursus.com",
    "age": 63,
    "company": "Yandex",
    "join_date": "2001-06-10T19:08:52-07:00",
    "job_title": "janitor",
    "gender": "male",
    "salary": 9688
}


class Database_simple_tests(IsolatedAsyncioTestCase):
    async def test_01_create_user(self):
        user = User()
        await user.add(test_user1)
        self.assertEqual(user.data, user.set_data(test_user1))

    async def test_02_get_all(self):
        users = await User.get_all()
        self.assertTrue(users)

    async def test_03_delete_user(self):
        user = User()
        await user.add(test_user2)
        self.assertEqual(user.data, user.set_data(test_user2))
        self.assertTrue(await user.delete())

    async def test_04_delete_all(self):
        users = await User.get_all()
        self.assertFalse(False in await User.delete_all(users))


class Load_data_simple_test(IsolatedAsyncioTestCase):
    async def test_01_create_all(self):
        await create_all_users()
        self.assertTrue(await User.get_all())
