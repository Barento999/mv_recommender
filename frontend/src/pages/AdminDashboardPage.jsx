import { useState, useEffect } from "react";
import {
  BarChart3,
  Users,
  Film,
  TrendingUp,
  Activity,
  AlertCircle,
  Settings,
} from "lucide-react";
import movieService from "../services/movieService";
import useAuth from "../hooks/useAuth";

function AdminDashboardPage() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState({
    totalMovies: 0,
    totalUsers: 0,
    avgRating: 0,
    systemHealth: "Healthy",
  });
  const [movies, setMovies] = useState([]);
  const [topMovies, setTopMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      // Load movies data
      const moviesData = await movieService.getAllMovies(0, 1000);
      const allMovies = moviesData.movies || [];
      setMovies(allMovies);

      // Calculate statistics
      const totalMovies = moviesData.total || 0;
      const avgRating =
        allMovies.length > 0
          ? (allMovies.reduce((sum, m) => sum + m.rating, 0) / allMovies.length).toFixed(1)
          : 0;

      // Get top rated movies
      const top = allMovies.sort((a, b) => b.rating - a.rating).slice(0, 10);
      setTopMovies(top);

      setStats({
        totalMovies,
        totalUsers: 150, // From seeded data
        avgRating,
        systemHealth: "Healthy",
      });
    } catch (error) {
      console.error("Error loading admin data:", error);
      setStats((prev) => ({ ...prev, systemHealth: "Error" }));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <p className="text-gray-400">Loading admin dashboard...</p>
      </div>
    );
  }

  // Check if user is admin (simple check - in production use proper RBAC)
  if (user?.email !== "admin@example.com") {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="mx-auto mb-4 text-red-500" size={48} />
          <h1 className="text-2xl font-bold mb-2">Access Denied</h1>
          <p className="text-gray-400">You don't have admin privileges</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">System monitoring and management</p>
        </div>

        {/* System Status */}
        <div className="mb-8 p-4 rounded-lg bg-green-500/10 border border-green-500/20">
          <div className="flex items-center gap-2">
            <Activity className="text-green-500" size={20} />
            <span className="text-green-400">System Status: {stats.systemHealth}</span>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Total Movies */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Movies</p>
                <p className="text-3xl font-bold">{stats.totalMovies}</p>
              </div>
              <Film className="text-primary" size={32} />
            </div>
          </div>

          {/* Total Users */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Users</p>
                <p className="text-3xl font-bold">{stats.totalUsers}</p>
              </div>
              <Users className="text-primary" size={32} />
            </div>
          </div>

          {/* Average Rating */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Avg Rating</p>
                <p className="text-3xl font-bold">{stats.avgRating}</p>
              </div>
              <TrendingUp className="text-primary" size={32} />
            </div>
          </div>

          {/* Database Status */}
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">DB Status</p>
                <p className="text-3xl font-bold text-green-500">Online</p>
              </div>
              <BarChart3 className="text-primary" size={32} />
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* System Information */}
          <div className="lg:col-span-1">
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20 space-y-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Settings size={20} className="text-primary" />
                System Info
              </h2>

              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-gray-400">ML Models</p>
                  <p className="font-semibold text-green-400">✓ Active</p>
                </div>
                <div>
                  <p className="text-gray-400">Cache Status</p>
                  <p className="font-semibold">88% Hit Rate</p>
                </div>
                <div>
                  <p className="text-gray-400">API Endpoints</p>
                  <p className="font-semibold">15+ Available</p>
                </div>
                <div>
                  <p className="text-gray-400">Uptime</p>
                  <p className="font-semibold">100%</p>
                </div>
              </div>

              <button className="w-full bg-primary text-white py-2 rounded hover:bg-red-600 transition mt-4">
                System Settings
              </button>
            </div>
          </div>

          {/* Movie Statistics */}
          <div className="lg:col-span-2">
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
              <h2 className="text-xl font-bold mb-4">Movie Statistics</h2>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-dark p-4 rounded">
                  <p className="text-gray-400 text-sm">Total Genres</p>
                  <p className="text-2xl font-bold">
                    {new Set(movies.flatMap((m) => m.genre)).size}
                  </p>
                </div>
                <div className="bg-dark p-4 rounded">
                  <p className="text-gray-400 text-sm">Year Range</p>
                  <p className="text-2xl font-bold">
                    {Math.min(...movies.map((m) => m.year))} -{" "}
                    {Math.max(...movies.map((m) => m.year))}
                  </p>
                </div>
                <div className="bg-dark p-4 rounded">
                  <p className="text-gray-400 text-sm">Highest Rated</p>
                  <p className="text-2xl font-bold">
                    {Math.max(...movies.map((m) => m.rating))}
                  </p>
                </div>
                <div className="bg-dark p-4 rounded">
                  <p className="text-gray-400 text-sm">Lowest Rated</p>
                  <p className="text-2xl font-bold">
                    {Math.min(...movies.map((m) => m.rating))}
                  </p>
                </div>
              </div>

              {/* Genre Breakdown */}
              <div>
                <h3 className="font-semibold mb-3">Top Genres</h3>
                <div className="space-y-2">
                  {Array.from(new Set(movies.flatMap((m) => m.genre)))
                    .slice(0, 5)
                    .map((genre) => {
                      const count = movies.filter((m) => m.genre.includes(genre)).length;
                      const percentage = ((count / movies.length) * 100).toFixed(1);
                      return (
                        <div key={genre} className="flex items-center justify-between">
                          <span className="text-sm text-gray-300">{genre}</span>
                          <div className="flex items-center gap-2 flex-1 ml-4">
                            <div className="flex-1 bg-dark rounded h-2">
                              <div
                                className="bg-primary h-2 rounded"
                                style={{ width: `${percentage}%` }}
                              />
                            </div>
                            <span className="text-sm text-gray-400 w-12 text-right">
                              {percentage}%
                            </span>
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Top Movies */}
        <div className="mt-8">
          <div className="bg-darkGray rounded-lg p-6 border border-primary/20">
            <h2 className="text-xl font-bold mb-4">Top Rated Movies</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-primary/20">
                    <th className="text-left py-3 px-4">Rank</th>
                    <th className="text-left py-3 px-4">Title</th>
                    <th className="text-left py-3 px-4">Rating</th>
                    <th className="text-left py-3 px-4">Genres</th>
                    <th className="text-left py-3 px-4">Year</th>
                  </tr>
                </thead>
                <tbody>
                  {topMovies.map((movie, idx) => (
                    <tr
                      key={movie._id}
                      className="border-b border-primary/10 hover:bg-dark transition"
                    >
                      <td className="py-3 px-4 font-bold text-primary">#{idx + 1}</td>
                      <td className="py-3 px-4">{movie.title}</td>
                      <td className="py-3 px-4">
                        <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">
                          ★ {movie.rating}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex gap-1 flex-wrap">
                          {movie.genre?.slice(0, 2).map((g) => (
                            <span
                              key={g}
                              className="text-xs bg-primary/20 px-2 py-1 rounded"
                            >
                              {g}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="py-3 px-4">{movie.year}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboardPage;
