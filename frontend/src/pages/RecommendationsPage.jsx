import { useState, useEffect } from "react";
import RecommendationCard from "../components/RecommendationCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import recommendationService from "../services/recommendationService";
import useAuth from "../hooks/useAuth";

function RecommendationsPage() {
  const { token } = useAuth();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [stats, setStats] = useState({
    total_favorites: 0,
  });

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const data = await recommendationService.getRecommendationsWithExplanations(20, token);
      setRecommendations(data.recommendations || []);
      setMessage(data.message);
      setStats({
        total_favorites: data.total_favorites || 0,
      });
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
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🎯 Recommended For You</h1>
          <p className="text-gray-400 mb-4">{message}</p>
          {stats.total_favorites > 0 && (
            <div className="inline-block bg-primary/10 border border-primary/30 rounded px-4 py-2">
              <p className="text-sm text-primary">
                ✨ Based on your {stats.total_favorites} favorite movies
              </p>
            </div>
          )}
        </div>

        {loading ? (
          <LoadingSkeleton count={12} />
        ) : recommendations.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {recommendations.map((movie) => (
                <RecommendationCard
                  key={movie._id}
                  movie={movie}
                  explanation={movie.explanation}
                  onFavoriteChange={loadRecommendations}
                />
              ))}
            </div>
            <div className="mt-8 p-4 bg-primary/10 border border-primary/20 rounded text-center">
              <p className="text-sm text-gray-300">
                💡 Hover over the recommendation badges to see why each movie is recommended!
              </p>
            </div>
          </>
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
