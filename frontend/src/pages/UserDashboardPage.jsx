import { useState, useEffect } from "react";
import { BarChart3, Heart, Star, TrendingUp, Clock } from "lucide-react";
import useAuth from "../hooks/useAuth";
import movieService from "../services/movieService";
import favoriteService from "../services/favoriteService";
import ratingService from "../services/ratingService";

function UserDashboardPage() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState({
    totalRatings: 0,
    totalFavorites: 0,
    avgRating: 0,
    topGenres: [],
  });
  const [recentRatings, setRecentRatings] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Load favorites
      const favData = await favoriteService.getFavorites(0, 5, token);
      setFavorites(favData.favorites || []);

      // Load ratings
      const ratingData = await ratingService.getUserRatings(token);
      setRecentRatings(ratingData.ratings || []);

      // Calculate stats
      const ratings = ratingData.ratings || [];
      const totalRatings = ratings.length;
      const avgRating =
        totalRatings > 0
          ? (ratings.reduce((sum, r) => sum + r.rating, 0) / totalRatings).toFixed(1)
          : 0;

      // Get top genres from rated movies
      const genreCount = {};
      for (const rating of ratings) {
        if (rating.genre) {
          const genres = Array.isArray(rating.genre) ? rating.genre : [rating.genre];
          genres.forEach((g) => {
            genreCount[g] = (genreCount[g] || 0) + 1;
          });
        }
      }

      const topGenres = Object.entries(genreCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([genre, count]) => ({ genre, count }));

      setStats({
        totalRatings,
        totalFavorites: favData.total || 0,
        avgRating,
        topGenres,
      });
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <p className="text-gray-400">Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Welcome, {user?.name}!</h1>
          <p className="text-gray-400">{user?.email}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Total Ratings */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Ratings</p>
                <p className="text-3xl font-bold">{stats.totalRatings}</p>
              </div>
              <Star className="text-primary" size={32} />
            </div>
          </div>

          {/* Average Rating */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Average Rating</p>
                <p className="text-3xl font-bold">{stats.avgRating} / 10</p>
              </div>
              <TrendingUp className="text-primary" size={32} />
            </div>
          </div>

          {/* Total Favorites */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Favorites</p>
                <p className="text-3xl font-bold">{stats.totalFavorites}</p>
              </div>
              <Heart className="text-primary" size={32} />
            </div>
          </div>

          {/* Recommendation Status */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Status</p>
                <p className="text-3xl font-bold text-green-500">Active</p>
              </div>
              <BarChart3 className="text-primary" size={32} />
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Top Genres */}
          <div className="lg:col-span-1">
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-xl font-bold mb-4">Your Top Genres</h2>
              {stats.topGenres.length > 0 ? (
                <div className="space-y-3">
                  {stats.topGenres.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-gray-300">{item.genre}</span>
                      <span className="bg-primary px-3 py-1 rounded text-sm font-semibold">
                        {item.count}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">Start rating movies to see your top genres!</p>
              )}
            </div>
          </div>

          {/* Recent Favorites */}
          <div className="lg:col-span-2">
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Heart size={20} className="text-primary" />
                Recent Favorites
              </h2>
              {favorites.length > 0 ? (
                <div className="space-y-4">
                  {favorites.map((movie) => (
                    <div
                      key={movie._id}
                      className="flex items-start gap-4 pb-4 border-b border-primary/10 last:border-b-0"
                    >
                      <img
                        src={movie.poster_url}
                        alt={movie.title}
                        className="w-12 h-16 rounded object-cover"
                      />
                      <div className="flex-1">
                        <h3 className="font-semibold text-white">{movie.title}</h3>
                        <p className="text-sm text-gray-400">{movie.year}</p>
                        <div className="flex gap-2 mt-2">
                          {movie.genre?.slice(0, 2).map((g) => (
                            <span
                              key={g}
                              className="text-xs bg-primary/20 px-2 py-1 rounded"
                            >
                              {g}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-yellow-400 font-bold">★ {movie.rating}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">No favorites yet. Start adding your favorites!</p>
              )}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8">
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Clock size={20} className="text-primary" />
              Recent Ratings
            </h2>
            {recentRatings.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-primary/20">
                      <th className="text-left py-3 px-4">Movie</th>
                      <th className="text-left py-3 px-4">Your Rating</th>
                      <th className="text-left py-3 px-4">Movie Rating</th>
                      <th className="text-left py-3 px-4">Year</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentRatings.slice(0, 10).map((rating) => (
                      <tr
                        key={rating._id}
                        className="border-b border-primary/10 hover:bg-dark transition"
                      >
                        <td className="py-3 px-4">{rating.title}</td>
                        <td className="py-3 px-4">
                          <span className="bg-primary px-3 py-1 rounded font-bold">
                            {rating.rating}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span className="text-yellow-400">★ {rating.rating}</span>
                        </td>
                        <td className="py-3 px-4">{rating.year}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-400">No ratings yet. Start rating movies!</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserDashboardPage;
