import { useState, useEffect } from "react";
import { Search } from "lucide-react";
import MovieCard from "../components/MovieCard";
import Pagination from "../components/Pagination";
import LoadingSkeleton from "../components/LoadingSkeleton";
import movieService from "../services/movieService";

const GENRES = [
  "Action",
  "Comedy",
  "Drama",
  "Horror",
  "Romance",
  "Sci-Fi",
  "Thriller",
  "Animation",
];

function MoviesPage() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("");
  const [selectedYear, setSelectedYear] = useState("");
  const [sortBy, setSortBy] = useState("rating");
  const [sortOrder, setSortOrder] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const itemsPerPage = 12;

  const loadMovies = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;

      let data;
      if (searchQuery) {
        data = await movieService.searchMovies(searchQuery, skip, itemsPerPage, sortBy, sortOrder);
      } else {
        data = await movieService.getAllMovies(
          skip,
          itemsPerPage,
          selectedGenre || null,
          selectedYear ? parseInt(selectedYear) : null,
          sortBy,
          sortOrder,
        );
      }

      setMovies(data.movies);
      setTotal(data.total);
    } catch (error) {
      console.error("Error loading movies:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery, selectedGenre, selectedYear, sortBy, sortOrder]);

  useEffect(() => {
    loadMovies();
  }, [currentPage, searchQuery, selectedGenre, selectedYear, sortBy, sortOrder]);

  const totalPages = Math.ceil(total / itemsPerPage);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <h1 className="text-4xl font-bold mb-8">Explore Movies</h1>

        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            />
          </div>

          {/* Filters and Sort */}
          <div className="grid md:grid-cols-4 gap-4">
            {/* Genre Filter */}
            <select
              value={selectedGenre}
              onChange={(e) => setSelectedGenre(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="">All Genres</option>
              {GENRES.map((genre) => (
                <option key={genre} value={genre}>
                  {genre}
                </option>
              ))}
            </select>

            {/* Year Filter */}
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="">All Years</option>
              {Array.from(
                { length: 50 },
                (_, i) => new Date().getFullYear() - i,
              ).map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>

            {/* Sort By */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="rating">Sort by Rating</option>
              <option value="year">Sort by Year</option>
              <option value="title">Sort by Title</option>
            </select>

            {/* Sort Order */}
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="px-4 py-3 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none transition"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>

        {/* Results Info */}
        <p className="text-gray-400 mb-8">
          Showing {movies.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0}{" "}
          - {Math.min(currentPage * itemsPerPage, total)} of {total} movies
        </p>

        {/* Movies Grid */}
        {loading ? (
          <LoadingSkeleton count={12} />
        ) : movies.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {movies.map((movie) => (
                <MovieCard
                  key={movie._id}
                  movie={movie}
                  onFavoriteChange={loadMovies}
                />
              ))}
            </div>

            {/* Pagination */}
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
            <p className="text-gray-400 text-lg">No movies found</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MoviesPage;
