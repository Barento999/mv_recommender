# 🚀 MovieReco - Complete Startup Guide

## Prerequisites
- MongoDB running on `localhost:27017`
- Node.js installed
- Python 3.10+ with venv

## 🎯 Step-by-Step Startup

### Step 1: Start MongoDB

**If MongoDB is installed locally:**
```bash
# Linux/Mac
mongod

# Or in background
mongod &

# Windows
mongod.exe
```

**Check if running:**
```bash
# Should connect without errors
mongo mongodb://localhost:27017
```

**If MongoDB is not installed:**
- [Install MongoDB Community Server](https://docs.mongodb.com/manual/installation/)
- Or use Docker: `docker run -d -p 27017:27017 mongo`

---

### Step 2: Start Backend (Terminal 1)

```bash
cd backend
./venv/bin/python -m uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**First startup will:**
- Auto-seed database with 2,000 movies, 150 users, 14,725 ratings
- Create default admin user: `admin@movierego.com`
- Initialize ML models

---

### Step 3: Set Admin Password (Terminal 2)

**After backend starts and shows "Application startup complete":**

```bash
cd backend
./venv/bin/python3 setup_admin.py
```

**Follow the prompts:**
```
Admin email (default: admin@movierego.com): [Press Enter]
Admin password (6+ characters): password123
Confirm password: password123
```

**Success output:**
```
✅ Admin user 'admin@movierego.com' created

📌 LOGIN CREDENTIALS:
   Email: admin@movierego.com
   Password: password123
```

---

### Step 4: Start Frontend (Terminal 3)

```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
```

---

### Step 5: Login to Application

1. Open browser: http://localhost:5173
2. Click **Login**
3. Enter credentials:
   - Email: `admin@movierego.com`
   - Password: `password123` (or what you set)
4. See "ADMIN" badge in navbar (red)
5. Access admin features from "More" dropdown

---

## 🎮 What You Can Do

### As Admin:
- **User Management** (`/admin/users`) - Manage all users
- **Analytics** (`/analytics`) - View system metrics
- **Admin Dashboard** (`/admin-dashboard`) - System overview
- Everything a regular user can do

### As Regular User:
- Browse 2,000 movies with posters
- Rate movies
- Add favorites & wishlist
- Get recommendations
- View watch history
- Write reviews

---

## 🔧 Troubleshooting

### "Connection refused" errors
**Problem:** MongoDB not running
**Solution:**
```bash
# Check if MongoDB is running
ps aux | grep mongod

# If not running, start it
mongod &

# Wait 5 seconds, then try again
```

### Backend won't start
**Problem:** Port 8000 already in use
**Solution:**
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Then restart backend
```

### Frontend won't start
**Problem:** Port 5173 already in use or npm not installed
**Solution:**
```bash
# Install dependencies
cd frontend
npm install

# Try a different port
npm run dev -- --port 3000
```

### Admin password not working
**Problem:** Setup script failed or MongoDB wasn't running
**Solution:**
```bash
# Verify MongoDB is running
mongo mongodb://localhost:27017

# Then run setup again
./venv/bin/python3 setup_admin.py
```

### ML models not training
**Problem:** Models train on first startup, takes 3-7 seconds
**Solution:**
```bash
# Check backend logs for "ML models initialized"
# Wait longer on first startup
# Refresh page if recommendations not showing
```

---

## 📊 System Components

| Component | Port | Status |
|-----------|------|--------|
| MongoDB | 27017 | Must be running |
| Backend | 8000 | Starts in Terminal 1 |
| Frontend | 5173 | Starts in Terminal 3 |

---

## 🎓 Testing RBAC

**Create test users:**

1. **Admin** (use the one you created)
   - Email: admin@movierego.com
   - See: User Management, Analytics, Admin Dashboard

2. **Moderator** (create new)
   - Register any email
   - Login as admin → User Management
   - Change role to "moderator"
   - See: Analytics, Moderation links

3. **Regular User** (create new)
   - Register any email
   - Login
   - See: Normal features only

---

## 💡 Tips

- **First startup takes longer** (ML initialization)
- **Recommendations need ratings** - Rate movies first to get recommendations
- **Admin features require login** - Non-admin users can't access /admin/users
- **Database auto-seeds** - Movies/users/ratings auto-loaded on first run
- **Hot reload enabled** - Edit backend/frontend code and see changes instantly

---

## 📝 Default Data

Generated automatically on first startup:
- **2,000 movies** with unique Unsplash posters
- **150 users** with realistic names
- **14,725 ratings** across movies
- **3 ML models** for recommendations

---

## ❓ Quick Commands Reference

```bash
# Start everything
# Terminal 1
cd backend && ./venv/bin/python -m uvicorn app.main:app --reload

# Terminal 2 (after backend starts)
cd backend && ./venv/bin/python3 setup_admin.py

# Terminal 3
cd frontend && npm run dev

# Stop everything
# Press Ctrl+C in each terminal
```

---

## 🎉 You're Ready!

Your complete movie recommendation system is now running with:
- ✅ Full RBAC (3 roles: user, moderator, admin)
- ✅ 2,000 movies with AI-generated posters
- ✅ ML-powered recommendations
- ✅ User ratings, favorites, wishlist
- ✅ Admin user management
- ✅ System analytics

**Happy coding!** 🚀
