# Fix: No Movies Showing in Frontend

## ❌ PROBLEM

Frontend shows "No movies found" even though there are 2,000 movies in the CSV files.

## 🔍 ROOT CAUSE

Movies are in **CSV files** (`backend/data/`) but **NOT in MongoDB database**.

The frontend fetches from MongoDB database, not CSV files.

## ✅ SOLUTION

### Step 1: Make Sure MongoDB is Running

```bash
# Start MongoDB
sudo systemctl start mongod

# Verify it's running
sudo systemctl status mongod
```

**Expected output:** `active (running)`

### Step 2: Seed Movies into Database

```bash
cd ~/Desktop/reco/backend
source venv/bin/activate
python seed_2000_movies_sync.py
```

**Expected output:**
```
Connecting to MongoDB...
Loading movies from CSV...
Seeding 2000 movies...
✅ Movies seeded successfully!
✅ Total: 2000 movies
```

### Step 3: Seed Users and Ratings (Optional but Recommended)

```bash
python seed_multi_users.py
python seed_ratings.py
```

### Step 4: Verify Data in Database

```bash
# Check if movies are in database
python -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.moviereco
    count = await db.movies.count_documents({})
    print(f'Total movies in DB: {count}')

asyncio.run(check())
"
```

**Expected output:** `Total movies in DB: 2000`

### Step 5: Refresh Frontend

1. Keep backend running
2. Refresh browser (or restart frontend)
3. Go to Movies page
4. Should now see 2,000 movies ✨

---

## 📊 DATA FLOW

```
CSV Files (backend/data/)
├─ movies.csv (2000 rows)
├─ users.csv (150 rows)
└─ ratings.csv (14725 rows)

     ↓ Run seed scripts

MongoDB Database
├─ movies collection (2000 docs)
├─ users collection (150 docs)
└─ ratings collection (14725 docs)

     ↓ Frontend queries

Frontend UI
├─ Movies page (shows 2000 movies)
├─ Recommendations (uses ratings)
└─ Favorites/Ratings (stores user data)
```

---

## 🔧 COMPLETE SETUP SEQUENCE

### Option A: Quick Setup (Recommended)

```bash
# Terminal 1: Start MongoDB
sudo systemctl start mongod

# Terminal 2: Backend folder
cd ~/Desktop/reco/backend
source venv/bin/activate

# Seed data
python seed_2000_movies_sync.py
python seed_multi_users.py
python seed_ratings.py

# Start backend
python -m uvicorn app.main:app --reload

# Terminal 3: Frontend
cd ~/Desktop/reco/frontend
npm install
npm run dev

# Browser
http://localhost:5173
```

### Option B: Using Docker

```bash
# Start MongoDB in Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Then follow Option A steps
```

---

## 🧪 TESTING

### Test 1: API Returns Movies

```bash
# Check backend
curl http://localhost:8000/movies | jq '.movies | length'

# Should return: 2000
```

### Test 2: Frontend Loads Movies

1. Open http://localhost:5173
2. Click "Browse Movies" or "Search"
3. Should see 12 movies per page
4. Total should show "2000 movies"

### Test 3: Search Works

1. Type "Action" in search box
2. Should find Action movies
3. Pagination should work

---

## 📁 SEED SCRIPT OPTIONS

### seed.py
```bash
python seed.py
```
Basic seed script - seeds initial data

### seed_2000_movies_sync.py (RECOMMENDED)
```bash
python seed_2000_movies_sync.py
```
Synchronously loads 2,000 movies from CSV

### seed_multi_users.py
```bash
python seed_multi_users.py
```
Seeds 150 users

### seed_ratings.py
```bash
python seed_ratings.py
```
Seeds 14,725 ratings (user-movie relationships)

### All at once:
```bash
python seed.py && python seed_multi_users.py && python seed_ratings.py
```

---

## ✅ VERIFICATION CHECKLIST

After following the steps:

- [ ] MongoDB running: `sudo systemctl status mongod`
- [ ] Movies seeded: `python seed_2000_movies_sync.py`
- [ ] Backend running: `http://localhost:8000/health` returns ok
- [ ] Frontend running: `http://localhost:5173` loads
- [ ] Movies page shows count: "Showing 1 - 12 of 2000 movies"
- [ ] Search works: Type in search box and get results
- [ ] Can click on movie cards

---

## 🐛 TROUBLESHOOTING

### "MongoDB connection refused"

**Solution:**
```bash
# Start MongoDB
sudo systemctl start mongod

# Or with Docker
docker run -d -p 27017:27017 mongo:latest
```

### "Seed script fails with connection error"

**Solution:**
```bash
# Make sure MongoDB is running first
sudo systemctl start mongod

# Then try seeding
python seed_2000_movies_sync.py
```

### "Still no movies after seeding"

**Solution:**
1. Check MongoDB has data:
   ```python
   python -c "
   import asyncio
   from motor.motor_asyncio import AsyncIOMotorClient
   
   async def check():
       client = AsyncIOMotorClient('mongodb://localhost:27017')
       db = client.moviereco
       count = await db.movies.count_documents({})
       print(f'Movies in DB: {count}')
   
   asyncio.run(check())
   "
   ```

2. If 0 movies, run seed again
3. Restart backend and frontend

### "API returns 0 movies"

**Solution:**
```bash
# Check backend API
curl http://localhost:8000/movies

# If empty, movies not in database
# Run: python seed_2000_movies_sync.py
```

### "Frontend still shows 'No movies'"

**Solution:**
1. Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
2. Clear browser cache
3. Restart frontend: `npm run dev`

---

## 🚀 FINAL COMMAND SEQUENCE

```bash
# 1. Ensure MongoDB is running
sudo systemctl start mongod

# 2. Navigate to backend
cd ~/Desktop/reco/backend
source venv/bin/activate

# 3. Seed the database (MOST IMPORTANT!)
python seed_2000_movies_sync.py

# 4. Start backend
python -m uvicorn app.main:app --reload

# 5. In new terminal - Start frontend
cd ~/Desktop/reco/frontend
npm install
npm run dev

# 6. Open browser
# http://localhost:5173

# 7. Navigate to Movies page
# Should now see 2,000 movies!
```

---

## 📝 WHAT EACH SEED DOES

### seed_2000_movies_sync.py
- **What:** Loads movies from `backend/data/movies.csv`
- **Result:** 2,000 movies in `db.movies` collection
- **File:** CSV with movie metadata (title, genre, year, rating, description)
- **Time:** ~5-10 seconds

### seed_multi_users.py
- **What:** Creates 150 test users
- **Result:** 150 users in `db.users` collection
- **File:** CSV with user data
- **Time:** ~2-5 seconds

### seed_ratings.py
- **What:** Creates 14,725 user ratings
- **Result:** 14,725 documents in `db.ratings` collection
- **File:** CSV with (user_id, movie_id, rating) tuples
- **Time:** ~5-10 seconds

**Total seed time:** ~15-25 seconds

---

## 🎯 KEY POINTS

1. **CSV data is in files** - not automatically in database
2. **Seed scripts move data** - from CSV to MongoDB
3. **Frontend needs database** - not CSV files
4. **Must seed before using** - or movies won't show

---

## ✨ AFTER FOLLOWING THIS GUIDE

✅ MongoDB running
✅ 2,000 movies in database
✅ Backend returning movies
✅ Frontend displaying movies
✅ All features working

Your system should be fully operational! 🚀
