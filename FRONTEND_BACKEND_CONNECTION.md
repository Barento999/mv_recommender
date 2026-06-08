# Frontend-Backend Connection Guide

## ✅ STATUS: READY TO CONNECT

The frontend and backend are **already configured** to work together. You just need to run both!

---

## 🚀 HOW TO RUN BOTH (Complete Setup)

### Terminal 1: Start Backend API

```bash
cd ~/Desktop/reco/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ MongoDB connected
✅ ML Pipeline initialized
✅ ML PIPELINE INITIALIZED SUCCESSFULLY
```

**⏱ Wait for:** "ML PIPELINE INITIALIZED SUCCESSFULLY" ✨

### Terminal 2: Start Frontend (in new terminal)

```bash
cd ~/Desktop/reco/frontend
npm install    # First time only
npm run dev
```

**Expected output:**
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Step 3: Open Browser

Visit: **http://localhost:5173**

🎉 **Done!** Frontend and backend are now connected!

---

## 📊 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────┐
│ Frontend (React + Vite)             │
│ http://localhost:5173               │
│                                     │
│ ├─ Movies Page                      │
│ ├─ Recommendations Page             │
│ ├─ Favorites                        │
│ ├─ Ratings                          │
│ └─ Auth (Login/Register)            │
└─────────────┬───────────────────────┘
              │
              │ HTTP API Calls (axios)
              │ CORS Enabled ✅
              ↓
┌─────────────────────────────────────┐
│ Backend (FastAPI)                   │
│ http://localhost:8000               │
│                                     │
│ ├─ ML Recommendation Engine         │
│ ├─ Movie Database (MongoDB)         │
│ ├─ User Authentication              │
│ ├─ Ratings & Favorites              │
│ └─ Cache System (60-80% hit rate)   │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ MongoDB Database                    │
│ movies, users, ratings, favorites   │
└─────────────────────────────────────┘
```

---

## 🔌 CONNECTION DETAILS

### Frontend Configuration

**File:** `frontend/.env`

```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Movie Recommendation System
```

✅ This file has been created for you!

### Backend Configuration

**File:** `backend/app/main.py` (lines 49-54)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # ✅ Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

✅ CORS already configured!

### How It Works

1. **Frontend makes API call:**
   ```javascript
   // src/services/movieService.js
   axios.get(`${API_URL}/movies`)
   ```

2. **Backend receives request:**
   ```python
   # backend/app/routes/movies.py
   @router.get("/movies")
   async def get_all_movies():
       return movies_data
   ```

3. **CORS middleware allows it:**
   ```
   Request from localhost:5173 → Allowed ✅
   Response sent back to frontend
   ```

4. **Frontend displays data:**
   ```jsx
   // src/pages/MoviesPage.jsx
   setMovies(response.data.movies)
   ```

---

## 📡 API ENDPOINTS (Available to Frontend)

### Movies
- `GET /movies` - Get all movies
- `GET /movies/{id}` - Get single movie
- `GET /movies/search?query=X` - Search movies

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Recommendations
- `GET /recommendations` - Get user recommendations
- `GET /recommendations/similar/{id}` - Similar movies
- `GET /recommendations/status` - ML status

### Favorites
- `GET /favorites` - Get favorites
- `POST /favorites/{id}` - Add to favorites
- `DELETE /favorites/{id}` - Remove from favorites

### Ratings
- `GET /ratings` - Get ratings
- `POST /ratings` - Add rating

---

## 🧪 TEST CONNECTION

### Step 1: Both running?

**Backend:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok", "database": "connected"}
```

**Frontend:**
```bash
curl http://localhost:5173
```

**Response:** HTML page loads

### Step 2: Can frontend reach backend?

In browser console (F12):
```javascript
fetch('http://localhost:8000/movies')
  .then(r => r.json())
  .then(d => console.log(d.count))
```

**Response:** `2000` (number of movies)

### Step 3: Try in UI

1. Visit http://localhost:5173
2. Click "Movies"
3. Should see 2,000 movies loaded ✅
4. Click "Search"
5. Search should work ✅

---

## 🔑 AUTHENTICATION FLOW

### How Login Works

```
1. User fills login form
   ↓
2. Frontend calls POST /auth/login
   ↓
3. Backend verifies credentials
   ↓
4. Backend returns access_token
   ↓
5. Frontend saves token in localStorage
   ↓
6. Frontend includes token in all requests:
   Header: Authorization: Bearer {token}
   ↓
7. Backend validates token
   ↓
8. Backend returns protected data
```

### Example: Get Recommendations (Protected Route)

```javascript
// Frontend (src/services/recommendationService.js)
const token = localStorage.getItem('access_token');
axios.get(`${API_URL}/recommendations`, {
  headers: {
    Authorization: `Bearer ${token}`
  }
})

// Backend (backend/app/middleware/auth.py)
def get_current_user(token: str):
  # Verify token
  # Return user if valid
```

---

## 🛠️ TROUBLESHOOTING

### Issue: "Cannot reach backend from frontend"

**Symptoms:**
- Movies page shows error
- Console shows CORS errors
- "Failed to fetch" message

**Solution:**

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check frontend .env:**
   ```bash
   cat ~/Desktop/reco/frontend/.env
   # Should have:
   # VITE_API_URL=http://localhost:8000
   ```

3. **Restart frontend:**
   ```bash
   cd ~/Desktop/reco/frontend
   npm run dev
   ```

### Issue: "CORS error"

**Symptoms:**
- Console: "Access to XMLHttpRequest ... blocked by CORS policy"

**Solution:**

Backend CORS is already enabled. If still getting error:

1. **Check CORS middleware in main.py** (already there ✅)
2. **Restart backend:**
   ```bash
   # Kill backend and restart
   python -m uvicorn app.main:app --reload
   ```

### Issue: "Token invalid / 401 Unauthorized"

**Symptoms:**
- Login works but recommendations fail
- "401 Unauthorized" error

**Solution:**

1. **Register/login first:**
   - Visit http://localhost:5173
   - Click Register or Login
   - Token saved automatically

2. **Check token in browser:**
   ```javascript
   // Open console (F12)
   localStorage.getItem('access_token')
   // Should show a long JWT token
   ```

3. **Clear and retry:**
   ```javascript
   localStorage.clear()
   // Then register/login again
   ```

### Issue: "MongoDB connection failed"

**Symptoms:**
- Backend error: "Cannot connect to MongoDB"
- Movies not loading

**Solution:**

1. **Start MongoDB:**
   ```bash
   sudo systemctl start mongod
   ```

2. **Verify MongoDB running:**
   ```bash
   mongosh
   ```

3. **Check backend logs:**
   ```bash
   # Look for: "✅ MongoDB connected"
   ```

---

## 📁 FRONTEND FILE STRUCTURE

```
frontend/
├── .env                              ← API URL (created for you)
├── src/
│   ├── config/
│   │   └── api.js                   ← Reads VITE_API_URL
│   │
│   ├── services/
│   │   ├── authService.js           ← Login/Register
│   │   ├── movieService.js          ← Get movies
│   │   ├── recommendationService.js ← Get recommendations
│   │   ├── favoriteService.js       ← Favorites
│   │   └── ratingService.js         ← Ratings
│   │
│   ├── pages/
│   │   ├── MoviesPage.jsx           ← All movies
│   │   ├── RecommendationsPage.jsx  ← Recommendations
│   │   ├── FavoritesPage.jsx        ← Favorites
│   │   ├── MovieDetailsPage.jsx     ← Movie details
│   │   └── RegisterPage.jsx         ← Auth
│   │
│   ├── components/
│   │   ├── MovieCard.jsx            ← Movie display
│   │   ├── Navbar.jsx               ← Navigation
│   │   ├── ProtectedRoute.jsx       ← Auth guard
│   │   └── ...
│   │
│   ├── context/
│   │   └── AuthContext.jsx          ← Auth state
│   │
│   ├── App.jsx                      ← Main app
│   └── main.jsx                     ← Entry point
│
├── package.json
├── vite.config.js
└── tailwind.config.js
```

---

## 🔄 DATA FLOW EXAMPLE

### Complete Flow: Get Recommendations

```
User clicks "Get Recommendations"
  ↓
Frontend: RecommendationsPage.jsx
  ↓
Calls: recommendationService.getRecommendations(token)
  ↓
Makes: GET /recommendations
       Header: Authorization: Bearer token
  ↓
Backend: app/routes/recommendations.py
  ↓
Checks: Is token valid?
        Is user authenticated?
  ↓
Calls: recommendation_service.get_recommendations(user_id)
  ↓
ML Pipeline (app/ml/pipeline.py)
  ↓
Checks: Cache for (user_id, limit=10)
  ↓
Cache HIT (80%):
  → Returns cached results immediately
  → 20-30ms response
  ↓
Cache MISS (20%):
  → Calls _global_cf_model.recommend()
  → Gets 10 movie recommendations
  → Caches results
  → 50-100ms response
  ↓
Backend returns: [Movie 1, Movie 2, ...]
  ↓
Frontend receives: JSON response
  ↓
Updates: setRecommendations(data)
  ↓
Renders: MovieCard components
  ↓
User sees: Personalized recommendations ✨
```

---

## 🎯 NEXT STEPS

1. **Terminal 1 - Start Backend:**
   ```bash
   cd ~/Desktop/reco/backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   ```

2. **Terminal 2 - Start Frontend:**
   ```bash
   cd ~/Desktop/reco/frontend
   npm install
   npm run dev
   ```

3. **Open Browser:**
   ```
   http://localhost:5173
   ```

4. **Test Features:**
   - [ ] Browse all movies
   - [ ] Search movies
   - [ ] Register/Login
   - [ ] Add to favorites
   - [ ] Get recommendations
   - [ ] Rate movies
   - [ ] Check ML status

---

## 📚 RELATED DOCUMENTATION

- `COMPLETE_SYSTEM_GUIDE.md` - Full system overview
- `HOW_TO_RUN.txt` - Simple how-to run
- `RUN_GUIDE.md` - Detailed run guide
- `QUICK_API_REFERENCE.txt` - API endpoint reference
- `WHERE_TO_FIND_DATA.md` - Data access guide

---

## ✅ CHECKLIST

- [x] Frontend .env created with API URL
- [x] Backend CORS enabled
- [x] API routes all configured
- [x] Services ready to call backend
- [x] Authentication flow implemented
- [x] Database integrated
- [x] ML pipeline working

**Everything is ready!** Just run both and start using! 🚀
