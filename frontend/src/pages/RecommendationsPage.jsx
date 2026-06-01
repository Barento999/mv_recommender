import { useState, useEffect } from "react";
import MovieCard from "../components/MovieCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import recommendationService from "../services/recommendationService";
import useAuth from "../hooks/useAuth";

function RecommendationsPage() {
  const { token } = useAuth();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const data = await recommendationService.getRecommendations(20, token);
      setRecommendations(data.recommendations || []);
      setMessage(data.message);
    } catch (error) {
      console.error("Error loading recommendations:", error);
      setMessage("Failed to load recommendations");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecommendations();
  }, []);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">Recommended For You</h1>
        <p className="text-gray-400 mb-8">{message}</p>

        {loading ? (
          <LoadingSkeleton count={12} />
        ) : recommendations.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {recommendations.map((movie) => (
              <MovieCard
                key={movie._id}
                movie={movie}
                onFavoriteChange={loadRecommendations}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No recommendations yet</p>
            <p className="text-gray-500">
              Add some favorite movies to get personalized recommendations!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default RecommendationsPage;
