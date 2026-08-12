import httpx

from app.integrations.APIIntegration import APIIntegration
from app.models.authentication.authentication_model import LoginRequestModel, RefreshTokenRequestModel, ResetPasswordBodyModel, TokenResponseModel

LOGIN_URI = '/login'
REFRESH_URI = '/refresh'
LOGOUT_URI = '/logout'
RESET_PASSWORD_URI = '/reset-password'

class AuthenticationService():
    def __init__(
        self,
        api_integrations: APIIntegration,
    ) -> None:
        self.__api_integrations = api_integrations

    async def login(self, login_data: LoginRequestModel) -> TokenResponseModel:
        url = self.get_url(LOGIN_URI)
        login_request_data = LoginRequestModel.model_dump(login_data)   

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=login_request_data)
            response.raise_for_status()
            return response.json()

    async def refresh(self, refresh_data: RefreshTokenRequestModel) -> TokenResponseModel:
        url = self.get_url(REFRESH_URI)
        refresh_request_data = RefreshTokenRequestModel.model_dump(refresh_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=refresh_request_data)
            response.raise_for_status()
            return response.json()

    async def reset_password(self, reset_password_data: ResetPasswordBodyModel) -> None:
        url = self.get_url(RESET_PASSWORD_URI)
        reset_request_data = ResetPasswordBodyModel.model_dump(reset_password_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=reset_request_data)
            response.raise_for_status()
    
    async def logout(self, refresh_data: RefreshTokenRequestModel) -> None:
        url = self.get_url(LOGOUT_URI)
        refresh_request_data = RefreshTokenRequestModel.model_dump(refresh_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=refresh_request_data)
            response.raise_for_status()

    def get_url(self, uri: str) -> str:
        return f'{self.__api_integrations.authentication_url}/authentication{uri}'