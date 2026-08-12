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

    async def get_user(self, user_id: str, access_token: str):
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.url}/{user_id}", headers=headers)
            response.raise_for_status()
            return response.json()

    async def post_user(self, user: UsersRequestModel):
        user_data = UsersRequestModel.model_dump(user)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, json=user_data)
            response.raise_for_status()
            return response.json()

    async def update_user(self, user_id: str, user_request: UsersUpdateModel, access_token: str):
        user_request_data = UsersUpdateModel.model_dump(user_request)
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.patch(self.url, json=user_request_data, headers=headers)
            response.raise_for_status()
            return response.json()

    async def delete_user(self, user_id: str, access_token: str):
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.url}/{user_id}", headers=headers)
            response.raise_for_status()
            return response.json()

    async def change_user_activity(
        self,
        user_id: str,
        is_active: bool,
        access_token: str,
    ):
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.url}/{user_id}/activity",
                json={'is_active': is_active},
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    def get_url(self):
        return f'{self.__api_integrations.authentication_url}{USERS_URI}'