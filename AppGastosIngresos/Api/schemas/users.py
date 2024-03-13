from pydantic import BaseModel, EmailStr
from enum import Enum as PydanticEnum
from datetime import datetime

class UserRole(str, PydanticEnum):
    admin ="admin"
    user ="user"


class UserBase(BaseModel):
    full_name: str
    mail: EmailStr

class UserCreate(UserBase):
    passhash: str
    user_status: bool=True

class UserCreateAdmin(UserBase):
    passhash: str
    user_role: UserRole
    user_status: bool=True

class UserRead(UserBase):
    user_id: str
    created_at: datetime
    user_role: UserRole
    updated_at: datetime
    user_status: bool

class UserUpdateAdmin(UserBase):
    user_id: str
    passhash: str
    user_status: bool=True
    user_role: UserRole

class UserUpdate(UserBase):
    user_id: str
    passhash: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

    #Cuando orm_mode esta habilitado,permite la conversion directa de objetos sqlalchemy a modelos pydantic sin nececidad de definir explicitamente todos los campos
    