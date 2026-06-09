import { useState, useEffect } from "react";
import { Heart } from "lucide-react";
import MovieCard from "../components/MovieCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import Pagination from "../components/Pagination";
import wishlistService from "../services/wishlistService";
import useAuth from "../hooks/useAuth";

function WishlistPage() {
  const { token } = useAuth();
  const [wishlist, setWishlist] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState("desc");
  const [stats, setStats] = useState({
    total: 0,
    low_priority: 0,
    normal_priority: 0,
    high_priority: 0,
  });

  const itemsPerPage = 12;

  const loadWishlist = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await wishlistService.getWishlist(
        skip,
        itemsPerPage,
        token,
        sortBy,
        sortOrder,
      );
      setWishlist(data.wishlist || []);
      setTotal(data.total);
    } catch (error) {
      console.error("Error loading wishlist:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await wishlistService.getWishlistStats(token);
      setStats(data.stats);
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [sortBy, sortOrder]);

  useEffect(() => {
    loadWishlist();
    loadStats();
  }, [currentPage, sortBy, sortOrder]);

  const totalPages = Math.ceil(total / itemsPerPage);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-2">
            <Heart size={40} className="text-primary" />
            My Wishlist
          </h1>
          <p className="text-gray-400">
            {total} wishlist {total === 1 ? "item" : "items"}
          </p>
        </div>

        {/* Stats Bar */}
        {total > 0 && (
          <div className="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <p className="text-gray-400 text-sm">Total Items</p>
              <p className="text-2xl font-bold">{stats.total}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-red-500/20">
              <p className="text-gray-400 text-sm">High Priority</p>
              <p className="text-2xl font-bold text-red-500">{stats.high_priority}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-yellow-500/20">
              <p className="text-gray-400 text-sm">Normal Priority</p>
              <p className="text-2xl font-bold text-yellow-500">{stats.normal_priority}</p>
            </div>
            <div className="bg-darkGray rounded-lg p-4 border border-green-500/20">
              <p className="text-gray-400 text-sm">Low Priority</p>
              <p className="text-2xl font-bold text-green-500">{stats.low_priority}</p>
            </div>
          </div>
        )}

        {/* Sort Options */}
        {total > 0 && (
          <div className="grid md:grid-cols-2 gap-4 mb-8">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="created_at">Sort by Date Added</option>
              <option value="priority">Sort by Priority</option>
              <option value="rating">Sort by Rating</option>
              <option value="year">Sort by Year</option>
              <option value="title">Sort by Title</option>
            </select>

            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        )}

        {/* Wishlist Grid */}
        {loading ? (
          <LoadingSkeleton count={12} />
        ) : wishlist.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {wishlist.map((movie) => (
                <div key={movie._id} className="relative">
                  <MovieCard
                    movie={movie}
                    onFavoriteChange={loadWishlist}
                  />
                  {/* Priority Badge */}
                  <div className={`absolute top-2 right-2 px-2 py-1 rounded text-xs font-bold ${
                    movie.wishlist_priority === "high" ? "bg-red-500" :
                    movie.wishlist_priority === "normal" ? "bg-yellow-500" :
                    "bg-green-500"
                  }`}>
                    {movie.wishlist_priority?.toUpperCase()}
                  </div>
                  {/* Notes Display */}
                  {movie.wishlist_notes && (
                    <div className="mt-2 p-2 bg-darkGray rounded text-xs text-gray-300 border border-primary/20">
                      {movie.wishlist_notes}
                    </div>
                  )}
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
            <Heart size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-400 text-lg">Your wishlist is empty</p>
            <p className="text-gray-500">
              Add movies to your wishlist to save them for later!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default WishlistPage;
