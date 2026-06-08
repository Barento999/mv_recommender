import { Link } from "react-router-dom";
import { Heart, Info } from "lucide-react";
import { useState, useEffect } from "react";
import useAuth from "../hooks/useAuth";
import favoriteService from "../services/favoriteService";

function MovieCard({ movie, onFavoriteChange }) {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated, token } = useAuth();

  // Check if movie is already favorited
  useEffect(() => {
    const checkFavorite = async () => {
      if (!isAuthenticated || !token) return;
      
      try {
        const result = await favoriteService.checkFavorite(movie._id, token);
        if (result && result.is_favorite) {
          setIsFavorite(true);
          console.log("✅ Movie is favorited:", movie.title);
        } else {
          setIsFavorite(false);
        }
      } catch (error) {
        console.warn("Could not check favorite status:", error);
      }
    };

    checkFavorite();
  }, [movie._id, isAuthenticated, token, onFavoriteChange]);

  const handleFavoriteToggle = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!isAuthenticated) {
      alert("Please login to add favorites");
      return;
    }

    setIsLoading(true);
    try {
      if (isFavorite) {
        await favoriteService.removeFavorite(movie._id, token);
        setIsFavorite(false);
        console.log("✅ Removed from favorites:", movie.title);
      } else {
        await favoriteService.addFavorite(movie._id, token);
        setIsFavorite(true);
        console.log("✅ Added to favorites:", movie.title);
      }
      onFavoriteChange?.();
    } catch (error) {
      console.error("❌ Error toggling favorite:", error);
      alert("Failed to update favorite: " + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Link
      to={`/movies/${movie._id}`}
      className="group relative cursor-pointer overflow-hidden rounded-lg"
    >
      <div className="relative h-80 overflow-hidden bg-darkGray">
        <img
          src={movie.poster_url}
          alt={movie.title}
          className="h-full w-full object-cover group-hover:scale-110 transition duration-300"
        />
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition duration-300" />
      </div>

      {/* Content Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition duration-300 flex flex-col justify-end p-4">
        <h3 className="text-lg font-bold mb-1 line-clamp-2">{movie.title}</h3>
        <div className="flex items-center justify-between mb-3">
          <div className="flex gap-1">
            {movie.genre?.slice(0, 2).map((g) => (
              <span key={g} className="text-xs bg-primary px-2 py-1 rounded">
                {g}
              </span>
            ))}
          </div>
          <span className="text-yellow-400">★ {movie.rating.toFixed(1)}</span>
        </div>
        <p className="text-xs text-gray-300 mb-3 line-clamp-2">
          {movie.description}
        </p>

        {isAuthenticated ? (
          <div className="flex gap-2">
            <button
              onClick={handleFavoriteToggle}
              disabled={isLoading}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded transition ${
                isFavorite 
                  ? "bg-primary text-white" 
                  : "bg-darkGray hover:bg-primary"
              }`}
            >
              <Heart size={18} fill={isFavorite ? "currentColor" : "none"} />
              {isLoading ? "Loading..." : isFavorite ? "Favorited" : "Favorite"}
            </button>
            <Link
              to={`/movies/${movie._id}`}
              className="flex-1 flex items-center justify-center gap-2 py-2 rounded bg-darkGray hover:bg-primary transition"
            >
              <Info size={18} />
              Details
            </Link>
          </div>
        ) : (
          <Link
            to="/login"
            className="w-full flex items-center justify-center gap-2 py-2 rounded bg-primary hover:bg-red-600 transition"
          >
            Login to Add Favorites
          </Link>
        )}
      </div>

      {/* Static Info */}
      <div className="p-3 bg-darkGray group-hover:hidden">
        <h3 className="font-semibold truncate">{movie.title}</h3>
        <p className="text-sm text-gray-400">{movie.year}</p>
      </div>
    </Link>
  );
}

export default MovieCard;
