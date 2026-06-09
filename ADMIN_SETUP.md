# 🔐 Admin User Setup Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)

When the backend starts for the first time, it automatically creates a default admin account:

**Default Admin Credentials:**
- Email: `admin@movierego.com`
- Password: Not set initially (use Option 2 or 3 to set)

### Option 2: Using Setup Script

Run the interactive admin setup script:

```bash
cd backend
python setup_admin.py
```

This will:
1. Prompt for admin email (or use default)
2. Prompt for password
3. Create/update admin user in database
4. Display confirmation

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

## Testing

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

### Admin not appearing in Management Panel
- Verify role is set to "admin" in database
- Check that permissions array contains admin permissions
- Reload the page and re-login

### Can't set password
- Ensure MongoDB is running
- Check that the user exists in database
- Verify passlib is installed: `pip install passlib`

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
