import { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Users,
  Activity,
  Film,
  Star,
  Heart,
  LineChart,
} from "lucide-react";
import analyticsService from "../services/analyticsService";

function AnalyticsDashboardPage() {
  const [overview, setOverview] = useState(null);
  const [ratingsDistribution, setRatingsDistribution] = useState([]);
  const [genreAnalytics, setGenreAnalytics] = useState([]);
  const [userEngagement, setUserEngagement] = useState(null);
  const [topMovies, setTopMovies] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [overviewData, ratingsData, genreData, engagementData, topMoviesData, timelineData] = await Promise.all([
        analyticsService.getOverview(),
        analyticsService.getRatingsDistribution(),
        analyticsService.getGenreAnalytics(),
        analyticsService.getUserEngagement(),
        analyticsService.getTopMoviesAnalytics(),
        analyticsService.getTimelineStats(),
      ]);

      setOverview(overviewData);
      setRatingsDistribution(ratingsData.distribution || []);
      setGenreAnalytics(genreData.genres || []);
      setUserEngagement(engagementData);
      setTopMovies(topMoviesData);
      setTimeline(timelineData.timeline || []);
    } catch (err) {
      console.error("Error loading analytics:", err);
      setError("Failed to load analytics data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <p className="text-gray-400">Loading analytics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={loadAnalytics}
            className="bg-primary text-white px-4 py-2 rounded hover:bg-red-600 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">📊 Analytics Dashboard</h1>
          <p className="text-gray-400">System-wide analytics and insights</p>
        </div>

        {/* Overview Stats */}
        {overview && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Users</p>
                  <p className="text-2xl font-bold">{overview.total_users}</p>
                </div>
                <Users className="text-primary" size={24} />
              </div>
            </div>

            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Movies</p>
                  <p className="text-2xl font-bold">{overview.total_movies}</p>
                </div>
                <Film className="text-primary" size={24} />
              </div>
            </div>

            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Ratings</p>
                  <p className="text-2xl font-bold">{overview.total_ratings}</p>
                </div>
                <Star className="text-primary" size={24} />
              </div>
            </div>

            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Avg Rating</p>
                  <p className="text-2xl font-bold">{overview.avg_rating}</p>
                </div>
                <TrendingUp className="text-primary" size={24} />
              </div>
            </div>

            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Engagement</p>
                  <p className="text-2xl font-bold">{overview.engagement_rate}%</p>
                </div>
                <Activity className="text-primary" size={24} />
              </div>
            </div>
          </div>
        )}

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Ratings Distribution */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <BarChart3 size={20} className="text-primary" />
              Rating Distribution
            </h2>
            <div className="space-y-3">
              {ratingsDistribution.map((item) => {
                const maxCount = Math.max(...ratingsDistribution.map((r) => r.count));
                const percentage = (item.count / maxCount) * 100;
                return (
                  <div key={item.rating}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-300">⭐ {item.rating}</span>
                      <span className="text-gray-400">{item.count}</span>
                    </div>
                    <div className="w-full bg-dark rounded h-2">
                      <div
                        className="bg-primary h-2 rounded transition-all"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* User Engagement */}
          {userEngagement && (
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Users size={20} className="text-primary" />
                User Engagement
              </h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-dark rounded">
                  <span>Active Users (30d)</span>
                  <span className="text-primary font-bold">
                    {userEngagement.active_users_30d}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-dark rounded">
                  <span>Super Users</span>
                  <span className="text-green-400 font-bold">
                    {userEngagement.super_users}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-dark rounded">
                  <span>Regular Users</span>
                  <span className="text-yellow-400 font-bold">
                    {userEngagement.engagement_categories.regular}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-dark rounded">
                  <span>Dormant Users</span>
                  <span className="text-gray-400 font-bold">
                    {userEngagement.dormant_users}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Genre Analytics */}
        <div className="bg-darkGray rounded-lg p-6 border border-primary/20 mb-8">
          <h2 className="text-xl font-bold mb-4">Genre Analytics</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-primary/20">
                  <th className="text-left py-3 px-4">Genre</th>
                  <th className="text-left py-3 px-4">Movies</th>
                  <th className="text-left py-3 px-4">Avg Rating</th>
                  <th className="text-left py-3 px-4">Total Ratings</th>
                  <th className="text-left py-3 px-4">Popularity</th>
                </tr>
              </thead>
              <tbody>
                {genreAnalytics.slice(0, 10).map((item) => {
                  const maxRatings = Math.max(...genreAnalytics.map((g) => g.total_ratings));
                  const popularity = (item.total_ratings / maxRatings) * 100;
                  return (
                    <tr
                      key={item.genre}
                      className="border-b border-primary/10 hover:bg-dark transition"
                    >
                      <td className="py-3 px-4 font-semibold">{item.genre}</td>
                      <td className="py-3 px-4">{item.movie_count}</td>
                      <td className="py-3 px-4">
                        <span className="text-yellow-400">★ {item.avg_rating}</span>
                      </td>
                      <td className="py-3 px-4">{item.total_ratings}</td>
                      <td className="py-3 px-4">
                        <div className="w-full bg-dark rounded h-2">
                          <div
                            className="bg-primary h-2 rounded"
                            style={{ width: `${popularity}%` }}
                          />
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Movies Grid */}
        {topMovies && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Top Rated */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-lg font-bold mb-4">Top Rated</h2>
              <div className="space-y-3">
                {topMovies.top_rated?.slice(0, 5).map((movie, idx) => (
                  <div key={idx} className="flex items-start gap-3 pb-3 border-b border-primary/10">
                    <span className="text-primary font-bold text-lg">#{idx + 1}</span>
                    <div className="flex-1">
                      <p className="font-semibold text-sm truncate">{movie.title}</p>
                      <p className="text-xs text-gray-400">{movie.year}</p>
                      <p className="text-yellow-400 font-bold text-sm">★ {movie.rating}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Most Favorited */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                <Heart size={16} className="text-primary" />
                Most Favorited
              </h2>
              <div className="space-y-3">
                {topMovies.most_favorited?.slice(0, 5).map((movie, idx) => (
                  <div key={idx} className="flex items-start gap-3 pb-3 border-b border-primary/10">
                    <span className="text-primary font-bold text-lg">#{idx + 1}</span>
                    <div className="flex-1">
                      <p className="font-semibold text-sm truncate">{movie.title}</p>
                      <p className="text-xs text-gray-400">{movie.favorite_count} favorites</p>
                      <p className="text-yellow-400 text-sm">★ {movie.rating}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Most Rated */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-lg font-bold mb-4">Most Rated</h2>
              <div className="space-y-3">
                {topMovies.most_rated?.slice(0, 5).map((movie, idx) => (
                  <div key={idx} className="flex items-start gap-3 pb-3 border-b border-primary/10">
                    <span className="text-primary font-bold text-lg">#{idx + 1}</span>
                    <div className="flex-1">
                      <p className="font-semibold text-sm truncate">{movie.title}</p>
                      <p className="text-xs text-gray-400">{movie.rating_count} ratings</p>
                      <p className="text-yellow-400 text-sm">★ {movie.avg_rating}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Timeline Chart */}
        {timeline.length > 0 && (
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <LineChart size={20} className="text-primary" />
              Ratings Timeline (Last 30 Days)
            </h2>
            <div className="space-y-3">
              {timeline.map((item) => {
                const maxCount = Math.max(...timeline.map((t) => t.ratings_count));
                const percentage = (item.ratings_count / maxCount) * 100;
                return (
                  <div key={item.date}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-300">{item.date}</span>
                      <span className="text-gray-400">
                        {item.ratings_count} ratings (avg: ★{item.avg_rating})
                      </span>
                    </div>
                    <div className="w-full bg-dark rounded h-2">
                      <div
                        className="bg-primary h-2 rounded transition-all"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalyticsDashboardPage;
