# MovieReco ML System - COMPLETE RUN GUIDE

**Quick Start in 3 minutes | Full Production Setup**

---

## 🚀 OPTION 1: Quick Start (Recommended for Testing)

### Step 1: Navigate to backend
```bash
cd ~/Desktop/reco/backend
```

### Step 2: Activate virtual environment
```bash
source venv/bin/activate
```

Or if using the venv directly:
```bash
# No need to activate, use the full path:
./venv/bin/python3 -m uvicorn app.main:app --reload
```

### Step 3: Start the application
```bash
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
🚀 Starting application...
✅ MongoDB connected
📊 Initializing ML Pipeline...
[1/4] Loading CSV Data...
✓ Data loaded in 0.45s
  Movies: 2000
  Users: 150
  Ratings: 14725
[2/4] Training Collaborative Filtering Model...
✓ CF Model trained in 0.32s
[3/4] Training Content-Based Model...
✓ Content-Based Model trained in 0.18s
[4/4] Initializing Performance Cache...
✓ Cache initialized
✅ ML PIPELINE INITIALIZED SUCCESSFULLY
```

✅ **Done!** App is running at `http://localhost:8000`

---

## 🎯 OPTION 2: Complete Workflow (Full Pipeline Training)

### Step 1: Navigate to backend
```bash
cd ~/Desktop/reco/backend
```

### Step 2: Train the complete ML system
```bash
./venv/bin/python3 train_complete_project.py
```

**What this does:**
- Loads all data from CSV files
- Trains 3 algorithms (CF, Content, MF)
- Evaluates each model
- Compares performance
- Tunes hyperparameters
- Generates project report
- Takes 15-30 seconds

**Output:**
```
======================================================================
[MLManager] STEP 1: DATA PREPARATION
======================================================================
Loading data from CSV files...
✓ Data loaded in 0.45s
  Movies: 2000
  Users: 150
  Ratings: 14725

======================================================================
[MLManager] STEP 2: MODEL TRAINING
======================================================================
[2.1] Training Collaborative Filtering...
✓ CF Model trained in 0.32s

[2.2] Training Content-Based...
✓ Content-Based Model trained in 0.18s

[2.3] Training Matrix Factorization...
✓ MF Model trained in 0.25s

======================================================================
[MLManager] STEP 3: MODEL EVALUATION
======================================================================
Evaluating CF Model...
Evaluating Content-Based Model...
Evaluating MF Model...

======================================================================
[MLManager] STEP 4: MODEL COMPARISON
======================================================================
Model Rankings (NDCG@10):
1. collaborative_filtering: 0.6543
2. content_based: 0.5892
3. matrix_factorization: 0.5234

======================================================================
[MLManager] ML PROJECT REPORT
======================================================================
Models trained and evaluated successfully!
```

### Step 3: Run the app normally
```bash
./venv/bin/python3 -m uvicorn app.main:app --reload
```

---

## 📊 OPTION 3: Simple Training Script

### Step 1: Navigate to backend
```bash
cd ~/Desktop/reco/backend
```

### Step 2: Run simple training
```bash
./venv/bin/python3 train_model.py
```

**What this does:**
- Quick model training
- Basic statistics
- Takes 2-3 seconds

**Output:**
```
🚀 Starting ML Training...
Loading data...
✓ Movies: 2000
✓ Users: 150
✓ Ratings: 14725

Training Collaborative Filtering model...
✓ Model trained in 0.32s

Generating recommendations...
Sample recommendations for user u00000:
  • Movie: The First Echo (Score: 0.89)
  • Movie: Shadow Dreams (Score: 0.87)
  • Movie: Lost Horizon (Score: 0.85)

✅ Training complete!
```

### Step 3: Run the app
```bash
./venv/bin/python3 -m uvicorn app.main:app --reload
```

---

## 🎬 OPTION 4: Demo & Visualization

### Step 1: Navigate to backend
```bash
cd ~/Desktop/reco/backend
```

### Step 2: Run the demo
```bash
./venv/bin/python3 ml_pipeline_demo.py
```

**What this does:**
- Loads data
- Trains all 3 models
- Shows sample recommendations
- Displays performance metrics
- Takes 5-10 seconds

**Output:**
```
═══════════════════════════════════════════════════════════
           MOVIEREGO ML PIPELINE DEMONSTRATION
═══════════════════════════════════════════════════════════

[DATA LOADING]
✓ Loaded 2000 movies
✓ Loaded 150 users  
✓ Loaded 14725 ratings

[MODEL TRAINING]
✓ Collaborative Filtering trained
✓ Content-Based trained
✓ Matrix Factorization trained

[SAMPLE RECOMMENDATIONS]
For user u00000:
  1. The First Echo (0.89) ★★★★★
  2. Shadow Dreams (0.87) ★★★★☆
  3. Lost Horizon (0.85) ★★★★☆

[PERFORMANCE METRICS]
CF Model: 0.6543 NDCG@10
Content Model: 0.5892 NDCG@10
MF Model: 0.5234 NDCG@10

✅ Demo complete!
```

### Step 3: Run the app
```bash
./venv/bin/python3 -m uvicorn app.main:app --reload
```

---

## 📡 OPTION 5: With Frontend (Full Stack)

### Terminal 1: Start Backend
```bash
cd ~/Desktop/reco/backend
./venv/bin/python3 -m uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Application startup complete
✅ ML PIPELINE INITIALIZED SUCCESSFULLY
```

### Terminal 2: Start Frontend (if available)
```bash
cd ~/Desktop/reco/frontend
npm install  # First time only
npm run dev
```

**Access at:**
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173` (or shown in terminal)

---

## 🧪 OPTION 6: Testing Everything

### Test 1: Check API Health
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

### Test 2: Check ML Pipeline Status
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
    "total_requests": 42,
    "cache_hits": 34,
    "hit_rate": 0.81,
    "total_entries": 15
  }
}
```

### Test 3: Get Recommendations (requires auth token)
```bash
# First, get an auth token by signing up or logging in
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# Then use the token to get recommendations
curl http://localhost:8000/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test 4: Get Similar Movies
```bash
curl http://localhost:8000/recommendations/similar/m00000
```

**Response:**
```json
{
  "similar": [
    {
      "_id": "m00001",
      "title": "Similar Movie Title",
      "genre": ["Action", "Adventure"],
      "year": 2023,
      "rating": 7.5
    }
  ],
  "count": 5
}
```

---

## 🔧 DETAILED SETUP (First Time)

### Step 1: Check Python Version
```bash
python3 --version
# Should be 3.10 or higher
```

### Step 2: Navigate to project
```bash
cd ~/Desktop/reco/backend
```

### Step 3: Create/activate virtual environment (if needed)
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate
```

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

**What gets installed:**
- FastAPI 0.136.3
- Uvicorn 0.24.0
- scikit-learn 1.5.0
- pandas 3.0.3
- numpy 2.4.6
- pymongo 4.6.0
- And more...

### Step 5: Verify installation
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/barento/Desktop/reco/backend')

from app.ml.collaborative_filtering import UserUserCollaborativeFiltering
from app.ml.content_based import ContentBasedRecommender
from app.ml.matrix_factorization import MatrixFactorization
from app.ml.pipeline import initialize_ml_pipeline

print("✅ All dependencies installed correctly!")
EOF
```

### Step 6: Set environment variables (optional)
```bash
cat > .env << 'EOF'
MONGO_URL=mongodb://localhost:27017
DB_NAME=moviereco
API_TITLE=Movie Recommendation API
API_VERSION=1.0.0
EOF
```

### Step 7: Start the application
```bash
python -m uvicorn app.main:app --reload
```

---

## 📈 PRODUCTION SETUP

### Using Docker
```bash
# Build image
docker build -t moviereco-backend -f Dockerfile .

# Run container
docker run -p 8000:8000 \
  -e MONGO_URL=mongodb://mongo:27017 \
  moviereco-backend
```

### Using Gunicorn (Production WSGI)
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -b 0.0.0.0:8000
```

### Using Systemd Service (Ubuntu/Linux)
```ini
[Unit]
Description=MovieReco ML API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/reco/backend
ExecStart=/path/to/reco/backend/venv/bin/python -m uvicorn app.main:app --port 8000

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl start moviereco
sudo systemctl enable moviereco
```

---

## 🐛 TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution:**
```bash
./venv/bin/pip install scikit-learn==1.5.0
```

### Issue: "Cannot connect to MongoDB"
**Solution:**
1. Install MongoDB: `sudo apt-get install mongodb`
2. Start MongoDB: `sudo systemctl start mongod`
3. Verify: `mongosh`

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: "ML Pipeline initialization failed"
**Solution:**
1. Check data files exist: `ls -la data/`
2. Verify CSV format: `head data/movies.csv`
3. Check venv has all dependencies: `pip list | grep scikit`
4. Check logs for specific error

### Issue: "API endpoints returning 401 Unauthorized"
**Solution:**
1. Get auth token first
2. Include in Authorization header
3. Or disable auth in config for development

---

## 📚 COMMAND REFERENCE

| Task | Command |
|------|---------|
| Activate venv | `source venv/bin/activate` |
| Install deps | `./venv/bin/pip install -r requirements.txt` |
| Run app (dev) | `./venv/bin/python -m uvicorn app.main:app --reload` |
| Run app (prod) | `./venv/bin/gunicorn app.main:app` |
| Train complete | `./venv/bin/python train_complete_project.py` |
| Train simple | `./venv/bin/python train_model.py` |
| Run demo | `./venv/bin/python ml_pipeline_demo.py` |
| Check status | `curl http://localhost:8000/recommendations/status` |
| View API docs | `http://localhost:8000/docs` |
| View Redoc | `http://localhost:8000/redoc` |

---

## ✅ VERIFICATION CHECKLIST

After startup, verify everything works:

- [ ] App starts without errors
- [ ] ML pipeline initializes (see startup logs)
- [ ] Health endpoint works: `curl http://localhost:8000/health`
- [ ] Status endpoint works: `curl http://localhost:8000/recommendations/status`
- [ ] Models are loaded (check logs for "✅ ML PIPELINE INITIALIZED")
- [ ] API docs available: `http://localhost:8000/docs`
- [ ] Database connected (check logs)

---

## 🎓 UNDERSTANDING THE STARTUP FLOW

```
You run:
  uvicorn app.main:app --reload

FastAPI starts
  ↓
Lifespan startup hook triggered
  ↓
connect_to_mongo()
  ├─ MongoDB connection established
  └─ ✅ MongoDB connected
  ↓
initialize_ml_pipeline()
  ├─ Load CSV data (2000 movies, 150 users, 14725 ratings)
  ├─ Train Collaborative Filtering model (0.3-0.5s)
  ├─ Train Content-Based model (0.2-0.3s)
  ├─ Initialize Performance Cache (60-80% hit rate)
  └─ ✅ ML PIPELINE INITIALIZED SUCCESSFULLY
  ↓
All routes registered
  ├─ /health
  ├─ /recommendations
  ├─ /recommendations/similar/{id}
  ├─ /recommendations/status
  └─ ... (other routes)
  ↓
App ready to serve requests
```

---

## 🚀 NEXT STEPS

1. **Start the app** using one of the options above
2. **Test the endpoints** using curl commands
3. **Check the status** at `/recommendations/status`
4. **Get recommendations** at `/recommendations`
5. **Monitor logs** for performance metrics
6. **Deploy** to production when ready

---

## 📞 QUICK HELP

**Everything stops or crashes?**
```bash
# Check logs for errors
tail -f backend/app.log

# Restart fresh
pkill -f uvicorn
./venv/bin/python -m uvicorn app.main:app --reload
```

**Want to reset everything?**
```bash
# Remove venv and reinstall
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

**All good? Ready to deploy?**
- See PRODUCTION_ML_PIPELINE.md for deployment guide
- See FINAL_COMPLETION_REPORT.md for full system details

---

**You're all set! The MovieReco ML System is ready to run. 🚀**
