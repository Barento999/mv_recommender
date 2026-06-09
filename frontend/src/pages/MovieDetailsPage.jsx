import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Heart, Play } from "lucide-react";
import movieService from "../services/movieService";
import recommendationService from "../services/recommendationService";
import favoriteService from "../services/favoriteService";
import ratingService from "../services/ratingService";
import watchHistoryService from "../services/watchHistoryService";
import RatingStars from "../components/RatingStars";
import MovieCard from "../components/MovieCard";
import ReviewsSection from "../components/ReviewsSection";
import useAuth from "../hooks/useAuth";

function MovieDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, token } = useAuth();
  const [movie, setMovie] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [isFavorite, setIsFavorite] = useState(false);
  const [userRating, setUserRating] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMovieDetails = async () => {
      try {
        const movieData = await movieService.getMovieById(id);
        setMovie(movieData);

        if (isAuthenticated) {
          // Record in watch history
          try {
            await watchHistoryService.addToHistory(id, token);
          } catch (error) {
            console.warn("Could not record watch history:", error);
          }

          const fav = await favoriteService.checkFavorite(id, token);
          setIsFavorite(fav.is_favorite);

          try {
            const rating = await ratingService.getMovieRating(id, token);
            setUserRating(rating.rating);
          } catch (error) {
            setUserRating(0);
          }
        }

        const similarData = await recommendationService.getSimilarMovies(id, 6);
        setSimilar(similarData.similar || []);
      } catch (error) {
        console.error("Error loading movie:", error);
      } finally {
        setLoading(false);
      }
    };

    loadMovieDetails();
  }, [id, isAuthenticated, token]);

  const handleFavoriteToggle = async () => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    try {
      if (isFavorite) {
        await favoriteService.removeFavorite(id, token);
      } else {
        await favoriteService.addFavorite(id, token);
      }
      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error("Error toggling favorite:", error);
    }
  };

  const handleRating = async (rating) => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    try {
      await ratingService.addRating(id, rating, token);
      setUserRating(rating);
    } catch (error) {
      console.error("Error rating movie:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-400">Movie not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark">
      {/* Hero Section */}
      <div
        className="relative h-96 bg-cover bg-center"
        style={{ backgroundImage: `url(${movie.poster_url})` }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-60" />

        <button
          onClick={() => navigate(-1)}
          className="absolute top-8 left-8 flex items-center gap-2 bg-darkGray hover:bg-primary px-4 py-2 rounded transition z-10"
        >
          <ArrowLeft size={20} />
          Back
        </button>

        {/* Movie Title Overlay */}
        <div className="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-dark to-transparent">
          <h1 className="text-5xl font-bold">{movie.title}</h1>
          <p className="text-gray-300 mt-2">{movie.year}</p>
        </div>
      </div>

      {/* Content Section */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="md:col-span-2">
            {/* Rating and Genre */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-gray-400 mb-2">IMDb Rating</p>
                  <p className="text-4xl font-bold text-yellow-400">
                    {movie.rating.toFixed(1)}/10
                  </p>
                </div>
                <div>
                  <p className="text-gray-400 mb-2">Your Rating</p>
                  {isAuthenticated ? (
                    <RatingStars
                      initialRating={userRating}
                      onRate={handleRating}
                      interactive={true}
                    />
                  ) : (
                    <button
                      onClick={() => navigate("/login")}
                      className="text-primary hover:underline"
                    >
                      Sign in to rate
                    </button>
                  )}
                </div>
              </div>

              {/* Genres */}
              <div className="flex flex-wrap gap-2">
                {movie.genre.map((g) => (
                  <span
                    key={g}
                    className="bg-primary px-3 py-1 rounded text-sm"
                  >
                    {g}
                  </span>
                ))}
              </div>
            </div>

            {/* Description */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">Synopsis</h2>
              <p className="text-gray-300 leading-relaxed">
                {movie.description}
              </p>
            </div>

            {/* Trailer */}
            {movie.trailer_url && (
              <div className="mb-8">
                <h2 className="text-2xl font-bold mb-4">Trailer</h2>
                <div className="relative pt-[56.25%] bg-black rounded-lg overflow-hidden">
                  <iframe
                    className="absolute inset-0 w-full h-full"
                    src={movie.trailer_url.replace("watch?v=", "embed/")}
                    title="Movie Trailer"
                    allowFullScreen
                  />
                </div>
              </div>
            )}

            {/* Similar Movies */}
            {similar.length > 0 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">Similar Movies</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {similar.map((s) => (
                    <MovieCard
                      key={s._id}
                      movie={s}
                      onFavoriteChange={() => {}}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Reviews Section */}
            <ReviewsSection movieId={id} movieTitle={movie.title} />
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Poster */}
            <div className="sticky top-20">
              <img
                src={movie.poster_url}
                alt={movie.title}
                className="w-full rounded-lg mb-6 shadow-lg"
              />

              {/* Action Buttons */}
              <button
                onClick={handleFavoriteToggle}
                className={`w-full py-3 rounded-lg font-semibold transition flex items-center justify-center gap-2 mb-3 ${
                  isFavorite
                    ? "bg-primary hover:bg-red-600"
                    : "bg-darkGray hover:bg-primary"
                }`}
              >
                <Heart size={20} fill={isFavorite ? "currentColor" : "none"} />
                {isFavorite ? "Favorited" : "Add to Favorites"}
              </button>

              {movie.trailer_url && (
                <button className="w-full bg-darkGray hover:bg-primary py-3 rounded-lg font-semibold transition flex items-center justify-center gap-2">
                  <Play size={20} />
                  Watch Trailer
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MovieDetailsPage;
