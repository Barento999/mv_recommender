import { Link } from "react-router-dom";
import { Heart, Info, Lightbulb, TrendingUp, Zap } from "lucide-react";
import { useState } from "react";
import favoriteService from "../services/favoriteService";
import useAuth from "../hooks/useAuth";

function RecommendationCard({ movie, explanation, onFavoriteChange }) {
  const { token, isAuthenticated } = useAuth();
  const [isFavorited, setIsFavorited] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  const handleFavorite = async () => {
    if (!isAuthenticated) {
      alert("Please login to add favorites");
      return;
    }

    setIsLoading(true);
    try {
      if (isFavorited) {
        await favoriteService.removeFavorite(movie._id, token);
        setIsFavorited(false);
      } else {
        await favoriteService.addFavorite(movie._id, token);
        setIsFavorited(true);
      }
      if (onFavoriteChange) {
        onFavoriteChange();
      }
    } catch (error) {
      console.error("Error updating favorite:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getExplanationIcon = () => {
    switch (explanation?.type) {
      case "Genre Match":
        return <Lightbulb size={16} className="text-yellow-400" />;
      case "High Rated":
        return <TrendingUp size={16} className="text-green-400" />;
      case "Recent & Popular":
        return <Zap size={16} className="text-blue-400" />;
      default:
        return <Info size={16} className="text-purple-400" />;
    }
  };

  return (
    <div className="bg-darkGray rounded-lg overflow-hidden border border-primary/20 hover:border-primary/50 transition-all duration-300 flex flex-col h-full">
      {/* Movie Poster */}
      <Link
        to={`/movies/${movie._id}`}
        className="relative block overflow-hidden bg-dark aspect-video"
      >
        <img
          src={movie.poster_url}
          alt={movie.title}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
          <span className="text-white text-sm font-semibold">View Details</span>
        </div>
      </Link>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        {/* Title */}
        <Link to={`/movies/${movie._id}`} className="hover:text-primary transition">
          <h3 className="font-bold text-white text-sm line-clamp-2 mb-2">
            {movie.title}
          </h3>
        </Link>

        {/* Year & Rating */}
        <div className="flex items-center justify-between mb-2 text-xs text-gray-400">
          <span>{movie.year}</span>
          <span className="text-yellow-400 font-bold">★ {movie.rating}</span>
        </div>

        {/* Genres */}
        <div className="flex flex-wrap gap-1 mb-3">
          {movie.genre?.slice(0, 2).map((g) => (
            <span
              key={g}
              className="text-xs bg-primary/20 text-primary px-2 py-1 rounded"
            >
              {g}
            </span>
          ))}
        </div>

        {/* Explanation Badge */}
        {explanation && (
          <div className="mb-3">
            <button
              onClick={() => setShowExplanation(!showExplanation)}
              className="w-full flex items-center gap-2 p-2 bg-primary/10 hover:bg-primary/20 rounded border border-primary/30 transition text-xs text-primary"
            >
              {getExplanationIcon()}
              <span className="font-semibold">{explanation.type}</span>
              <span className="ml-auto text-xs bg-primary px-2 py-1 rounded text-white font-bold">
                {explanation.confidence}%
              </span>
            </button>

            {/* Explanation Details */}
            {showExplanation && (
              <div className="mt-2 p-2 bg-dark rounded border border-primary/20 text-xs text-gray-300">
                {explanation.reasons.map((reason, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    <span>{reason}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Favorite Button */}
        <button
          onClick={handleFavorite}
          disabled={isLoading}
          className={`w-full mt-auto py-2 px-3 rounded font-semibold text-sm transition flex items-center justify-center gap-2 ${
            isFavorited
              ? "bg-primary text-white hover:bg-red-600"
              : "bg-gray-700 text-white hover:bg-gray-600"
          } ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          <Heart size={16} fill={isFavorited ? "currentColor" : "none"} />
          {isFavorited ? "Favorited" : "Add to Favorites"}
        </button>
      </div>
    </div>
  );
}

export default RecommendationCard;
