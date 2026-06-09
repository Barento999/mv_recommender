#!/usr/bin/env python3
"""
Setup user with any role (admin, moderator, user)
Run this script to create or update a user with any role
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.security import hash_password
from app.middleware.rbac import get_permission_list, ROLES
import getpass

# Get MongoDB URL from environment
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "movierego")


async def setup_user():
    """Create or update user with specified role."""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print("\n" + "="*70)
        print("👤 USER SETUP")
        print(f"📍 Connecting to: {MONGO_URL[:50]}...")
        print("="*70)
        
        # Test connection
        try:
            await db.command('ping')
            print("✅ Connected to MongoDB Atlas\n")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {str(e)}")
            client.close()
            return False
        
        # Get role selection
        print("Available roles:")
        for i, role_name in enumerate(ROLES.keys(), 1):
            print(f"  {i}. {role_name.upper()}")
        
        role_choice = input("\nSelect role (1-3, default=3 for user): ").strip()
        role_names = list(ROLES.keys())
        
        try:
            role_index = int(role_choice) - 1 if role_choice else 0
            if role_index < 0 or role_index >= len(role_names):
                role_index = 0
        except:
            role_index = 0
        
        selected_role = role_names[role_index]
        
        # Get user credentials
        email = input(f"\nEmail (default: {selected_role}@movierego.com): ").strip()
        if not email:
            email = f"{selected_role}@movierego.com"
        
        password = getpass.getpass("Password (6+ characters): ")
        if not password or len(password) < 6:
            print("❌ Password must be at least 6 characters")
            client.close()
            return False
        
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("❌ Passwords don't match")
            client.close()
            return False
        
        # Hash password using Argon2 (same as login system)
        password_hash = hash_password(password)
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": email})
        
        if existing_user:
            # Update existing user
            result = await db.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "password": password_hash,
                        "role": selected_role,
                        "permissions": get_permission_list(selected_role),
                    }
                }
            )
            if result.modified_count > 0:
                print(f"\n✅ User '{email}' updated to {selected_role.upper()}")
            else:
                print(f"\n✅ User '{email}' already exists")
        else:
            # Create new user
            from datetime import datetime
            from bson import ObjectId
            
            new_user = {
                "_id": ObjectId(),
                "name": selected_role.capitalize(),
                "email": email,
                "password": password_hash,
                "role": selected_role,
                "permissions": get_permission_list(selected_role),
                "created_at": datetime.utcnow(),
            }
            
            result = await db.users.insert_one(new_user)
            print(f"\n✅ {selected_role.upper()} user '{email}' created")
        
        print("\n📌 LOGIN CREDENTIALS:")
        print(f"   Email: {email}")
        print(f"   Password: (the one you just entered)")
        print(f"   Role: {selected_role.upper()}")
        print(f"   Permissions: {len(get_permission_list(selected_role))} permissions")
        print("\n" + "="*70 + "\n")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(setup_user())
    sys.exit(0 if result else 1)
