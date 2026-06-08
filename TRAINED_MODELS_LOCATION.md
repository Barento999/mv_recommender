# Where Are Trained Models Stored?

## 🎯 Short Answer

**Models are stored IN MEMORY (globally) - NOT on disk by default**

When you start the app, models are trained and kept in memory for fast access.

---

## 📍 Model Storage Locations

### 1. **Runtime (IN MEMORY) - Default** ✅ Production Ready
```
When app starts:
  app/main.py → initialize_ml_pipeline()
  ↓
  Models trained in RAM
  ↓
  Global variables in pipeline.py:
    _global_cf_model        (Collaborative Filtering)
    _global_content_model   (Content-Based)
    _global_cache           (Performance Cache)
  ↓
  Fast inference (50-100ms per prediction)
```

**Location:** `app/ml/pipeline.py` lines 20-24
```python
_global_model = None
_global_cf_model = None
_global_content_model = None
_global_cache = None
```

### 2. **Disk (OPTIONAL) - For Persistence**
```
When you run train_complete_project.py:
  ↓
  Models can be saved to:
  backend/models/
  ├─ cf_model.pkl
  ├─ content_model.pkl
  ├─ mf_model.pkl
  └─ project_metadata.json
```

**Current Status:** This directory doesn't exist yet (you can create it if needed)

---

## 🚀 How Models Work

### When You Start the App
```
Terminal:
  python -m uvicorn app.main:app --reload

What happens:
  1. FastAPI starts
  2. Lifespan hook calls initialize_ml_pipeline()
  3. Loads CSV data (2000 movies, 150 users, 14725 ratings)
  4. Trains models in memory:
     - CF model (K-NN, cosine similarity)
     - Content model (TF-IDF)
     - Cache (TTL + LRU)
  5. Models stored in global variables
  6. API endpoints use global models
  7. Total time: 3-7 seconds
```

### When You Make a Request
```
User Request:
  GET /recommendations?limit=10

Flow:
  1. Service calls get_recommendation(user_id)
  2. Pipeline function checks cache
  3. Cache HIT (60-80%): Return cached result → FAST ⚡
  4. Cache MISS (20-40%):
     - Use _global_cf_model to predict
     - Takes 50-100ms
     - Cache result
     - Return to user
```

---

## 📊 Storage Comparison

| Location | Status | Speed | Persistent | Use Case |
|----------|--------|-------|------------|----------|
| **Memory (Global)** | ✅ Default | ⚡ Very Fast | ❌ No | Production API |
| **Disk (PKL)** | ⏳ Optional | 🐢 Slower | ✅ Yes | Backup, Archive |
| **Database** | 💭 Future | 🐢 Slow | ✅ Yes | Multi-instance |

---

## 💾 Create Disk Storage (Optional)

If you want to save models to disk:

### Step 1: Create models directory
```bash
mkdir -p ~/Desktop/reco/backend/models
```

### Step 2: Train and save
```bash
cd ~/Desktop/reco/backend
source venv/bin/activate
python train_complete_project.py
```

This will:
- Train all models
- Save to `backend/models/`:
  - `cf_model.pkl`
  - `content_model.pkl`
  - `mf_model.pkl`
  - `project_metadata.json`

### Step 3: Check what was saved
```bash
ls -lh ~/Desktop/reco/backend/models/
```

Example output:
```
-rw-r--r-- 1 user user 2.5M cf_model.pkl
-rw-r--r-- 1 user user 1.2M content_model.pkl
-rw-r--r-- 1 user user 1.8M mf_model.pkl
-rw-r--r-- 1 user user 5.2K project_metadata.json
```

---

## 🔄 Complete Flow

```
┌─────────────────────────────────────────────┐
│ YOU: python -m uvicorn app.main:app --reload│
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ main.py lifespan startup hook               │
│ ↓ initialize_ml_pipeline()                  │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ app/ml/pipeline.py                          │
│ ├─ Load data from CSV                       │
│ ├─ Train CF model (0.3-0.5s)               │
│ ├─ Train Content model (0.2-0.3s)          │
│ ├─ Init cache                               │
│ └─ Store in global variables:               │
│    _global_cf_model                         │
│    _global_content_model                    │
│    _global_cache                            │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ Models READY IN MEMORY                      │
│ ✅ Fast access (no disk I/O)                │
│ ✅ Inference: 50-100ms                      │
│ ✅ Cache hits: 60-80%                       │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ API Ready at localhost:8000                 │
│ /recommendations → uses _global_cf_model    │
│ /recommendations/similar/{id} → Content     │
│ /recommendations/status → Cache stats       │
└─────────────────────────────────────────────┘
```

---

## 🔍 Check Models in Memory

### While app is running, in another terminal:
```bash
curl http://localhost:8000/recommendations/status
```

Response:
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
    "hit_rate": 0.8095,
    "total_entries": 15
  }
}
```

This confirms models are **loaded and running in memory**.

---

## 📈 Performance Benefits

### In-Memory Models (Default)
```
✅ No disk I/O
✅ Instant model access
✅ Cache hit: 20-30ms
✅ Cache miss: 50-100ms
✅ No persistence overhead
✅ Perfect for API servers
```

### Disk-Persisted Models (Optional)
```
✅ Survive server restart
✅ Share across processes
✅ Archive old versions
❌ Slower loading (hundreds of ms)
❌ Disk space usage
❌ Sync complexity
```

---

## 🎯 Recommendations

**For Production API (Recommended):**
- Keep models in memory
- Use caching for performance
- No need for disk storage
- Models retrain on each restart (3-7 seconds)

**For Model Backup/Archive:**
- Run `train_complete_project.py` occasionally
- Saves models to `backend/models/`
- Create version history
- Compare model performance

**For Multi-Instance Deployment:**
- Load models once per instance into memory
- Use shared cache (Redis)
- Each instance has its own models
- No inter-process coordination needed

---

## 🔧 Modify Storage Behavior (Advanced)

If you want to change where models are stored, edit:
- `app/ml/pipeline.py` - Change global variable locations
- `app/ml/ml_manager.py` - Line 35: `self.models_dir = Path(models_dir)`

---

## ✅ Summary

| Question | Answer |
|----------|--------|
| Where are trained models? | **IN MEMORY** (global variables in pipeline.py) |
| Are they saved to disk? | **Not by default**, but can be with `train_complete_project.py` |
| Where would they be saved? | `backend/models/` directory |
| Do I need to save them? | **No** - perfect for production API |
| How do I check if they're loaded? | `curl http://localhost:8000/recommendations/status` |
| How long does training take? | **3-7 seconds** on app startup |
| Is training automatic? | **Yes** - happens on startup |
| Can I skip training? | **No** - needed for predictions |
| Do models persist on restart? | **No** - retrained each time |
| Is that a problem? | **No** - only takes 3-7 seconds |

---

## 📚 Related Files

- `app/ml/pipeline.py` - Where models are stored (global variables)
- `app/ml/ml_manager.py` - Where models can be persisted (optional)
- `app/main.py` - Where initialization happens (lifespan hook)
- `backend/train_complete_project.py` - Script to train and save models

---

**Bottom Line:** Models are trained in memory when the app starts and used for real-time predictions. No disk storage needed for production. Everything is fast and automatic. ✨
