# 🔐 RBAC Access Matrix - Complete Guide

## Quick Summary

| Feature | User | Moderator | Admin |
|---------|:----:|:---------:|:-----:|
| Browse Movies | ✅ | ✅ | ✅ |
| Search & Filter | ✅ | ✅ | ✅ |
| Rate Movies | ✅ | ✅ | ✅ |
| Write Reviews | ✅ | ✅ | ✅ |
| Add Favorites | ✅ | ✅ | ✅ |
| Wishlist | ✅ | ✅ | ✅ |
| Watch History | ✅ | ✅ | ✅ |
| Get Recommendations | ✅ | ✅ | ✅ |
| User Dashboard | ✅ | ✅ | ✅ |
| User Preferences | ✅ | ✅ | ✅ |
| **View Analytics** | ❌ | ✅ | ✅ |
| **Delete Reviews** | ❌ | ✅ | ✅ |
| **Edit Movies** | ❌ | ✅ | ✅ |
| **Admin Dashboard** | ❌ | ❌ | ✅ |
| **Manage Users** | ❌ | ❌ | ✅ |
| **Change User Roles** | ❌ | ❌ | ✅ |
| **View System Analytics** | ❌ | ❌ | ✅ |

---

## 👤 REGULAR USER (8 Permissions)

### What They Can Access:

#### 🎬 **Movies & Discovery**
- ✅ Browse all 2,000 movies
- ✅ View movie details (title, year, genre, rating, poster, description)
- ✅ Search movies by keyword
- ✅ Filter by genre, year, rating
- ✅ Sort by rating, year, title
- ✅ View top-rated movies

#### ⭐ **Ratings & Reviews**
- ✅ Rate movies (1-10 scale)
- ✅ Read reviews from other users
- ✅ Write own reviews
- ✅ Edit own reviews
- ✅ Delete own reviews
- ✅ Mark reviews as helpful

#### ❤️ **Favorites & Collections**
- ✅ Add movies to favorites
- ✅ Remove from favorites
- ✅ View favorites list
- ✅ Add movies to wishlist
- ✅ Set wishlist priority (low/normal/high)
- ✅ Add notes to wishlist items
- ✅ View wishlist with filtering

#### 📊 **Personalization**
- ✅ View watch history (auto-tracked)
- ✅ Get personalized recommendations
- ✅ View user dashboard (stats, ratings, favorites)
- ✅ Set genre preferences
- ✅ View preference analysis

#### 👤 **Profile**
- ✅ View own profile
- ✅ Edit own profile
- ✅ View account statistics

### Navbar Access:
```
Movies
Search
Recommendations
Favorites
Wishlist
More ▼
  ├─ Watch History
  ├─ Dashboard
  └─ Preferences
Profile
```

### Pages Available:
```
/movies
/search
/recommendations
/favorites
/wishlist
/watch-history
/user-dashboard
/preferences
/profile
```

---

## 🛡️ MODERATOR (12 Permissions)

### Everything Users Can Do PLUS:

#### 📊 **Analytics**
- ✅ View system-wide analytics dashboard
- ✅ Rating distribution charts
- ✅ Genre popularity analysis
- ✅ User engagement metrics
- ✅ Top movies by various metrics
- ✅ Timeline statistics
- ✅ Active vs dormant users

#### 🎬 **Content Moderation**
- ✅ Delete inappropriate reviews
- ✅ Flag reviews for further review
- ✅ Edit movie metadata (title, description, genre)
- ✅ View moderation reports
- ✅ Moderate user-generated content

#### 📈 **Content Insights**
- ✅ View genre analytics
- ✅ Track rating trends
- ✅ User engagement statistics
- ✅ Content performance metrics

### Navbar Access:
```
Movies
Search
Recommendations
Favorites
Wishlist
More ▼
  ├─ Watch History
  ├─ Dashboard
  ├─ Preferences
  ├─ Analytics          👈 NEW
  ├─ 🛡️ Moderation     👈 NEW
Profile
```

### Additional Pages:
```
/analytics                    👈 NEW
/moderation                   👈 NEW (if implemented)
```

---

## 👨‍💼 ADMIN (17 Permissions)

### Everything Users & Moderators Can Do PLUS:

#### 👥 **User Management**
- ✅ View all users in system
- ✅ View user details and statistics
- ✅ Change user roles (user ↔ moderator ↔ admin)
- ✅ Delete users
- ✅ View all user permissions
- ✅ Manage user accounts
- ✅ Reset user passwords (via setup script)

#### 📊 **System Analytics**
- ✅ All moderator analytics
- ✅ User statistics dashboard
- ✅ System-wide metrics
- ✅ User growth trends
- ✅ Engagement rates
- ✅ Content analysis

#### 🎬 **Content Management**
- ✅ Create movies
- ✅ Edit movie metadata
- ✅ Delete movies
- ✅ Manage genres
- ✅ Update posters/thumbnails
- ✅ All moderator content permissions

#### 🔐 **Role Management**
- ✅ Assign roles to users
- ✅ Revoke roles
- ✅ View all role definitions
- ✅ See permission details for each role
- ✅ Manage access control

#### 📈 **System Dashboard**
- ✅ View admin dashboard
- ✅ System health status
- ✅ Database statistics
- ✅ Movie/User/Rating counts
- ✅ Top-rated movies
- ✅ Active users

### Navbar Access:
```
Movies
Search
Recommendations
Favorites
Wishlist
More ▼
  ├─ Watch History
  ├─ Dashboard
  ├─ Preferences
  ├─ Analytics
  ├─ 🛡️ Moderation
  ├─ System Admin              👈 NEW
  └─ 👥 Manage Users          👈 NEW
Profile
```

### Additional Pages:
```
/admin-dashboard              👈 NEW
/admin/users                  👈 NEW
```

---

## 🔒 Backend API Protection

### User Endpoints (Accessible by All Logged-In Users)
```
POST   /auth/register           (anyone)
POST   /auth/login              (anyone)
GET    /auth/me                 (authenticated)

GET    /movies                  (all users)
GET    /movies/{id}             (all users)
GET    /movies/search           (all users)

POST   /ratings                 (all users)
GET    /ratings/{movie_id}      (all users)

POST   /favorites/add/{id}      (all users)
DELETE /favorites/remove/{id}   (all users)
GET    /favorites               (all users)

POST   /wishlist/add/{id}       (all users)
DELETE /wishlist/remove/{id}    (all users)
GET    /wishlist                (all users)

GET    /watch-history           (all users)
POST   /watch-history/track     (all users)

GET    /recommendations         (all users)

POST   /reviews                 (all users)
PUT    /reviews/{id}            (all users - own reviews only)
DELETE /reviews/{id}            (all users - own reviews only)

GET    /preferences             (all users)
PUT    /preferences             (all users)
```

### Moderator+ Endpoints
```
GET    /analytics/overview               (moderator+)
GET    /analytics/ratings-distribution   (moderator+)
GET    /analytics/genre-analytics        (moderator+)
GET    /analytics/user-engagement        (moderator+)
GET    /analytics/top-movies-analytics   (moderator+)
GET    /analytics/timeline-stats         (moderator+)

DELETE /reviews/{id}            (moderator+ can delete any review)
PUT    /movies/{id}             (moderator+ can edit)
```

### Admin+ Endpoints
```
GET    /admin/users                     (admin+)
GET    /admin/users/{id}                (admin+)
PUT    /admin/users/{id}/role           (admin only)
DELETE /admin/users/{id}                (admin only)

GET    /admin/users/roles/all           (admin+)
GET    /admin/users/stats/overview      (admin only)

GET    /admin-dashboard                 (admin+)
```

---

## 🎯 Typical User Journeys

### User Journey:
```
1. Register/Login
   ↓
2. Browse Movies → Rate → Add to Favorites
   ↓
3. Get Recommendations → Watch History
   ↓
4. Write Reviews → View Stats
   ↓
5. Set Preferences → Wishlist
```

### Moderator Journey:
```
1. Everything User does
   ↓
2. Check Analytics Dashboard
   ↓
3. Review flagged content
   ↓
4. Delete inappropriate reviews
   ↓
5. Edit movie metadata
```

### Admin Journey:
```
1. Everything Moderator does
   ↓
2. View Admin Dashboard
   ↓
3. Manage Users (view, update roles, delete)
   ↓
4. System Analytics & Metrics
   ↓
5. Create/Edit/Delete Movies
```

---

## 🔐 Frontend Protection

### Role-Based Route Access:
```javascript
// Protected routes check user role before rendering
/admin/users         → Admin only (redirects non-admin to home)
/admin-dashboard     → Admin only (redirects non-admin to home)
/analytics          → Moderator+ (redirects user to home)
/moderation         → Moderator+ (redirects user to home)
```

### Role-Based UI Elements:
```javascript
// Navbar links conditionally rendered based on role
user?.role === "admin" && <Link to="/admin/users">Manage Users</Link>
user?.role === "moderator" && <Link to="/moderation">Moderation</Link>
user?.role !== "user" && <Link to="/analytics">Analytics</Link>
```

---

## 📋 Test All Access Levels

### Step 1: Login with Each Role

```
👤 User
Email: user@movierego.com
Password: password123

🛡️ Moderator
Email: moderator@movierego.com
Password: password123

👨‍💼 Admin
Email: admin@movierego.com
Password: password123
```

### Step 2: Verify Access

**As User:**
- ✅ See basic features only
- ❌ Cannot access Analytics
- ❌ Cannot see User Management
- ❌ Cannot see Admin Dashboard

**As Moderator:**
- ✅ See Analytics link in "More" dropdown
- ✅ Can access /analytics
- ❌ Cannot access User Management
- ❌ Cannot access Admin Dashboard

**As Admin:**
- ✅ See all links in "More" dropdown
- ✅ Can access Analytics
- ✅ Can access User Management
- ✅ Can access Admin Dashboard
- ✅ See role badge (red ADMIN)

### Step 3: Test API Protection

```bash
# Try accessing admin endpoint as regular user
curl -H "Authorization: Bearer {user_token}" \
  http://localhost:8000/admin/users
# Response: 403 Forbidden

# Same endpoint as admin
curl -H "Authorization: Bearer {admin_token}" \
  http://localhost:8000/admin/users
# Response: 200 OK with user list
```

---

## 🎓 Permission Summary

### User (8 Permissions)
```
✓ read_movies
✓ rate_movies
✓ add_favorites
✓ write_reviews
✓ view_recommendations
✓ manage_wishlist
✓ view_watch_history
✓ view_preferences
```

### Moderator (12 Permissions)
```
✓ All User permissions
✓ delete_reviews
✓ edit_movies
✓ view_analytics
✓ moderate_reviews
```

### Admin (17 Permissions)
```
✓ All Moderator permissions
✓ manage_users
✓ manage_roles
✓ view_system_analytics
✓ manage_movies
✓ manage_content
```

---

## 🚀 Production Notes

1. **User Registration**: Creates account with default "user" role
2. **Admin Promotion**: Use `setup_user.py` script to change roles
3. **Role Hierarchy**: user (0) < moderator (1) < admin (2)
4. **API Protection**: All endpoints validate role via JWT token
5. **Frontend Protection**: Routes redirect based on user role
6. **Dual Protection**: Both backend and frontend enforce access control

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│           Frontend (React + Vite)               │
│  ┌──────────────────────────────────────────┐   │
│  │ Role-Based Route Guards                  │   │
│  │ • Redirect unauthorized users            │   │
│  │ • Show/hide navbar links by role         │   │
│  │ • Conditionally render components        │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                      ↓ (API Calls with JWT)
┌─────────────────────────────────────────────────┐
│           Backend (FastAPI)                     │
│  ┌──────────────────────────────────────────┐   │
│  │ RBAC Middleware                          │   │
│  │ • Verify JWT token                       │   │
│  │ • Extract user role                      │   │
│  │ • Check role permissions                 │   │
│  │ • Return 403 if unauthorized             │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                      ↓ (Authorized)
┌─────────────────────────────────────────────────┐
│           MongoDB Atlas                         │
│  ┌──────────────────────────────────────────┐   │
│  │ Users Collection                         │   │
│  │ • _id, name, email, password             │   │
│  │ • role (user/moderator/admin)            │   │
│  │ • permissions array                      │   │
│  │ • created_at timestamp                   │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## ✅ Current Implementation Status

- ✅ User role stored in database
- ✅ Role returned in login response
- ✅ Frontend navbar shows role badge
- ✅ Frontend routes check role before rendering
- ✅ Backend endpoints validate role via RBAC middleware
- ✅ 3-level permission hierarchy implemented
- ✅ All API endpoints protected
- ✅ Test credentials for all 3 roles available

**System is fully operational with complete RBAC!** 🎉
