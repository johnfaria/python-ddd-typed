from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str


class CreateUserResponse(BaseModel):
    id: str
    name: str
    email: str


class UpdateUserRequest(BaseModel):
    name: str
    email: str


class UpdateUserResponse(BaseModel):
    id: str
    name: str
    email: str


class SigninUserRequest(BaseModel):
    email: str
    password: str


class SigninUserResponse(BaseModel):
    token: str


class ListUsersResponse(BaseModel):
    id: str
    name: str
    email: str
