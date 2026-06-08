# 🚀 Quick Run Guide - Start in 60 Seconds

## The 3-Step Launch

### Step 1️⃣: Start Backend (Terminal 1)

```bash
cd /home/barento/Desktop/reco/backend
./venv/bin/python -m uvicorn app.main:app --reload
```

**Wait for:**
```
✅ ML Pipeline initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **This does automatically:**
- Connects to MongoDB
- Checks if database needs seeding
- Seeds 2,000 movies, 150 users, 14,725 ratings (if first time)
- Trains ML models (3-7 seconds)
- Starts API server

### Step 2️⃣: Start Frontend (Terminal 2)

```bash
cd /home/barento/Desktop/reco/frontend
npm install  # First time only
npm run dev
```

**Wait for:**
```
VITE v5.0.0  ready in 123 ms
➜  Local:   http://localhost:5173/
```

### Step 3️⃣: Open Browser

Visit: **`http://localhost:5173`**

---

## That's It! 🎉

Your system is running with:
- ✅ 2,000 movies
- ✅ ML recommendation system (3 algorithms)
- ✅ Real-time caching (60-80% hit rate)
- ✅ User ratings & favorites

---

## Quick Tests

### Test Backend
```bash
# Get movies
curl "http://localhost:8000/movies?skip=0&limit=5"

# Search
curl "http://localhost:8000/movies/search?q=Inception"

# Get recommendations for user 1
curl "http://localhost:8000/recommendations?user_id=1&limit=10"

# Check pipeline status
curl "http://localhost:8000/recommendations/status"
```

### Test Frontend
- Browse movies page
- Search for movies
- Get recommendations
- Rate movies
- Add favorites

---

## What's Happening Behind the Scenes

```
Terminal 1 (Backend):
  1. Connects to MongoDB ✅
  2. Loads 2,000 movies from CSV (first time) ✅
  3. Loads 150 users from CSV (first time) ✅
  4. Loads 14,725 ratings from CSV (first time) ✅
  5. Trains Collaborative Filtering model ✅
  6. Trains Content-Based model ✅
  7. Sets up caching system ✅
  8. API ready! ✅

Terminal 2 (Frontend):
  1. npm install (installs React, Vite, Axios, etc.)
  2. npm run dev starts Vite dev server
  3. Frontend loads VITE_API_URL from .env
  4. Ready to talk to backend at http://localhost:8000 ✅

Browser:
  1. Open http://localhost:5173
  2. See 2,000 movies from backend ✅
  3. Get recommendations from ML system ✅
  4. Rate movies and get personalized recommendations ✅
```

---

## Troubleshooting 1 Minute

| Problem | Solution |
|---------|----------|
| "Port 8000 in use" | `lsof -ti:8000 \| xargs kill -9` |
| "Port 5173 in use" | `lsof -ti:5173 \| xargs kill -9` |
| "No movies in frontend" | Restart backend (triggers seeding) |
| "ModuleNotFoundError" | Run: `./venv/bin/pip install -r requirements.txt` |
| "MongoDB connection error" | Ensure MongoDB is running |

---

## Files You Need to Know About

```
/backend/venv/bin/python          ← Use this Python
/backend/app/main.py              ← App entry point with auto-seeding
/backend/app/ml/pipeline.py       ← ML models initialization
/backend/app/services/seed_service.py  ← Auto database seeding
/frontend/.env                    ← API URL configuration
/backend/data/*.csv               ← Data sources
```

---

## Performance Notes

- **First startup**: 15-20 seconds (includes seeding + ML training)
- **Subsequent startups**: 5-10 seconds (seeding skipped)
- **ML inference time**: <100ms (with 60-80% cache hits)
- **Database queries**: Indexed by movie_id, user_id for fast access

---

**Done! Enjoy your movie recommendation system! 🎬**
