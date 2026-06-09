#!/usr/bin/env python3
"""
Setup admin user with password
Run this script to create or update the admin user password
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
import getpass
import hashlib

# Get MongoDB URL from environment
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "movierego")


def hash_password(password: str) -> str:
    """Simple password hashing using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


async def setup_admin():
    """Create or update admin user with password."""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print("\n" + "="*70)
        print("🔐 ADMIN USER SETUP")
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
        
        # Get admin credentials
        email = input("Admin email (default: admin@movierego.com): ").strip()
        if not email:
            email = "admin@movierego.com"
        
        password = getpass.getpass("Admin password (6+ characters): ")
        if not password or len(password) < 6:
            print("❌ Password must be at least 6 characters")
            client.close()
            return False
        
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("❌ Passwords don't match")
            client.close()
            return False
        
        # Hash password
        password_hash = hash_password(password)
        
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
                    }
                }
            )
            if result.modified_count > 0:
                print(f"\n✅ Admin user '{email}' password updated")
            else:
                print(f"\n✅ Admin user '{email}' already has role set")
        else:
            # Create new admin
            from datetime import datetime
            from bson import ObjectId
            from app.middleware.rbac import get_permission_list
            
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
            print(f"\n✅ Admin user '{email}' created")
        
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
