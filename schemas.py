# schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# --------- USER SCHEMAS ---------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    # password dibatasi 8–72 karakter supaya aman untuk bcrypt
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        # pengganti orm_mode di Pydantic v2
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# --------- CONTACT SCHEMAS ---------

class ContactBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    category: Optional[str] = None  # Keluarga/Teman/Kerja/dll


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    category: Optional[str] = None


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True
