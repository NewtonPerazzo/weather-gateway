from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from typing import Annotated

from fastapi import Depends

# from app.exceptions.exceptions import (
#     InactiveUserException,
#     InvalidAccessTokenException,
# )
from app.models.authentication.users_model import UsersModel

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> UsersModel:
    pass
    # if credentials is None:
    #     raise InvalidAccessTokenException()

    # if credentials.scheme.lower() != "bearer":
    #     raise InvalidAccessTokenException()

    # payload = authentication_service.validate_access_token(
    #     access_token=credentials.credentials,
    # )

    # user = users_service.get_user(
    #     user_id=payload.sub,
    # )

    # if not user.is_active:
    #     raise InactiveUserException()

    # return user
