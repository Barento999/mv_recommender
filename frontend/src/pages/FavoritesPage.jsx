import { useState, useEffect } from "react";
import MovieCard from "../components/MovieCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import Pagination from "../components/Pagination";
import favoriteService from "../services/favoriteService";
import useAuth from "../hooks/useAuth";

function FavoritesPage() {
  const { token } = useAuth();
  const [favorites, setFavorites] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState("desc");

  const itemsPerPage = 12;

  const loadFavorites = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await favoriteService.getFavorites(
        skip,
        itemsPerPage,
        token,
        sortBy,
        sortOrder,
      );
      setFavorites(data.favorites || []);
      setTotal(data.total);
    } catch (error) {
      console.error("Error loading favorites:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [sortBy, sortOrder]);

  useEffect(() => {
    loadFavorites();
  }, [currentPage, sortBy, sortOrder]);

  const totalPages = Math.ceil(total / itemsPerPage);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">My Favorites</h1>
        <p className="text-gray-400 mb-8">
          {total} favorite {total === 1 ? "movie" : "movies"}
        </p>

        {/* Sort Options */}
        {total > 0 && (
          <div className="grid md:grid-cols-2 gap-4 mb-8">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="created_at">Sort by Date Added</option>
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

        {loading ? (
          <LoadingSkeleton count={12} />
        ) : favorites.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {favorites.map((movie) => (
                <MovieCard
                  key={movie._id}
                  movie={movie}
                  onFavoriteChange={loadFavorites}
                />
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
            <p className="text-gray-400 text-lg">No favorites yet</p>
            <p className="text-gray-500">
              Add movies to your favorites to see them here!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default FavoritesPage;
