from pydantic import BaseModel

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str

class GetUserResponse(BaseModel):
    id: str
    name: str
    

class GetProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    
class AuthResponse(BaseModel):
    access_token: str