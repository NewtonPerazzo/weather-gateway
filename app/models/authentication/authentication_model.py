from pydantic import BaseModel, ConfigDict

class LoginRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str

class RefreshTokenRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str

class ResetPasswordBodyModel(BaseModel):
    refresh_token: str
    new_password: str

class TokenResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_expires_in: int