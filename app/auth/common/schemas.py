from pydentic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthenticatedUser(BaseModel):
    id: str
    email: str
    role: str    