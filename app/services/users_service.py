import httpx

from app.integrations.APIIntegration import APIIntegration
from app.models.authentication.users_model import UsersRequestModel, UsersUpdateModel

USERS_URI = '/users'

class UsersService():
    def __init__(
        self,
        api_integrations: APIIntegration,
    ):
        self.__api_integrations = api_integrations
        self.url = self.get_url()

    async def get_user(self, user_id: str):
        response = httpx.get(self.url, params={'user_id': user_id})

        return response

    async def post_user(self, user: UsersRequestModel):
        user_data = UsersRequestModel.model_dump(user)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, json=user_data)
            response.raise_for_status()
            return response.json()

    async def update_user(self, user_id: str, user_request: UsersUpdateModel):
        user_request_data = UsersUpdateModel.model_dump(user_request)

        async with httpx.AsyncClient() as client:
            response = await client.patch(self.url, json=user_request_data, params={ 'user_id': user_id })
            response.raise_for_status()
            return response.json()

    async def delete_user(self, user_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.delete(self.url, params={ 'user_id': user_id })
            response.raise_for_status()
            return response.json()

    async def change_user_activity(
        self,
        user_id: str,
        is_active: bool
    ):
        async with httpx.AsyncClient() as client:
            response = await client.patch(self.url, params={ 'user_id': user_id }, json={ 'is_active': is_active })
            response.raise_for_status()
            return response.json()

    def get_url(self):
        return f'{self.__api_integrations.authentication_url}{USERS_URI}'