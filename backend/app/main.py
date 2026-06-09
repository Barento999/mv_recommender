from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.database import connect_to_mongo, close_mongo_connection
from app.config import settings

# Import routers (make sure each has `router = APIRouter()`)
from app.routes import auth, movies, favorites, ratings, recommendations, recommendation_explanations, analytics, preferences, advanced_filter, wishlist, watch_history, reviews, user_management

# Import ML pipeline
from app.ml.pipeline import initialize_ml_pipeline

# Import data seeding
from app.services.seed_service import seed_database

logger = logging.getLogger(__name__)


# -------------------------
# Lifespan (startup/shutdown)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting application...")
    
    # Connect to MongoDB
    await connect_to_mongo()
    print("✅ MongoDB connected")
    
    # Seed database from CSV if empty
    print("\n📥 Checking database...")
    await seed_database()
    
    # Initialize ML Pipeline
    print("\n📊 Initializing ML Pipeline...")
    ml_success = await initialize_ml_pipeline()
    if ml_success:
        print("✅ ML Pipeline initialized")
    else:
        print("⚠️  ML Pipeline initialization incomplete")
    
    yield
    
    await close_mongo_connection()
    print("🛑 MongoDB disconnected")


# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(
    title=getattr(settings, "API_TITLE", "Movie Recommendation API"),
    version=getattr(settings, "API_VERSION", "1.0.0"),
    lifespan=lifespan,
)


# -------------------------
# CORS configuration
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "ALLOWED_ORIGINS", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Routes
# -------------------------
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
app.include_router(recommendations.router)
app.include_router(recommendation_explanations.router)
app.include_router(analytics.router)
app.include_router(preferences.router)
app.include_router(advanced_filter.router)
app.include_router(wishlist.router)
app.include_router(watch_history.router)
app.include_router(reviews.router)
app.include_router(user_management.router)

# -------------------------
# Basic endpoints
# -------------------------
@app.get("/")
async def root():
    return {
        "message": "Movie Recommendation System API",
        "version": getattr(settings, "API_VERSION", "1.0.0"),
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "database": "connected"
    }


# -------------------------
# Run server manually (optional)
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)