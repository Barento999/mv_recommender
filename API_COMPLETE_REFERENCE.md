# 📚 Complete API Reference

## Base URL
```
http://localhost:8000
```

---

## 🎬 Movies Endpoints

### GET /movies
**Get all movies with pagination**

```bash
curl "http://localhost:8000/movies?skip=0&limit=10"
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | integer | 0 | Number of movies to skip (pagination) |
| limit | integer | 10 | Number of movies to return (max 100) |
| genre | string | null | Filter by genre (e.g., "Action") |
| year | integer | null | Filter by year (e.g., 2020) |
| min_rating | float | null | Filter by minimum rating (0-10) |

**Response:**
```json
{
  "movies": [
    {
      "_id": "6a1e034438f20bf1b1a4664c",
      "title": "The Shawshank Redemption",
      "genre": ["Drama"],
      "year": 1994,
      "rating": 9.3,
      "description": "Two imprisoned men bond...",
      "poster_url": "https://...",
      "trailer_url": "https://...",
      "created_at": "2026-06-01T22:10:12.416000"
    }
  ],
  "total": 2000,
  "skip": 0,
  "limit": 10
}
```

---

### GET /movies/search
**Search movies by title or description**

```bash
curl "http://localhost:8000/movies/search?q=Inception&skip=0&limit=10"
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query |
| skip | integer | No | Pagination offset |
| limit | integer | No | Max results (default: 10) |

**Response:**
```json
{
  "movies": [
    {
      "_id": "6a1e034438f20bf1b1a4664e",
      "title": "Inception",
      "genre": ["Action", "Sci-Fi", "Thriller"],
      "year": 2010,
      "rating": 8.8,
      "description": "A thief who steals corporate secrets...",
      "poster_url": "https://...",
      "trailer_url": "https://...",
      "created_at": "2026-06-01T22:10:12.416000"
    }
  ],
  "total": 1,
  "query": "Inception"
}
```

---

### GET /movies/{movie_id}
**Get a specific movie by ID**

```bash
curl "http://localhost:8000/movies/6a1e034438f20bf1b1a4664c"
```

**Response:**
```json
{
  "_id": "6a1e034438f20bf1b1a4664c",
  "title": "The Shawshank Redemption",
  "genre": ["Drama"],
  "year": 1994,
  "rating": 9.3,
  "description": "Two imprisoned men bond...",
  "poster_url": "https://...",
  "trailer_url": "https://...",
  "created_at": "2026-06-01T22:10:12.416000"
}
```

---

### POST /movies
**Create a new movie (Requires authentication)**

```bash
curl -X POST http://localhost:8000/movies \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Movie",
    "genre": ["Action", "Drama"],
    "year": 2024,
    "rating": 8.5,
    "description": "A great movie...",
    "poster_url": "https://...",
    "trailer_url": "https://..."
  }'
```

**Request Body:**
```json
{
  "title": "string (required)",
  "genre": ["string"],
  "year": "integer",
  "rating": "float (0-10)",
  "description": "string",
  "poster_url": "string",
  "trailer_url": "string"
}
```

**Response:** Same as movie object above

---

### PUT /movies/{movie_id}
**Update a movie (Requires authentication)**

```bash
curl -X PUT http://localhost:8000/movies/6a1e034438f20bf1b1a4664c \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 9.5
  }'
```

**Response:** Updated movie object

---

### DELETE /movies/{movie_id}
**Delete a movie (Requires authentication)**

```bash
curl -X DELETE http://localhost:8000/movies/6a1e034438f20bf1b1a4664c \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "message": "Movie deleted successfully"
}
```

---

## ⭐ Ratings Endpoints

### GET /ratings
**Get all ratings with pagination**

```bash
curl "http://localhost:8000/ratings?skip=0&limit=10"
```

**Query Parameters:**
| Parameter | Type | Default |
|-----------|------|---------|
| skip | integer | 0 |
| limit | integer | 10 |

**Response:**
```json
{
  "ratings": [
    {
      "_id": "...",
      "user_id": "1",
      "movie_id": "6a1e034438f20bf1b1a4664c",
      "rating": 9.0,
      "created_at": "2026-06-01T22:10:12.416000"
    }
  ],
  "total": 14725
}
```

---

### POST /ratings
**Rate a movie (Requires authentication)**

```bash
curl -X POST http://localhost:8000/ratings \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": "6a1e034438f20bf1b1a4664c",
    "rating": 8.5
  }'
```

**Request Body:**
```json
{
  "movie_id": "string (required)",
  "rating": "float 0-10 (required)"
}
```

**Response:** Rating object

---

### GET /ratings/user/{user_id}
**Get all ratings from a specific user**

```bash
curl "http://localhost:8000/ratings/user/1"
```

**Response:** Array of rating objects

---

## 🎯 Recommendations Endpoints

### GET /recommendations
**Get personalized recommendations for a user**

```bash
curl "http://localhost:8000/recommendations?user_id=1&limit=10&model_type=cf"
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| user_id | string | required | User ID |
| limit | integer | 10 | Number of recommendations (1-100) |
| model_type | string | cf | "cf" (Collaborative), "content" (Content-based) |

**Response:**
```json
{
  "recommendations": [
    {
      "movie_id": "6a1e034438f20bf1b1a4664d",
      "title": "The Dark Knight",
      "score": 0.92,
      "rank": 1,
      "reason": "Similar users liked this movie"
    }
  ],
  "user_id": "1",
  "total": 10,
  "model_type": "cf"
}
```

---

### GET /recommendations/similar/{movie_id}
**Get movies similar to a given movie**

```bash
curl "http://localhost:8000/recommendations/similar/6a1e034438f20bf1b1a4664c?limit=10"
```

**Query Parameters:**
| Parameter | Type | Default |
|-----------|------|---------|
| limit | integer | 10 |

**Response:**
```json
{
  "similar_movies": [
    {
      "movie_id": "6a1e034438f20bf1b1a464d",
      "title": "The Dark Knight",
      "similarity_score": 0.85
    }
  ],
  "base_movie_id": "6a1e034438f20bf1b1a4664c",
  "total": 10
}
```

---

### GET /recommendations/status
**Get ML pipeline status**

```bash
curl "http://localhost:8000/recommendations/status"
```

**Response:**
```json
{
  "cf_model": true,
  "content_model": true,
  "cache": true,
  "cache_stats": {
    "total_requests": 1250,
    "cache_hits": 1000,
    "cache_misses": 250,
    "hit_rate": 0.8
  }
}
```

---

## ❤️ Favorites Endpoints

### GET /favorites
**Get all favorites (Requires authentication)**

```bash
curl "http://localhost:8000/favorites" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "favorites": [
    {
      "_id": "...",
      "user_id": "1",
      "movie_id": "6a1e034438f20bf1b1a4664c",
      "created_at": "2026-06-01T22:10:12.416000"
    }
  ],
  "total": 25
}
```

---

### POST /favorites
**Add movie to favorites (Requires authentication)**

```bash
curl -X POST http://localhost:8000/favorites \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": "6a1e034438f20bf1b1a4664c"
  }'
```

**Request Body:**
```json
{
  "movie_id": "string (required)"
}
```

**Response:** Favorite object

---

### DELETE /favorites/{movie_id}
**Remove movie from favorites (Requires authentication)**

```bash
curl -X DELETE http://localhost:8000/favorites/6a1e034438f20bf1b1a4664c \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "message": "Favorite removed successfully"
}
```

---

## 🔐 Authentication Endpoints

### POST /auth/signup
**Create a new account**

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe"
  }'
```

**Request Body:**
```json
{
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)",
  "name": "string (required)"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "_id": "...",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

### POST /auth/login
**Login to get access token**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Request Body:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "...",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## 🏥 System Endpoints

### GET /
**Root endpoint - API info**

```bash
curl "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Movie Recommendation System API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### GET /health
**Health check**

```bash
curl "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### GET /docs
**Interactive API documentation (Swagger UI)**

Visit: `http://localhost:8000/docs`

---

## 📊 ML Pipeline Details

### Models Available

#### 1. Collaborative Filtering (CF)
- **Algorithm**: User-to-user K-NN with cosine similarity
- **K-neighbors**: 10
- **Use case**: Best for users with similar tastes
- **Access**: `model_type=cf` in /recommendations

#### 2. Content-Based
- **Algorithm**: TF-IDF on movie genres
- **Use case**: Best when user profile is new or limited
- **Access**: `model_type=content` in /recommendations

#### 3. Matrix Factorization
- **Algorithm**: SVD with 50 latent factors
- **Use case**: Advanced pattern discovery
- **Status**: Trained but used internally in ranking

### Performance
- **Cache Hit Rate**: 60-80%
- **Average Response Time**: <100ms (cached), <500ms (uncached)
- **Model Training Time**: 3-7 seconds on startup
- **Inference Time**: <50ms per user

### Caching
- **TTL**: 3600 seconds (1 hour)
- **Max Entries**: 10,000
- **Strategy**: LRU (Least Recently Used) eviction

---

## ❌ Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid query parameter: limit must be between 1 and 100"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Movie not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 🔗 Usage Examples

### Example 1: Browse Movies
```bash
# Get first 20 movies
curl "http://localhost:8000/movies?skip=0&limit=20"

# Get action movies only
curl "http://localhost:8000/movies?genre=Action&limit=10"

# Get movies from 2020 onwards
curl "http://localhost:8000/movies?year=2020"
```

### Example 2: Search and Rate
```bash
# Search for a movie
curl "http://localhost:8000/movies/search?q=Inception"

# Get the movie ID from response
# Rate it (requires token)
curl -X POST http://localhost:8000/ratings \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": "MOVIE_ID",
    "rating": 9.0
  }'
```

### Example 3: Get Personalized Recommendations
```bash
# After rating some movies, get recommendations
curl "http://localhost:8000/recommendations?user_id=1&limit=15&model_type=cf"
```

### Example 4: Find Similar Movies
```bash
# Find movies similar to Inception
curl "http://localhost:8000/recommendations/similar/INCEPTION_MOVIE_ID?limit=10"
```

---

## 📱 Frontend Integration

### JavaScript Example
```javascript
// Get movies
const response = await fetch('http://localhost:8000/movies?skip=0&limit=10');
const data = await response.json();
console.log(data.movies);

// Get recommendations
const userId = "1";
const recsResponse = await fetch(
  `http://localhost:8000/recommendations?user_id=${userId}&limit=10`
);
const recommendations = await recsResponse.json();
console.log(recommendations.recommendations);
```

### React Example
```jsx
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;
const api = axios.create({ baseURL: API_URL });

// Get movies
const getMovies = async () => {
  const response = await api.get('/movies', {
    params: { skip: 0, limit: 10 }
  });
  return response.data.movies;
};

// Get recommendations
const getRecommendations = async (userId) => {
  const response = await api.get('/recommendations', {
    params: { user_id: userId, limit: 10 }
  });
  return response.data.recommendations;
};
```

---

## 🔄 Rate Limits

Currently no rate limiting is implemented. In production, consider:
- 100 requests per minute per IP
- 10,000 requests per hour per authenticated user
- Burst limits for spike handling

---

## 🔐 Authentication Details

- **Type**: JWT (JSON Web Tokens)
- **Header**: `Authorization: Bearer TOKEN`
- **Token Format**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **Expiration**: 7 days from login
- **Secret**: Stored in backend/.env

---

## 📞 API Documentation Interactive

Visit: **`http://localhost:8000/docs`** (Swagger UI)

This provides interactive testing of all endpoints with automatic request/response documentation.

---

*Generated: June 9, 2026*
*API Version: 1.0.0*
*Last Updated: Production Release*
