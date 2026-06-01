from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "password123",
            }
        }

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    created_at: datetime

    class Config:
        populate_by_name = True
        by_alias = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T12:00:00",
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
