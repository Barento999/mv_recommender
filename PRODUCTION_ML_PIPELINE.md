# Production ML Pipeline - Complete Guide

A complete refactored ML recommendation system with CSV data handling, model training, evaluation, and persistence.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Production ML Pipeline                    │
│                                                               │
│  CSV Files  →  DataLoader  →  DataFrames  →  Trainer  →    │
│                                                  ↓            │
│  (movies.csv)                            CollaborativeFiltering
│  (users.csv)                             Model               │
│  (ratings.csv)                            ↓                  │
│                                      ModelEvaluator          │
│                                      (metrics)               │
│                                           ↓                  │
│                                      Model Persistence       │
│                                      (pickle)                │
│                                           ↓                  │
│                                      MongoDB Importer        │
│                                      (import data)           │
│                                           ↓                  │
│                                      FastAPI Integration     │
│                                      (serve predictions)     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 New ML Modules

### 1. `data_loader.py` - CSV Data Loading
Loads and validates CSV files with format checking, type conversion, and foreign key validation.

```python
from app.ml.data_loader import DataLoader

loader = DataLoader()
movies_df = loader.load_movies("data/movies.csv")
users_df = loader.load_users("data/users.csv")
ratings_df = loader.load_ratings("data/ratings.csv")

summary = loader.get_data_summary()
```

**CSV Format:**

`movies.csv`:
```
movie_id,title,genre,year,rating,description,poster_url
m00001,Movie Title,Action|Drama,2024,8.5,Description text,https://...
```

`users.csv`:
```
user_id,name,email
u00001,User Name,user@example.com
```

`ratings.csv`:
```
user_id,movie_id,rating
u00001,m00001,9
```

### 2. `csv_generator.py` - Synthetic Data Generation
Generates realistic CSV data with proper distributions.

```python
from app.ml.csv_generator import generate_csvs

csvs = generate_csvs(
    n_movies=2000,
    n_users=150,
    output_dir="data"
)
# Returns: {'movies': 'data/movies.csv', 'users': 'data/users.csv', ...}
```

### 3. `collaborative_filtering.py` - Refactored ML Model
Production-grade collaborative filtering with:
- Modular design (easy to swap algorithms)
- Model persistence (save/load)
- Training metrics
- Backward compatibility with old code

```python
from app.ml.collaborative_filtering import UserUserCollaborativeFiltering

# Create model
model = UserUserCollaborativeFiltering(k_neighbors=10)

# Train from DataFrame
model.train(ratings_df, movies_df, users_df)

# Get metrics
metrics = model.get_metrics()

# Save to disk
model.save("models/cf_model_v1.pkl")

# Load from disk
model.load("models/cf_model_v1.pkl")
```

### 4. `model_evaluator.py` - Model Quality Metrics
Evaluates model performance:
- Coverage (% of items recommendable)
- Sparsity impact
- Similarity distribution
- Rating distribution

```python
from app.ml.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator(model, ratings_df, movies_df)
evaluation = evaluator.get_full_evaluation()
```

### 5. `mongo_importer.py` - MongoDB Integration
Imports CSV data and trained models into MongoDB.

```python
from app.ml.mongo_importer import import_all_to_mongo

result = await import_all_to_mongo(
    movies_df, users_df, ratings_df, db
)
```

---

## 🚀 Quick Start

### Step 1: Generate CSV Data
```bash
cd backend
python -c "
from app.ml.csv_generator import generate_csvs
csvs = generate_csvs(2000, 150, 'data')
print(f'Generated: {csvs}')
"
```

### Step 2: Train Model
```bash
python train_model.py \
  --movies data/movies.csv \
  --users data/users.csv \
  --ratings data/ratings.csv \
  --output models \
  --generate
```

Expected output:
```
[MLTrainer] ======================================================================
[MLTrainer] ML RECOMMENDATION MODEL TRAINING PIPELINE
[MLTrainer] ======================================================================

[MLTrainer] [STEP 1] Preparing data...
[MLTrainer] Generating 2000 movies and 150 users...

[CSVGenerator] Generating 2000 movies...
[CSVGenerator] ✓ Generated data/movies.csv

[CSVGenerator] Generating 150 users...
[CSVGenerator] ✓ Generated data/users.csv

[CSVGenerator] Generating ratings (heavy-tail)...
[CSVGenerator] ✓ Generated 9,250 ratings in data/ratings.csv

[MLTrainer] [STEP 2] Loading and validating data...
[DataLoader] Loading movies from: data/movies.csv
[DataLoader] ✓ Loaded 2000 movies
[DataLoader] Loading users from: data/users.csv
[DataLoader] ✓ Loaded 150 users
[DataLoader] Loading ratings from: data/ratings.csv
[DataLoader] ✓ Loaded 9,250 ratings

[MLTrainer] [STEP 3] Training model...
[CF Model] ✓ Training complete in 0.423s
[CF Model]   • Users: 150 | Movies: 2000 | Ratings: 9,250
[CF Model]   • Sparsity: 99.7%

[MLTrainer] [STEP 4] Model evaluation...
[Evaluator] ✓ Evaluation complete

[MLTrainer] [STEP 5] Persisting model...
[CF Model] ✓ Model saved to: models/collaborative_filtering_model.pkl

[MLTrainer] [STEP 6] Activating model...
[MLPipeline] Global model updated

[MLTrainer] ======================================================================
[MLTrainer] ✓ TRAINING COMPLETE!
```

### Step 3: Import to MongoDB & Start API
```bash
# Start MongoDB
docker compose up -d

# (Optional) Import data to MongoDB with separate script

# Start FastAPI
uvicorn app.main:app --reload --port 8000
```

---

## 📊 ML Model Features

### User-User Collaborative Filtering

**Algorithm:**
1. Build user-item matrix from ratings
2. Compute cosine similarity between users
3. For recommendation:
   - Find k=10 most similar users
   - Predict unrated movie scores as weighted average
   - Return top-10 by predicted score

**Key Properties:**
- O(n²) similarity computation (efficient for <10K users)
- Handles cold start (new users)
- Sparse matrix support
- Graceful fallbacks

### Model Classes

```python
# Abstract base
class MLModel(ABC):
    def train() → bool
    async def recommend() → List[Tuple[str, float]]
    def get_metrics() → Dict

# Implementation
class UserUserCollaborativeFiltering(MLModel):
    def train(ratings_df, movies_df, users_df) → bool
    async def recommend(user_id, limit) → List[(movie_id, score)]
    def save(filepath) → bool
    def load(filepath) → bool
    def get_metrics() → Dict
```

---

## 📈 Metrics & Evaluation

### Training Metrics
- `n_users`: Number of users in training data
- `n_movies`: Number of movies
- `n_ratings`: Number of ratings
- `sparsity`: % of zero values in matrix (99%+ is normal)
- `training_time_seconds`: Time to build model
- `algorithm`: Algorithm name for versioning

### Quality Metrics
- **Coverage**: % of items that can be recommended (typically 80-100%)
- **Diversity**: Different genres in recommendations
- **Similarity Distribution**: User taste clustering patterns
- **Rating Distribution**: Skewness toward positive ratings

### Example Metrics Output
```json
{
  "training_metrics": {
    "n_users": 150,
    "n_movies": 2000,
    "n_ratings": 9250,
    "sparsity": 0.997,
    "training_time_seconds": 0.423,
    "algorithm": "user_user_cf"
  },
  "coverage_metrics": {
    "coverage": 0.95,
    "coverage_percent": "95.0%",
    "unique_items_recommended": 1900,
    "total_items": 2000
  },
  "sparsity_metrics": {
    "avg_ratings_per_user": 62,
    "avg_ratings_per_movie": 4.6,
    "min_ratings_per_user": 10,
    "max_ratings_per_user": 150
  }
}
```

---

## 🔄 Workflow: CSV to Production

### Scenario 1: Start from Scratch

```bash
# 1. Generate CSVs
python train_model.py --generate --data-dir data

# 2. Train model
python train_model.py --movies data/movies.csv --ratings data/ratings.csv

# 3. Model is ready for API
# Start FastAPI and make recommendations
```

### Scenario 2: Use Existing CSVs

```bash
# 1. Have CSVs ready (movies.csv, users.csv, ratings.csv)

# 2. Train model
python train_model.py \
  --movies data/movies.csv \
  --users data/users.csv \
  --ratings data/ratings.csv \
  --output models

# 3. Model saved to: models/collaborative_filtering_model.pkl
```

### Scenario 3: Scheduled Retraining

```bash
# Production: Use APScheduler for daily retraining
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def retrain_model():
    """Retrain model nightly with fresh data"""
    # Load latest CSVs
    # Train new model
    # Evaluate metrics
    # Backup old model
    # Deploy new model
    pass

scheduler.add_job(retrain_model, 'cron', hour=2, minute=0)
scheduler.start()
```

---

## 🔧 Advanced Configuration

### Custom Data Loader
```python
from app.ml.data_loader import DataLoader

loader = DataLoader()

# Load with custom paths
movies = loader.load_movies("path/to/custom_movies.csv")
users = loader.load_users("path/to/custom_users.csv")
ratings = loader.load_ratings("path/to/custom_ratings.csv")

# Get summary
summary = loader.get_data_summary()
```

### Custom Model Training
```python
from app.ml.collaborative_filtering import UserUserCollaborativeFiltering

# Create with custom k
model = UserUserCollaborativeFiltering(k_neighbors=20)

# Train
success = model.train(ratings_df, movies_df, users_df)

# Get metrics
metrics = model.get_metrics()

# Save
model.save("models/custom_model.pkl")
```

### Model Evaluation
```python
from app.ml.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator(model, ratings_df, movies_df)

# Individual evaluations
coverage = evaluator.evaluate_coverage(limit=10)
sparsity = evaluator.evaluate_sparsity_impact()
similarity = evaluator.evaluate_similarity_distribution()

# Full evaluation
full_eval = evaluator.get_full_evaluation()
```

---

## 📊 Data Specifications

### Movies CSV
```
Columns: movie_id, title, genre, year, rating, description, poster_url
Types: str, str, str, int, float, str, str
Validation:
  - movie_id: unique
  - year: 1900-2024
  - rating: 0-10
  - genre: pipe-separated (Action|Drama|Romance)
```

### Users CSV
```
Columns: user_id, name, email
Types: str, str, str
Validation:
  - user_id: unique
  - email: unique
```

### Ratings CSV
```
Columns: user_id, movie_id, rating
Types: str, str, float
Validation:
  - rating: 1-10
  - user_id, movie_id: must exist in respective CSVs
  - (user_id, movie_id): unique pairs
```

---

## 🎯 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Load 2000 movies | <0.1s | CSV parsing |
| Load 150 users | <0.1s | CSV parsing |
| Load 9250 ratings | 0.1-0.2s | CSV parsing + validation |
| Train model | 0.3-0.5s | Similarity computation O(n²) |
| Generate recommendation | 50-100ms | Per-user prediction |
| Save model | 0.1-0.2s | Pickle serialization |
| Load model | 0.05-0.1s | Pickle deserialization |

---

## ✅ Verification Checklist

- [ ] CSV files created in `data/` directory
- [ ] Data validates without errors
- [ ] Model trains successfully
- [ ] Model metrics computed
- [ ] Model saved to `models/` directory
- [ ] Model loaded successfully
- [ ] Recommendations generated for sample users
- [ ] API accepts and serves predictions
- [ ] MongoDB has data (optional)

---

## 🐛 Troubleshooting

### CSV File Issues
```
Error: File not found: data/movies.csv
Solution: Generate CSVs first with:
  python train_model.py --generate --data-dir data
```

### Data Validation Errors
```
Error: Invalid year in movies
Solution: Data loader will auto-clip years to 1900-current_year
```

### Model Training Failure
```
Error: Insufficient data
Solution: Need at least 2 users and 2 movies with ratings
         Current system generates 150 users and 2000 movies
```

### MongoDB Import Issues
```
Error: Connection refused
Solution: Start MongoDB first with:
  docker compose up -d
```

---

## 🚀 Production Deployment

### With Docker
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Generate data and train model
RUN python train_model.py --generate

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### With Kubernetes
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: retrain-ml-model
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: trainer
            image: reco-ml:latest
            command: ["python", "train_model.py", "--generate"]
```

---

## 📚 Code Examples

### End-to-End Example
```python
import asyncio
from app.ml.csv_generator import generate_csvs
from app.ml.data_loader import DataLoader
from app.ml.collaborative_filtering import create_model_from_csv, set_global_model
from app.ml.model_evaluator import ModelEvaluator

async def main():
    # 1. Generate data
    csvs = generate_csvs(2000, 150, "data")
    
    # 2. Load data
    loader = DataLoader()
    movies = loader.load_movies(csvs['movies'])
    users = loader.load_users(csvs['users'])
    ratings = loader.load_ratings(csvs['ratings'])
    
    # 3. Train model
    model = create_model_from_csv(
        csvs['ratings'],
        csvs['movies'],
        csvs['users'],
        k_neighbors=10
    )
    
    # 4. Evaluate
    evaluator = ModelEvaluator(model, ratings, movies)
    eval_results = evaluator.get_full_evaluation()
    print(f"Coverage: {eval_results['coverage_metrics']['coverage_percent']}")
    
    # 5. Save
    model.save("models/cf_v1.pkl")
    
    # 6. Set as global
    set_global_model(model)
    print("✓ Model ready for API!")

asyncio.run(main())
```

---

## 📖 Next Steps

1. Generate CSV data: `python train_model.py --generate`
2. Train model: `python train_model.py`
3. Start API: `uvicorn app.main:app --reload`
4. Make recommendations: `curl http://localhost:8000/recommendations`
5. Monitor metrics: Check model evaluation output

---

**Production ML Pipeline Ready! 🚀**
