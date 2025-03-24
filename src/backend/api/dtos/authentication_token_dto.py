from pydantic import BaseModel


class AuthenticationTokenDto(BaseModel):
    access_token: str
    token_type: str
