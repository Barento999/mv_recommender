# Quick Start Guide

Get the Movie Recommendation System up and running in minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (locally or use MongoDB Atlas)

## Option 1: Quick Local Setup (Recommended)

### Step 1: Start MongoDB

```bash
# If MongoDB is installed locally
mongod
```

Or use MongoDB Atlas:

- Create account at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string
- Update MONGODB_URL in backend/.env

### Step 2: Setup Backend

```bash
# From the root directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Update .env with your MongoDB URL if using Atlas
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/

# Run backend
python -m app.main
```

Backend will start at: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### Step 3: Setup Frontend (New Terminal)

```bash
# From the root directory
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will start at: http://localhost:5173

### Step 4: Seed Sample Data (Optional)

```bash
cd backend
python seed.py
```

This adds sample movies to the database.

## Using the Application

### 1. Register/Login

- Go to http://localhost:5173
- Click "Register" to create an account
- Login with your credentials

### 2. Explore Movies

- Browse all movies on the Movies page
- Search by title or description
- Filter by genre and year

### 3. Manage Favorites

- Click the heart icon on movie cards to add/remove from favorites
- View all favorites on the Favorites page

### 4. Rate Movies

- Click on a movie to open details page
- Rate the movie (1-10 stars)
- Your ratings are used for recommendations

### 5. Get Recommendations

- Go to Recommendations page
- View personalized suggestions based on your favorite movies

## API Testing

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and execute

### Using cURL

Register:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "email@example.com",
    "password": "password123"
  }'
```

Login:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email@example.com",
    "password": "password123"
  }'
```

Get Movies:

```bash
curl http://localhost:8000/movies?skip=0&limit=10
```

## Troubleshooting

### "Cannot connect to MongoDB"

- Ensure MongoDB is running: `mongod`
- Check MONGODB_URL in backend/.env
- If using Atlas, check connection string format

### "Frontend can't connect to backend"

- Ensure backend is running on port 8000
- Check VITE_API_URL in frontend/.env
- Check browser console for errors (F12)

### "CORS error"

- CORS is enabled by default for http://localhost:5173
- If using different port, update ALLOWED_ORIGINS in backend/app/config.py

## Production Deployment

### Backend Deployment (Heroku example)

1. Push to GitHub
2. Connect Heroku to repository
3. Add environment variables:
   - MONGODB_URL
   - SECRET_KEY (strong random key)
   - DEBUG=False

### Frontend Deployment (Vercel example)

1. Push to GitHub
2. Connect Vercel to repository
3. Set environment variables:
   - VITE_API_URL=https://your-backend-url

## Next Steps

- Read full [README.md](./README.md) for detailed documentation
- Check API docs at http://localhost:8000/docs
- Explore the codebase structure
- Customize colors in frontend/tailwind.config.js
- Add more features as needed

## Need Help?

- Check backend logs for server errors
- Check browser console (F12) for frontend errors
- Review API responses in Network tab
- Check the full README for more details

---

**Happy Movie Watching! 🎬**
