import aiohttp
from config import http_api


async def check_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/user/?user_id={user_id}") as resp:
            data  = await resp.json()
            if resp.status == 200 and len(data) > 0:
                return data
            else:
                return False
            

async def user_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/user/", data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            

async def code_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/code/", data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            
async def check_code_exists(code):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/code/?code={code}") as resp:
            if resp.status == 200:
                return True
            else:
                return False
    

async def patch_phone(user_id, phone):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{http_api}/user/?user_id={user_id}') as resp:
            data = await resp.json()
            id_user = [response['id'] for response in data]
            
            async with session.patch(f'{http_api}/user/{id_user[0]}/', \
                                     data={'phone_number2': phone}) as resp:
                if resp.status == 200:
                    return True
                else:
                    return False
                


async def regular_user_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/regular/", data={'user_id': data}) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            

async def check_user_roles(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/regular/?user__user_id={user_id}") as resp:
            data  = await resp.json()
            if resp.status == 200 and len(data) > 0:
                return data
            else:
                return False
            

async def delete_regular_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{http_api}/regular/?user__user_id={user_id}') as resp:
            data = await resp.json()
            id_user = [response['id'] for response in data]
            if id_user:
                async with session.delete(f'{http_api}/regular/{id_user[0]}/') as resp:
                    if resp.status == 204:
                        return True
                    else:
                        return False
                    

async def get_branches():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/branches/") as resp:
            data  = await resp.json()
            if resp.status == 200 and len(data) > 0:
                return data
            else:
                return False


async def get_regular_info(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/regular/?user__user_id={user_id}") as resp:
            data  = await resp.json()
            if resp.status == 200 and len(data) > 0:
                return data
            else:
                return False
            