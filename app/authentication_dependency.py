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

async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    api_integration: APIIntegrationDependency,
) -> UsersModel:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    url = f"{api_integration.authentication_url}/users/me"
    headers = {
        "Authorization": f"Bearer {credentials.credentials}",
    }

    response = httpx.get(url, headers=headers)

    return UsersModel.model_validate(response.json())
