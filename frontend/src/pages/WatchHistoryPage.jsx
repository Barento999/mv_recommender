import { useState, useEffect } from "react";
import { Clock, Trash2 } from "lucide-react";
import MovieCard from "../components/MovieCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import Pagination from "../components/Pagination";
import watchHistoryService from "../services/watchHistoryService";
import useAuth from "../hooks/useAuth";

function WatchHistoryPage() {
  const { token } = useAuth();
  const [history, setHistory] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    today: 0,
    this_week: 0,
    this_month: 0,
  });
  const [topGenres, setTopGenres] = useState({});

  const itemsPerPage = 12;

  const loadWatchHistory = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await watchHistoryService.getWatchHistory(
        skip,
        itemsPerPage,
        token,
      );
      setHistory(data.history || []);
      setTotal(data.total);
    } catch (error) {
      console.error("Error loading watch history:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await watchHistoryService.getStats(token);
      setStats(statsData.stats);

      const genresData = await watchHistoryService.getMostWatchedGenres(5, token);
      setTopGenres(genresData.genres);
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm("Are you sure you want to clear all watch history?")) {
      try {
        await watchHistoryService.clearHistory(token);
        setHistory([]);
        setTotal(0);
        loadStats();
      } catch (error) {
        console.error("Error clearing history:", error);
        alert("Failed to clear history");
      }
    }
  };

  useEffect(() => {
    loadWatchHistory();
    loadStats();
  }, [currentPage]);

  const totalPages = Math.ceil(total / itemsPerPage);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
    } else if (date.toDateString() === yesterday.toDateString()) {
      return "Yesterday";
    } else {
      return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    }
  };

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-2">
            <Clock size={40} className="text-primary" />
            Watch History
          </h1>
          <p className="text-gray-400">
            {total} {total === 1 ? "movie" : "movies"} watched
          </p>
        </div>

        {/* Stats Bar */}
        {total > 0 && (
          <div className="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <p className="text-gray-400 text-sm">Total Watched</p>
              <p className="text-2xl font-bold">{stats.total}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-blue-500/20">
              <p className="text-gray-400 text-sm">Today</p>
              <p className="text-2xl font-bold text-blue-500">{stats.today}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-green-500/20">
              <p className="text-gray-400 text-sm">This Week</p>
              <p className="text-2xl font-bold text-green-500">{stats.this_week}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-purple-500/20">
              <p className="text-gray-400 text-sm">This Month</p>
              <p className="text-2xl font-bold text-purple-500">{stats.this_month}</p>
            </div>
          </div>
        )}

        {/* Top Genres */}
        {Object.keys(topGenres).length > 0 && (
          <div className="mb-8 bg-darkGray rounded-lg p-6 border border-primary/20">
            <h2 className="text-xl font-bold mb-4">Most Watched Genres</h2>
            <div className="flex flex-wrap gap-3">
              {Object.entries(topGenres).map(([genre, count]) => (
                <div
                  key={genre}
                  className="bg-primary/20 border border-primary/40 rounded-full px-4 py-2"
                >
                  <p className="text-sm">
                    <span className="font-semibold">{genre}</span>
                    <span className="text-gray-400 ml-2">({count})</span>
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Clear History Button */}
        {total > 0 && (
          <div className="mb-8">
            <button
              onClick={handleClearHistory}
              className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded font-bold transition"
            >
              <Trash2 size={18} />
              Clear All History
            </button>
          </div>
        )}

        {/* Watch History Grid */}
        {loading ? (
          <LoadingSkeleton count={12} />
        ) : history.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {history.map((movie) => (
                <div key={movie._id} className="relative">
                  <MovieCard
                    movie={movie}
                    onFavoriteChange={loadWatchHistory}
                  />
                  {/* Watched Date Badge */}
                  <div className="absolute top-2 left-2 bg-black/70 px-2 py-1 rounded text-xs font-bold">
                    {formatDate(movie.watched_at)}
                  </div>
                </div>
              ))}
            </div>

            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <Clock size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-400 text-lg">Your watch history is empty</p>
            <p className="text-gray-500">
              Start watching movies to build your history!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default WatchHistoryPage;
