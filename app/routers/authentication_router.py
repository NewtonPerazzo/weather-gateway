from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependency import AuthenticationServiceDependency
from app.models.authentication.authentication_model import (
    LoginRequestModel,
    RefreshTokenRequestModel,
    ResetPasswordBodyModel,
    TokenResponseModel,
)
from app.models.authentication.users_model import UsersModel
from app.authentication_dependency import get_current_user


authentication_router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)

@authentication_router.post("/login", response_model=TokenResponseModel)
async def login(
    login_data: LoginRequestModel,
    authentication_service: AuthenticationServiceDependency,
) -> TokenResponseModel:
    return await authentication_service.login(login_data=login_data)


@authentication_router.post("/refresh", response_model=TokenResponseModel)
async def refresh(
    refresh_data: RefreshTokenRequestModel,
    authentication_service: AuthenticationServiceDependency
) -> TokenResponseModel:
    return await authentication_service.refresh(refresh_data=refresh_data)


@authentication_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    refresh_data: RefreshTokenRequestModel,
    authentication_service: AuthenticationServiceDependency,
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
) -> Response:
    await authentication_service.logout(refresh_data=refresh_data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@authentication_router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def reset_password(
    reset_password_data: ResetPasswordBodyModel,
    authentication_service: AuthenticationServiceDependency,
) -> Response:
    await authentication_service.reset_password(
        reset_password_data=reset_password_data,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
