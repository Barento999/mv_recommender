#!/usr/bin/env python3
"""
Setup admin user with password
Run this script to create or update the admin user password
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import getpass

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.middleware.rbac import get_permission_list

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "movierego"


async def setup_admin():
    """Create or update admin user with password."""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print("\n" + "="*70)
        print("🔐 ADMIN USER SETUP")
        print("="*70)
        
        # Get admin credentials
        email = input("\nAdmin email (default: admin@movierego.com): ").strip()
        if not email:
            email = "admin@movierego.com"
        
        password = getpass.getpass("\nAdmin password (will be hidden): ").strip()
        if not password or len(password) < 6:
            print("❌ Password must be at least 6 characters")
            return False
        
        password_confirm = getpass.getpass("Confirm password: ").strip()
        if password != password_confirm:
            print("❌ Passwords don't match")
            return False
        
        # Hash password
        password_hash = pwd_context.hash(password)
        
        # Check if admin exists
        existing_admin = await db.users.find_one({"email": email})
        
        if existing_admin:
            # Update existing admin
            result = await db.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "password_hash": password_hash,
                        "role": "admin",
                        "permissions": get_permission_list("admin"),
                    }
                }
            )
            if result.modified_count > 0:
                print(f"\n✅ Admin user '{email}' password updated")
            else:
                print(f"\n✅ Admin user '{email}' already exists")
        else:
            # Create new admin
            from datetime import datetime
            from bson import ObjectId
            
            admin_user = {
                "_id": ObjectId(),
                "name": "Admin User",
                "email": email,
                "password_hash": password_hash,
                "role": "admin",
                "permissions": get_permission_list("admin"),
                "created_at": datetime.utcnow(),
            }
            
            result = await db.users.insert_one(admin_user)
            print(f"\n✅ Admin user '{email}' created (ID: {result.inserted_id})")
        
        print("\n📌 LOGIN CREDENTIALS:")
        print(f"   Email: {email}")
        print(f"   Password: (the one you just entered)")
        print("\n" + "="*70 + "\n")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(setup_admin())
    sys.exit(0 if result else 1)
