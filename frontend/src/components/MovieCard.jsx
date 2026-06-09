import { Link } from "react-router-dom";
import { Heart, Info, Bookmark } from "lucide-react";
import { useState, useEffect } from "react";
import useAuth from "../hooks/useAuth";
import favoriteService from "../services/favoriteService";
import wishlistService from "../services/wishlistService";

function MovieCard({ movie, onFavoriteChange }) {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated, token } = useAuth();

  // Check if movie is already favorited and in wishlist
  useEffect(() => {
    const checkStatus = async () => {
      if (!isAuthenticated || !token) return;
      
      try {
        const favResult = await favoriteService.checkFavorite(movie._id, token);
        if (favResult && favResult.is_favorite) {
          setIsFavorite(true);
        } else {
          setIsFavorite(false);
        }

        const wishResult = await wishlistService.checkWishlist(movie._id, token);
        if (wishResult && wishResult.is_in_wishlist) {
          setIsInWishlist(true);
        } else {
          setIsInWishlist(false);
        }
      } catch (error) {
        console.warn("Could not check status:", error);
      }
    };

    checkStatus();
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
      } else {
        await favoriteService.addFavorite(movie._id, token);
        setIsFavorite(true);
      }
      onFavoriteChange?.();
    } catch (error) {
      console.error("Error toggling favorite:", error);
      alert("Failed to update favorite");
    } finally {
      setIsLoading(false);
    }
  };

  const handleWishlistToggle = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!isAuthenticated) {
      alert("Please login to use wishlist");
      return;
    }

    setIsLoading(true);
    try {
      if (isInWishlist) {
        await wishlistService.removeFromWishlist(movie._id, token);
        setIsInWishlist(false);
      } else {
        await wishlistService.addToWishlist(movie._id, token);
        setIsInWishlist(true);
      }
      onFavoriteChange?.();
    } catch (error) {
      console.error("Error toggling wishlist:", error);
      alert("Failed to update wishlist");
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
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={handleFavoriteToggle}
              disabled={isLoading}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded transition text-sm ${
                isFavorite 
                  ? "bg-primary text-white" 
                  : "bg-darkGray hover:bg-primary"
              }`}
            >
              <Heart size={16} fill={isFavorite ? "currentColor" : "none"} />
              {isLoading ? "..." : isFavorite ? "Fav" : "Fav"}
            </button>
            <button
              onClick={handleWishlistToggle}
              disabled={isLoading}
              className={`flex-1 flex items-center justify-center gap-2 py-2 rounded transition text-sm ${
                isInWishlist 
                  ? "bg-primary text-white" 
                  : "bg-darkGray hover:bg-primary"
              }`}
            >
              <Bookmark size={16} fill={isInWishlist ? "currentColor" : "none"} />
              {isLoading ? "..." : isInWishlist ? "List" : "List"}
            </button>
            <Link
              to={`/movies/${movie._id}`}
              className="flex-1 flex items-center justify-center gap-2 py-2 rounded bg-darkGray hover:bg-primary transition text-sm"
            >
              <Info size={16} />
              Info
            </Link>
          </div>
        ) : (
          <Link
            to="/login"
            className="w-full flex items-center justify-center gap-2 py-2 rounded bg-primary hover:bg-red-600 transition"
          >
            Login
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
