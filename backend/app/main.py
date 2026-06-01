from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import connect_to_mongo, close_mongo_connection
from app.config import settings

# Import routers (make sure each has `router = APIRouter()`)
from app.routes import auth, movies, favorites, ratings, recommendations


# -------------------------
# Lifespan (startup/shutdown)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting application...")
    await connect_to_mongo()
    print("✅ MongoDB connected")
    
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
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])


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