from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    user_id: int = Field(alias="UserId", ge=1, examples=123)


class UserBody(BaseModel):
    """Входная модель пользователей"""

    username: str
    first_name: str = Field(serialization_alias="firstName")
    last_name: str = Field(serialization_alias="lastName")
    email: str
    phone: str


class UserResponse(BaseModel):
    """Входная модель пользователей"""

    username: str
    first_name: str = Field(serialization_alias="firstName")
    last_name: str = Field(serialization_alias="lastName")
    email: str
    phone: str


class UpdateUser(BaseModel):
    first_name: str = Field(serialization_alias="firstName")
    last_name: str = Field(serialization_alias="lastName")
    email: str
    phone: str
