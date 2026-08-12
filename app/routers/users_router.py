from typing import Annotated

from fastapi import APIRouter, Depends

from app.authentication_dependency import get_current_user
from app.dependency import UsersServiceDependency
from app.models.authentication.users_model import (
    UserActivityModel,
    UsersModel,
    UsersRequestModel,
    UsersUpdateModel,
)


users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.get(
    "/me",
    response_model=UsersModel,
)
async def get_own_profile(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
) -> UsersModel:
    return current_user


@users_router.get(
    "/{user_id}",
    response_model=UsersModel
)
async def get_user(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    users_service: UsersServiceDependency,
):
    response = await users_service.get_user(user_id=current_user.id)
    return response


@users_router.post(
    "",
    response_model=UsersModel
)
async def post_user(
    user_request: UsersRequestModel,
    users_service: UsersServiceDependency,
):
    response = await users_service.post_user(user=user_request)
    return response


@users_router.patch(
    "",
    response_model=UsersModel
)
async def update_user(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    user_request: UsersUpdateModel,
    users_service: UsersServiceDependency,
):
    response = await users_service.update_user(
        user_id=current_user.id,
        user_request=user_request,
    )
    return response


@users_router.delete("/{user_id}")
async def delete_user(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    users_service: UsersServiceDependency,
):
    response = await users_service.delete_user(user_id=current_user.id)
    return response


@users_router.patch(
    "/{user_id}/activity",
    response_model=UsersModel
)
async def change_user_activity(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    activity: UserActivityModel,
    users_service: UsersServiceDependency,
):
    response = await users_service.change_user_activity(
        user_id=current_user.id,
        is_active=activity.is_active,
    )
    return response
