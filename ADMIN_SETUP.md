# 🔐 Admin User Setup Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)

When the backend starts for the first time, it automatically creates a default admin account:

**Default Admin Credentials:**
- Email: `admin@movierego.com`
- Password: Not set initially (use Option 2 or 3 to set)

### Option 2: Using Setup Script (After Starting Backend)

**Make sure MongoDB is running first!** Then run:

```bash
cd backend
./venv/bin/python3 setup_admin.py
```

This will:
1. Prompt for admin email (or use default)
2. Prompt for password (6+ characters)
3. Create/update admin user in database
4. Display confirmation

**Example:**
```
🔐 ADMIN USER SETUP
====================

Admin email (default: admin@movierego.com): admin@movierego.com
Admin password (6+ characters): ••••••••
Confirm password: ••••••••

✅ Admin user 'admin@movierego.com' created

📌 LOGIN CREDENTIALS:
   Email: admin@movierego.com
   Password: (the one you just entered)
```

### Option 3: Registration via Web UI

1. Go to the application frontend
2. Click **Register**
3. Create account with email: `admin@movierego.com`
4. Manually promote user to admin via MongoDB (see below)

### Option 4: Manual Database Update

Connect to MongoDB and update the user:

```javascript
db.users.updateOne(
  { email: "admin@movierego.com" },
  {
    $set: {
      role: "admin",
      permissions: [
        "read_movies",
        "rate_movies",
        "add_favorites",
        "write_reviews",
        "view_recommendations",
        "manage_wishlist",
        "view_watch_history",
        "view_preferences",
        "delete_reviews",
        "edit_movies",
        "view_analytics",
        "moderate_reviews",
        "manage_users",
        "manage_roles",
        "view_system_analytics",
        "manage_movies",
        "manage_content"
      ]
    }
  }
)
```

## Full Setup Flow

**Terminal 1 - Start Backend:**
```bash
cd backend
./venv/bin/python -m uvicorn app.main:app --reload
```

**Terminal 2 - Set Admin Password:**
```bash
cd backend
./venv/bin/python3 setup_admin.py
# Follow prompts to set admin email and password
```

**Terminal 3 - Start Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:**
1. Go to http://localhost:5173
2. Login with admin credentials you just set
3. You should see "ADMIN" badge in navbar and have access to admin features

## Admin Capabilities

Once logged in as admin, you'll have access to:

### 👥 User Management (`/admin/users`)
- List all users
- View user details
- Update user roles (user → moderator → admin)
- Delete users
- View role permissions

### 📊 Analytics (`/analytics`)
- System-wide analytics dashboard
- Rating distribution
- Genre analytics
- User engagement metrics
- Top movies by various metrics
- Timeline statistics

### 🛡️ Admin Dashboard (`/admin-dashboard`)
- System status
- Movie statistics
- User statistics
- Top-rated movies

### Other Admin Features
- Full moderation capabilities
- System analytics access
- Content management

## Role Hierarchy

The system has 3 roles with increasing permissions:

1. **User** (8 permissions)
   - Read movies, rate, add favorites, write reviews, etc.

2. **Moderator** (12 permissions)
   - All user permissions + delete reviews, edit movies, view analytics, moderate reviews

3. **Admin** (17 permissions)
   - All permissions + manage users, manage roles, manage movies, manage content

## Testing RBAC

### To Test RBAC:

1. Create multiple test accounts:
   - One regular user
   - One moderator
   - One admin

2. Log in as each role and verify:
   - User: Cannot see "More" dropdown admin links
   - Moderator: Can see Analytics and Moderation links  
   - Admin: Can see all admin links including User Management

3. Verify API protection:
   - Try accessing `/admin/users` without admin role → 403 Forbidden
   - Try accessing `/analytics` without moderator role → 403 Forbidden

## Troubleshooting

### "Connection refused" when running setup_admin.py
- Make sure MongoDB is running
- Make sure backend is started (or at least MongoDB is accessible)
- Check MongoDB is on localhost:27017

### Admin not appearing in Management Panel
- Verify role is set to "admin" in database
- Check that permissions array contains admin permissions
- Reload the page and re-login

### Can't set password
- Ensure MongoDB is running and accessible
- Check that the user exists in database
- Run setup_admin.py again to update password

### Admin page redirects to home
- Check browser console for errors
- Verify JWT token contains role field
- Check backend logs for authentication errors

## Security Notes

- Keep admin credentials secure
- Change default admin password immediately after setup
- Create additional admin accounts only when necessary
- Use moderator role for content moderation (more restricted)
- Monitor admin activity in the system logs

## Password Requirements

- Minimum 6 characters
- Must match confirmation
- Stored as SHA256 hash in database
- Used for authentication only
