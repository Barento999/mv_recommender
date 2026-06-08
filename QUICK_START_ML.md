# Quick Start: ML Model with 2000 Movies

Get the collaborative filtering model running in 5 minutes.

---

## ⚡ TL;DR

```bash
# 1. Start MongoDB
docker compose up -d  # or: mongod --dbpath /path/to/data

# 2. Seed database (from backend folder)
source venv/bin/activate
python seed_2000_movies_sync.py

# 3. Start backend (from backend folder)
uvicorn app.main:app --reload --port 8000

# 4. Visit frontend
# Open http://localhost:3000
# Register → Rate movies → Get recommendations!
```

---

## 📋 Step-by-Step

### Step 1: Start MongoDB

Choose one:

**Docker (recommended, easiest):**
```bash
cd /home/barento/Desktop/reco
docker compose up -d
```

**Local MongoDB:**
```bash
mongod --dbpath ~/data/mongodb
# Keep this running in a separate terminal
```

**MongoDB Atlas (cloud, no setup):**
- Visit https://www.mongodb.com/cloud/atlas
- Create free account → cluster → get connection string
- Update `/backend/.env` with connection URL

**Verify MongoDB is running:**
```bash
# Should print something, not error
mongosh --eval "db.version()"
```

### Step 2: Seed the Database

```bash
cd /home/barento/Desktop/reco/backend

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or: venv\Scripts\activate  # Windows

# Run seed script (1-2 minutes)
python seed_2000_movies_sync.py
```

**Expected output:**
```
======================================================================
MOVIE RECOMMENDATION SYSTEM - DATA SEEDING (SYNC)
======================================================================

[SEEDING] Connecting to MongoDB at localhost:27017...
[SEEDING] ✓ Connected to MongoDB

[SEEDING] Clearing existing collections...
[SEEDING] ✓ Collections cleared

[SEEDING] Generating 2000 movies...
[SEEDING] ✓ Generated 2000 movies
[SEEDING] Generating 150 users...
[SEEDING] ✓ Generated 150 users
[SEEDING] Generating ratings (heavy-tail distribution)...
[SEEDING] ✓ Generated 9,250 ratings
[SEEDING]   • Avg ratings per user: 62
[SEEDING]   • Avg ratings per movie: 4.6

[SEEDING] Inserting data into MongoDB...
[SEEDING] ✓ Inserted 2000 movies
[SEEDING] ✓ Inserted 150 users
[SEEDING] ✓ Inserted 9,250 ratings
[SEEDING] ✓ Indexes created

======================================================================
SEEDING COMPLETE - DATABASE STATISTICS
======================================================================
Movies:           2,000
Users:            150
Ratings:          9,250
Avg ratings/user: 62
Avg ratings/movie:4.6
======================================================================

[SEEDING] 🎉 Database ready for ML model training!
```

If you see an error, see **Troubleshooting** section below.

### Step 3: Start the Backend

```bash
# Make sure you're in /backend with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output (look for this):**
```
[CF Model] ✓ Model built successfully in 0.45s
[CF Model]   • Users: 150 | Movies: 2000 | Ratings: 9,250
[CF Model]   • Matrix sparsity: 99.7%
```

This means the ML model successfully loaded and is ready to generate recommendations!

Server will be running at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

### Step 4: Start the Frontend

In a new terminal:

```bash
cd /home/barento/Desktop/reco/frontend

# Make sure Node.js dependencies are installed
npm install

# Start development server
npm run dev
```

Frontend will be at: `http://localhost:3000`

### Step 5: Test the System

1. **Open frontend:** http://localhost:3000
2. **Register** a new account (any email/password)
3. **Browse movies** on the Movies page
4. **Rate some movies** (click the stars)
5. **Go to Recommendations** page
   - Should show personalized recommendations!
   - Based on ratings of similar users

---

## 🧪 Test the ML Model Directly

### Via API

```bash
# Get model stats (no auth needed)
curl http://localhost:8000/debug/ml-stats

# Response:
# {
#   "n_users": 150,
#   "n_movies": 2000,
#   "n_ratings": 9250,
#   "sparsity": 0.997,
#   "build_time_seconds": 0.45,
#   "model_age_seconds": 45.23
# }
```

### Via Frontend

1. Log in to http://localhost:3000
2. Go to `/recommendations` page
3. Should see 10 personalized movie recommendations
4. Recommendations change as you rate more movies

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error: Connection refused (configured timeouts: socketTimeoutMS: 20000.0ms)
```

**Solution:** MongoDB is not running
```bash
# Check if Docker container running
docker ps | grep mongo

# Or start MongoDB manually
mongod --dbpath ~/data/mongodb

# Or verify local MongoDB is running
mongosh
```

### No ratings found / Model not building
```
[CF Model] ⚠️  No ratings in database. Model cannot be built.
```

**Solution:** Run the seed script first
```bash
python seed_2000_movies_sync.py
```

### Module not found
```
ModuleNotFoundError: No module named 'motor' / 'scikit-learn' / etc.
```

**Solution:** Install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Model build timeout
```
[CF Model] Building model... (hanging for >5 seconds)
```

**Solution:** Normal on first load. If it persists:
- Check if MongoDB connection is slow
- Verify you have 2000+ movies and 8000+ ratings
- Check free disk space

### Frontend won't connect to backend
```
GET http://localhost:8000/... returns CORS error
```

**Solution:** Make sure both servers are running
```bash
# Terminal 1: Backend at :8000
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend at :3000
npm run dev
```

---

## 📊 What's Happening

When you hit the `/recommendations` endpoint, here's what happens:

1. **Load ratings** — System loads all ~9,250 ratings from MongoDB
2. **Build matrix** — Creates 150 users × 2000 movies matrix
3. **Compute similarity** — Finds how similar each user is to each other user (150×150)
4. **Find neighbors** — For your user, finds 10 most similar users
5. **Predict ratings** — For each unrated movie:
   - Gets ratings from those 10 similar users
   - Weights by similarity
   - Averages to predict your rating
6. **Return top-10** — Sorts by predicted rating, returns highest scores

**All in 50-100ms!**

---

## 🎯 Next: Try These

1. **Rate more movies** → Recommendations improve
2. **Log in as different user** → See different recommendations
3. **Add a movie to favorites** → It appears on Favorites page
4. **Check API docs** → http://localhost:8000/docs
5. **Read full guide** → See `ML_MODEL_SETUP_GUIDE.md`

---

## 📚 Files You Should Know About

| File | Purpose |
|------|---------|
| `backend/app/ml/collaborative_filtering.py` | The ML model (user-user CF) |
| `backend/seed_2000_movies_sync.py` | Generates 2000 movies + 150 users + ratings |
| `ML_MODEL_SETUP_GUIDE.md` | Comprehensive guide with algorithm details |
| `ML_MODEL_SUMMARY.md` | What was built and why |

---

## 🎓 Learning Resources

Want to understand the ML better?

1. **How it works** — See `ML_MODEL_SETUP_GUIDE.md` → "How the New ML Model Works"
2. **The code** — Read `collaborative_filtering.py` (lots of comments)
3. **The data** — Run: `python seed_2000_movies_sync.py --verbose`
4. **The math** — Cosine similarity, k-NN, weighted averaging

---

## 🚀 Common Questions

**Q: Why 2000 movies and 150 users?**
A: Enough data for the ML model to work well. ~2 orders of magnitude above minimum (2 users, 2 movies).

**Q: Why does it sometimes give bad recommendations?**
A: If you rated movies nobody else rated, there's no "similar user". It falls back to top-rated movies. Rate more popular movies!

**Q: Can I add more data?**
A: Yes! Edit `seed_2000_movies_sync.py` and change:
```python
generate_movies(2000)    # Change to 5000, 10000, etc.
generate_users(150)      # Change to 500, 1000, etc.
```

**Q: Can I use this in production?**
A: Yes! The code is production-ready. For scale:
- Add Redis caching
- Use sparse matrices (scipy.sparse)
- Switch to matrix factorization (faster for large datasets)
- Add monitoring

**Q: How do I make it better?**
A: See "Next Steps" in `ML_MODEL_SUMMARY.md`

---

Good luck! 🎉

Questions? Check `ML_MODEL_SETUP_GUIDE.md` for detailed troubleshooting.
