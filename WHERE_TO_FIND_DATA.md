# WHERE TO FIND: RECOMMENDATIONS & ALL MOVIES

## 🎯 Quick Answer

**Recommendations:** `http://localhost:8000/recommendations`  
**All Movies:** `http://localhost:8000/movies`  
**Similar Movies:** `http://localhost:8000/recommendations/similar/{movie_id}`

---

## 🚀 HOW TO ACCESS (Step by Step)

### Step 1: Start the App
```bash
cd ~/Desktop/reco/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Step 2: Open Browser
Visit: `http://localhost:8000/docs`

This opens **Interactive API Documentation** where you can:
- See all endpoints
- Try each endpoint
- View responses
- Test with different parameters

---

## 📡 API ENDPOINTS

### 1️⃣ GET ALL MOVIES
**Endpoint:**
```
GET http://localhost:8000/movies
```

**Using curl:**
```bash
curl http://localhost:8000/movies
```

**Response Example:**
```json
{
  "movies": [
    {
      "_id": "m00000",
      "title": "Iron Guardian",
      "genre": ["Documentary", "War", "Action"],
      "year": 2004,
      "rating": 7.5,
      "description": "A thrilling story...",
      "poster_url": "https://via.placeholder.com/...",
      "trailer_url": "https://youtube.com/..."
    },
    {
      "_id": "m00001",
      "title": "Digital Storm 1",
      "genre": ["Action", "Animation"],
      "year": 2016,
      "rating": 6.8,
      ...
    }
  ],
  "count": 2000,
  "total": 2000
}
```

---

### 2️⃣ GET RECOMMENDATIONS FOR USER
**Endpoint:**
```
GET http://localhost:8000/recommendations?limit=10
```

**Requirements:** Authentication token needed

**Step 1: Sign Up / Login**
```bash
# Sign up
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Response includes token:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Step 2: Get Recommendations**
```bash
curl http://localhost:8000/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response Example:**
```json
{
  "recommendations": [
    {
      "_id": "m00123",
      "title": "The First Echo",
      "genre": ["Drama", "Mystery"],
      "year": 2020,
      "rating": 8.2,
      "description": "A captivating journey...",
      "poster_url": "https://...",
      "trailer_url": "https://..."
    },
    {
      "_id": "m00456",
      "title": "Shadow Dreams",
      "genre": ["Fantasy", "Adventure"],
      "year": 2019,
      "rating": 7.9,
      ...
    }
  ],
  "count": 10,
  "message": "Recommendations based on your favorites"
}
```

---

### 3️⃣ GET SIMILAR MOVIES
**Endpoint:**
```
GET http://localhost:8000/recommendations/similar/m00000
```

**Using curl:**
```bash
curl http://localhost:8000/recommendations/similar/m00000
```

**Response Example:**
```json
{
  "similar": [
    {
      "_id": "m00234",
      "title": "War Chronicles",
      "genre": ["Documentary", "War"],
      "year": 2005,
      "rating": 7.3,
      ...
    },
    {
      "_id": "m00567",
      "title": "Historical Drama",
      "genre": ["Documentary", "Action"],
      "year": 2018,
      "rating": 6.9,
      ...
    }
  ],
  "count": 5
}
```

---

### 4️⃣ SEARCH MOVIES BY TITLE
**Endpoint:**
```
GET http://localhost:8000/movies/search?query=Iron
```

**Using curl:**
```bash
curl http://localhost:8000/movies/search?query=Iron
```

---

### 5️⃣ GET MOVIE BY ID
**Endpoint:**
```
GET http://localhost:8000/movies/{movie_id}
```

**Example:**
```bash
curl http://localhost:8000/movies/m00000
```

---

### 6️⃣ CHECK ML SYSTEM STATUS
**Endpoint:**
```
GET http://localhost:8000/recommendations/status
```

**Using curl:**
```bash
curl http://localhost:8000/recommendations/status
```

**Response:**
```json
{
  "status": "ok",
  "models": {
    "collaborative_filtering": true,
    "content_based": true,
    "cache": true
  },
  "cache_stats": {
    "total_requests": 150,
    "cache_hits": 120,
    "hit_rate": 0.8,
    "total_entries": 45
  }
}
```

---

## 🌐 WEB INTERFACE

### Option 1: Interactive API Docs (Swagger UI)
```
URL: http://localhost:8000/docs
```

**Features:**
- See all endpoints
- Try each endpoint
- View request/response formats
- Automatic schema validation

### Option 2: Alternative API Docs (ReDoc)
```
URL: http://localhost:8000/redoc
```

**Features:**
- Read-only documentation
- Beautiful layout
- Searchable

### Option 3: OpenAPI Schema
```
URL: http://localhost:8000/openapi.json
```

**Features:**
- Machine-readable API specification
- Can import into Postman, etc.

---

## 📊 DATA STRUCTURE

### Movie Object
```json
{
  "_id": "m00000",
  "title": "Iron Guardian",
  "genre": ["Documentary", "War", "Action"],
  "year": 2004,
  "rating": 7.5,
  "description": "A thrilling story...",
  "poster_url": "https://via.placeholder.com/300x450?text=Iron+Guardian",
  "trailer_url": "https://youtube.com/watch?v=...",
  "created_at": "2024-06-09T12:34:56"
}
```

### Recommendation Object
```json
{
  "_id": "m00123",
  "title": "The First Echo",
  "genre": ["Drama", "Mystery"],
  "year": 2020,
  "rating": 8.2,
  "description": "A captivating journey...",
  "poster_url": "https://...",
  "trailer_url": "https://...",
  "predicted_score": 0.89
}
```

---

## 📁 DATA SOURCES

### CSV Files (Raw Data)
```
backend/data/
├── movies.csv       (2,000 movies)
├── users.csv        (150 users)
└── ratings.csv      (14,725 ratings)
```

**Movies CSV Structure:**
```
movie_id,title,genre,year,rating,description,poster_url
m00000,Iron Guardian,"Documentary|War|Action",2004,7.5,"A thrilling story...",...
m00001,Digital Storm 1,"Action|Animation",2016,6.8,"A thrilling story...",...
```

### Database (MongoDB)
```
Collections:
├── movies          (2000 documents)
├── users           (150 documents)
├── ratings         (14725 documents)
└── favorites       (user favorites)
```

---

## 🔍 FIND SPECIFIC MOVIES

### Method 1: Search API
```bash
curl "http://localhost:8000/movies/search?query=Iron"
```

### Method 2: Read CSV File
```bash
cat ~/Desktop/reco/backend/data/movies.csv | head -20
grep "Iron" ~/Desktop/reco/backend/data/movies.csv
```

### Method 3: Python Script
```python
import pandas as pd

df = pd.read_csv('backend/data/movies.csv')

# Get all movies
print(df)

# Search by title
iron_movies = df[df['title'].str.contains('Iron', case=False)]
print(iron_movies)

# Get movie by ID
movie = df[df['movie_id'] == 'm00000']
print(movie)
```

### Method 4: MongoDB Query
```bash
mongosh

use moviereco
db.movies.find({}).limit(10)
db.movies.find({title: /Iron/i})
db.movies.findOne({_id: ObjectId("...")})
```

---

## 📈 RECOMMENDATION WORKFLOW

### How Recommendations Work

```
1. User Requests Recommendations
   GET /recommendations?limit=10

2. System Checks Cache
   ✓ Cache HIT (60-80%): Return in 20-30ms
   ✗ Cache MISS (20-40%): Call model

3. ML Model Predicts
   - Uses Collaborative Filtering
   - Finds similar users
   - Calculates scores
   - Takes 50-100ms

4. Return Top 10 Movies
   - Sorted by predicted score
   - Includes movie details
   - Cache result for future

5. User Gets Movies
   [Movie 1, Movie 2, Movie 3, ...]
```

---

## 🧪 EXAMPLE: COMPLETE WORKFLOW

### Step 1: Start App
```bash
cd ~/Desktop/reco/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Step 2: Get All Movies
```bash
curl http://localhost:8000/movies | jq '.movies | length'
# Output: 2000
```

### Step 3: Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "pass123"
  }' | jq '.access_token' -r

# Copy token from response
TOKEN="eyJhbGciOiJIUzI1NiIs..."
```

### Step 4: Get Recommendations
```bash
curl http://localhost:8000/recommendations \
  -H "Authorization: Bearer $TOKEN" | jq '.recommendations'
```

### Step 5: Add Movie to Favorites
```bash
curl -X POST http://localhost:8000/favorites/m00000 \
  -H "Authorization: Bearer $TOKEN"
```

### Step 6: Get Similar Movies
```bash
curl http://localhost:8000/recommendations/similar/m00000 | jq '.similar'
```

### Step 7: Check Status
```bash
curl http://localhost:8000/recommendations/status | jq
```

---

## 📊 STATISTICS

### Total Data
- **Movies:** 2,000
- **Users:** 150
- **Ratings:** 14,725
- **Data Size:** 626 KB

### API Statistics
- **Endpoints:** 15+
- **Response Time:** 20-100ms
- **Cache Hit Rate:** 60-80%
- **Model Inference:** 50-100ms

---

## 🎬 INTERACTIVE TESTING

### Best Way to Test

**Visit:** `http://localhost:8000/docs`

Then:
1. Click on any endpoint (blue bar)
2. Click "Try it out"
3. Fill in parameters if needed
4. Click "Execute"
5. See response

**Example:** Try GET `/movies`
- Click on endpoint
- Click "Try it out"
- Click "Execute"
- See all 2000 movies loaded!

---

## 📝 COMMON QUERIES

### Get First 10 Movies
```bash
curl "http://localhost:8000/movies?limit=10"
```

### Get Movies by Genre
```bash
curl "http://localhost:8000/movies/search?query=Action"
```

### Get User Recommendations (Requires Auth)
```bash
curl http://localhost:8000/recommendations \
  -H "Authorization: Bearer TOKEN"
```

### Get Similar to Movie
```bash
curl http://localhost:8000/recommendations/similar/m00000
```

### Get Movie Details
```bash
curl http://localhost:8000/movies/m00000
```

### Check Cache Performance
```bash
curl http://localhost:8000/recommendations/status
```

---

## 🔑 KEY ENDPOINTS

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|----------------|
| GET | `/movies` | All movies | No |
| GET | `/movies/{id}` | Movie details | No |
| GET | `/movies/search` | Search movies | No |
| GET | `/recommendations` | User recommendations | Yes |
| GET | `/recommendations/similar/{id}` | Similar movies | No |
| GET | `/recommendations/status` | ML system status | No |
| POST | `/auth/register` | Register user | No |
| POST | `/auth/login` | Login user | No |
| POST | `/favorites/{id}` | Add to favorites | Yes |
| GET | `/favorites` | Get favorites | Yes |

---

## ✅ QUICK CHECKLIST

- [ ] App is running at `http://localhost:8000`
- [ ] Can access `/docs` for interactive testing
- [ ] Can get all movies from `/movies`
- [ ] Can get ML status from `/recommendations/status`
- [ ] Can register user at `/auth/register`
- [ ] Can get recommendations at `/recommendations`
- [ ] Can get similar movies at `/recommendations/similar/{id}`

---

## 📚 NEXT STEPS

1. **Start the app** - `python -m uvicorn app.main:app --reload`
2. **Visit docs** - `http://localhost:8000/docs`
3. **Try endpoints** - Use Swagger UI to test
4. **Get movies** - `GET /movies`
5. **Get recommendations** - Register and call `/recommendations`
6. **Monitor** - Check `/recommendations/status`

---

**Everything is accessible via HTTP API or the web interface!** 🚀
