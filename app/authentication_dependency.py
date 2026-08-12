from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.dependency import APIIntegrationDependency
from app.models.authentication.users_model import UsersModel

bearer_scheme = HTTPBearer(auto_error=False)

async def get_access_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials


async def get_current_user(
    access_token: Annotated[str, Depends(get_access_token)],
    api_integration: APIIntegrationDependency,
) -> UsersModel:
    url = f"{api_integration.authentication_url}/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    return UsersModel.model_validate(response.json())
