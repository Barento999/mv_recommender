from app.database import get_database
from app.models.user import User
from app.utils.security import hash_password, verify_password
from bson import ObjectId
from typing import Optional

async def create_user(name: str, email: str, password: str) -> User:
    db = get_database()
    existing_user = await db.users.find_one({"email": email})
    if existing_user:
        raise ValueError("Email already registered")

    user = User(name=name, email=email, password=hash_password(password))
    result = await db.users.insert_one(user.to_dict())
    user._id = result.inserted_id
    return user

async def get_user_by_email(email: str) -> Optional[User]:
    db = get_database()
    user_data = await db.users.find_one({"email": email})
    if user_data:
        return User.from_dict(user_data)
    return None

async def get_user_by_id(user_id: str) -> Optional[User]:
    db = get_database()
    try:
        user_data = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User.from_dict(user_data)
    except Exception:
        pass
    return None

async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
