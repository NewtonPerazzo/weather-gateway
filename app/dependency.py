from typing import Annotated

from fastapi import Depends

from app.integrations.APIIntegration import APIIntegration
from app.services.authentication_service import AuthenticationService
from app.services.users_service import UsersService
from app.services.weather_service import WeatherService
from config.settings import Settings, get_settings


def get_api_integration(
    settings: Annotated[Settings, Depends(get_settings)],
) -> APIIntegration:
    return APIIntegration(
        authentication_url=settings.auth_service_url,
        weather_url=settings.weather_service_url,
        request_timeout_seconds=settings.request_timeout_seconds,
    )


APIIntegrationDependency = Annotated[
    APIIntegration,
    Depends(get_api_integration),
]


def get_authentication_service(
    api_integration: APIIntegrationDependency,
) -> AuthenticationService:
    return AuthenticationService(api_integrations=api_integration)


def get_users_service(
    api_integration: APIIntegrationDependency,
) -> UsersService:
    return UsersService(api_integrations=api_integration)


def get_weather_service(
    api_integration: APIIntegrationDependency,
) -> WeatherService:
    return WeatherService(api_integrations=api_integration)


AuthenticationServiceDependency = Annotated[
    AuthenticationService,
    Depends(get_authentication_service),
]

UsersServiceDependency = Annotated[
    UsersService,
    Depends(get_users_service),
]

WeatherServiceDependency = Annotated[
    WeatherService,
    Depends(get_weather_service),
]
