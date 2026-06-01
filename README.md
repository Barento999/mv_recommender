# Movie Recommendation System

A full-stack web application for discovering and managing movie recommendations with personalized suggestions based on user preferences.

## Features

### Backend (FastAPI + MongoDB)

- ✅ User authentication with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ CRUD operations for movies
- ✅ User ratings and favorites management
- ✅ Content-based recommendation engine
- ✅ Search and filtering capabilities
- ✅ RESTful API architecture
- ✅ CORS enabled for frontend integration
- ✅ Async database operations with Motor

### Frontend (React + Vite)

- ✅ Modern Netflix-inspired UI
- ✅ Responsive design (Mobile, Tablet, Desktop)
- ✅ User authentication flow
- ✅ Movie browsing with search and filters
- ✅ Movie details page with trailer
- ✅ Rating and favorites system
- ✅ Personalized recommendations
- ✅ User profile management
- ✅ Context API for state management
- ✅ React Router for navigation

## Tech Stack

### Backend

- **Framework**: FastAPI
- **Database**: MongoDB
- **Async Driver**: Motor
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Server**: Uvicorn

### Frontend

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router DOM
- **Icons**: Lucide React
- **State Management**: Context API

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 5.0+ (local or cloud)

### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**

   ```bash
   cp .env.example .env
   ```

5. **Configure .env**

   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=movie_recommendation
   SECRET_KEY=your-secret-key-change-in-production
   DEBUG=True
   ```

6. **Run backend server**

   ```bash
   python -m app.main
   # or
   uvicorn app.main:app --reload
   ```

   Backend will be available at: `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Create .env file**

   ```bash
   cp .env.example .env
   ```

4. **Configure .env**

   ```env
   VITE_API_URL=http://localhost:8000
   VITE_APP_NAME=Movie Recommendation System
   ```

5. **Run development server**

   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

## Project Structure

```
movie-recommendation-system/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── movie.py
│   │   │   ├── rating.py
│   │   │   └── favorite.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── movie.py
│   │   │   ├── rating.py
│   │   │   ├── favorite.py
│   │   │   └── recommendation.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── movie_service.py
│   │   │   ├── rating_service.py
│   │   │   ├── favorite_service.py
│   │   │   └── recommendation_service.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── movies.py
│   │   │   ├── ratings.py
│   │   │   ├── favorites.py
│   │   │   └── recommendations.py
│   │   ├── middleware/
│   │   │   └── auth.py
│   │   ├── utils/
│   │   │   └── security.py
│   │   ├── main.py
│   │   ├── database.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── HomePage.jsx
    │   │   ├── LoginPage.jsx
    │   │   ├── RegisterPage.jsx
    │   │   ├── MoviesPage.jsx
    │   │   ├── MovieDetailsPage.jsx
    │   │   ├── FavoritesPage.jsx
    │   │   ├── RecommendationsPage.jsx
    │   │   ├── ProfilePage.jsx
    │   │   └── NotFoundPage.jsx
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   ├── MovieCard.jsx
    │   │   ├── ProtectedRoute.jsx
    │   │   ├── LoadingSkeleton.jsx
    │   │   ├── Pagination.jsx
    │   │   └── RatingStars.jsx
    │   ├── context/
    │   │   └── AuthContext.jsx
    │   ├── services/
    │   │   ├── authService.js
    │   │   ├── movieService.js
    │   │   ├── favoriteService.js
    │   │   ├── ratingService.js
    │   │   └── recommendationService.js
    │   ├── hooks/
    │   │   └── useAuth.js
    │   ├── config/
    │   │   └── api.js
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── .env.example
```

## API Documentation

### Authentication Endpoints

```
POST   /auth/register     - Register new user
POST   /auth/login        - Login user
GET    /auth/me           - Get current user (requires auth)
```

### Movies Endpoints

```
GET    /movies            - List all movies with pagination
GET    /movies/search     - Search movies by title/description
GET    /movies/{id}       - Get movie details
POST   /movies            - Create new movie (requires auth)
PUT    /movies/{id}       - Update movie (requires auth)
DELETE /movies/{id}       - Delete movie (requires auth)
```

### Favorites Endpoints

```
GET    /favorites                 - Get user favorites
POST   /favorites/add/{movie_id}  - Add to favorites (requires auth)
DELETE /favorites/remove/{movie_id} - Remove from favorites (requires auth)
GET    /favorites/check/{movie_id}  - Check if movie is favorited (requires auth)
```

### Ratings Endpoints

```
GET    /ratings           - Get user ratings (requires auth)
POST   /ratings/add       - Add/update rating (requires auth)
GET    /ratings/{movie_id} - Get rating for specific movie (requires auth)
```

### Recommendations Endpoint

```
GET    /recommendations          - Get personalized recommendations (requires auth)
GET    /recommendations/similar/{movie_id} - Get similar movies
```

## Database Collections

### Users

```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (hashed),
  created_at: DateTime
}
```

### Movies

```javascript
{
  _id: ObjectId,
  title: String,
  genre: [String],
  year: Number,
  rating: Number (0-10),
  description: String,
  poster_url: String,
  trailer_url: String (optional),
  created_at: DateTime
}
```

### Ratings

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  movie_id: ObjectId,
  rating: Number (1-10),
  created_at: DateTime
}
```

### Favorites

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  movie_id: ObjectId,
  created_at: DateTime
}
```

## Recommendation Algorithm

The system uses **Content-Based Filtering** to generate recommendations:

1. **Analyze User Preferences**: Examine user's favorite movies
2. **Extract Genres**: Collect genres from favorited movies
3. **Calculate Frequency**: Count genre occurrences
4. **Find Similar Content**: Query movies with similar genres
5. **Exclude Known Items**: Remove already watched/favorited movies
6. **Rank Results**: Sort by rating in descending order

## Security Features

- ✅ JWT-based authentication
- ✅ Bcrypt password hashing
- ✅ Protected API endpoints
- ✅ CORS configuration
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (MongoDB document validation)
- ✅ Environment variable configuration

## Performance Optimization

- ✅ Async/await for non-blocking operations
- ✅ Pagination for large datasets
- ✅ Database indexing on common queries
- ✅ Lazy loading in frontend
- ✅ Component-based UI with React

## Development

### Running in Development Mode

**Terminal 1 - Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

**Terminal 2 - Frontend**

```bash
cd frontend
npm install
npm run dev
```

### Building for Production

**Backend**

```bash
# Run with production settings
export DEBUG=False
export SECRET_KEY=your-production-secret-key
python -m app.main
```

**Frontend**

```bash
npm run build
# Output will be in dist/
```

## Testing

### Sample Curl Requests

**Register**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Login**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Get Movies**

```bash
curl http://localhost:8000/movies?skip=0&limit=10
```

## Troubleshooting

### MongoDB Connection Error

- Ensure MongoDB is running: `mongod`
- Check MONGODB_URL in .env file
- Verify MongoDB is accessible at the specified URL

### CORS Error

- Check that frontend URL is in ALLOWED_ORIGINS in backend/app/config.py
- Verify CORS middleware is properly configured

### Frontend API Errors

- Ensure backend is running on port 8000
- Check VITE_API_URL in frontend/.env file
- Open browser console for detailed error messages

## Contributing

1. Create a new branch for features/fixes
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI, React, and MongoDB**
