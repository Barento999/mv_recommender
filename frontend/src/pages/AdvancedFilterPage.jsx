import { useState, useEffect } from "react";
import { Search, Filter, X, Loader } from "lucide-react";
import MovieCard from "../components/MovieCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import advancedFilterService from "../services/advancedFilterService";

function AdvancedFilterPage() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [metadata, setMetadata] = useState(null);
  const [totalResults, setTotalResults] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);

  // Filter state
  const [filters, setFilters] = useState({
    query: "",
    genres: [],
    min_rating: 0,
    max_rating: 10,
    min_year: 1900,
    max_year: 2026,
    sort_by: "rating",
    sort_order: "desc",
    limit: 20,
  });

  const [showFilters, setShowFilters] = useState(true);

  // Load metadata on mount
  useEffect(() => {
    loadMetadata();
  }, []);

  const loadMetadata = async () => {
    try {
      const data = await advancedFilterService.getMetadata();
      setMetadata(data);
      if (data.year_range) {
        setFilters((prev) => ({
          ...prev,
          min_year: data.year_range.min,
          max_year: data.year_range.max,
        }));
      }
    } catch (err) {
      console.error("Error loading filter metadata:", err);
    }
  };

  const performSearch = async (pageNum = 1) => {
    setLoading(true);
    try {
      const skip = (pageNum - 1) * filters.limit;
      const results = await advancedFilterService.search({
        ...filters,
        skip,
      });

      setMovies(results.movies || []);
      setTotalResults(results.total || 0);
      setCurrentPage(pageNum);
    } catch (err) {
      console.error("Error performing search:", err);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    setCurrentPage(1);
    performSearch(1);
  };

  const handleGenreToggle = (genre) => {
    setFilters((prev) => {
      const genres = [...prev.genres];
      const index = genres.indexOf(genre);
      if (index > -1) {
        genres.splice(index, 1);
      } else {
        genres.push(genre);
      }
      return { ...prev, genres };
    });
  };

  const handleReset = () => {
    setFilters({
      query: "",
      genres: [],
      min_rating: 0,
      max_rating: 10,
      min_year: metadata?.year_range?.min || 1900,
      max_year: metadata?.year_range?.max || 2026,
      sort_by: "rating",
      sort_order: "desc",
      limit: 20,
    });
    setMovies([]);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(totalResults / filters.limit);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🔍 Advanced Movie Search</h1>
          <p className="text-gray-400">Find movies with detailed filtering</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div
              className={`bg-darkGray rounded-lg border border-primary/20 p-6 ${
                !showFilters && "hidden md:block"
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold flex items-center gap-2">
                  <Filter size={20} />
                  Filters
                </h2>
                <button
                  onClick={() => setShowFilters(false)}
                  className="md:hidden text-gray-400 hover:text-primary"
                >
                  <X size={20} />
                </button>
              </div>

              <div className="space-y-6">
                {/* Text Search */}
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Search Title/Description
                  </label>
                  <input
                    type="text"
                    placeholder="Enter keywords..."
                    value={filters.query}
                    onChange={(e) =>
                      setFilters({ ...filters, query: e.target.value })
                    }
                    className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white placeholder-gray-500"
                  />
                </div>

                {/* Genres */}
                {metadata && (
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Genres ({filters.genres.length} selected)
                    </label>
                    <div className="max-h-48 overflow-y-auto space-y-2">
                      {metadata.genres?.map((genre) => (
                        <label key={genre} className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={filters.genres.includes(genre)}
                            onChange={() => handleGenreToggle(genre)}
                            className="w-4 h-4 accent-primary"
                          />
                          <span className="text-sm text-gray-300">{genre}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}

                {/* Rating Range */}
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Rating: {filters.min_rating.toFixed(1)} - {filters.max_rating.toFixed(1)}
                  </label>
                  <div className="space-y-2">
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.5"
                      value={filters.min_rating}
                      onChange={(e) =>
                        setFilters({
                          ...filters,
                          min_rating: Math.min(parseFloat(e.target.value), filters.max_rating),
                        })
                      }
                      className="w-full accent-primary"
                    />
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.5"
                      value={filters.max_rating}
                      onChange={(e) =>
                        setFilters({
                          ...filters,
                          max_rating: Math.max(parseFloat(e.target.value), filters.min_rating),
                        })
                      }
                      className="w-full accent-primary"
                    />
                  </div>
                </div>

                {/* Year Range */}
                {metadata && (
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Year: {filters.min_year} - {filters.max_year}
                    </label>
                    <div className="space-y-2">
                      <input
                        type="range"
                        min={metadata.year_range?.min || 1900}
                        max={metadata.year_range?.max || 2026}
                        value={filters.min_year}
                        onChange={(e) =>
                          setFilters({
                            ...filters,
                            min_year: Math.min(parseInt(e.target.value), filters.max_year),
                          })
                        }
                        className="w-full accent-primary"
                      />
                      <input
                        type="range"
                        min={metadata.year_range?.min || 1900}
                        max={metadata.year_range?.max || 2026}
                        value={filters.max_year}
                        onChange={(e) =>
                          setFilters({
                            ...filters,
                            max_year: Math.max(parseInt(e.target.value), filters.min_year),
                          })
                        }
                        className="w-full accent-primary"
                      />
                    </div>
                  </div>
                )}

                {/* Sort */}
                <div>
                  <label className="block text-sm font-semibold mb-2">Sort By</label>
                  <div className="space-y-2">
                    <select
                      value={filters.sort_by}
                      onChange={(e) =>
                        setFilters({ ...filters, sort_by: e.target.value })
                      }
                      className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white"
                    >
                      <option value="rating">Rating</option>
                      <option value="year">Year</option>
                      <option value="title">Title</option>
                    </select>

                    <select
                      value={filters.sort_order}
                      onChange={(e) =>
                        setFilters({ ...filters, sort_order: e.target.value })
                      }
                      className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white"
                    >
                      <option value="desc">Descending</option>
                      <option value="asc">Ascending</option>
                    </select>
                  </div>
                </div>

                {/* Buttons */}
                <div className="space-y-2 pt-4 border-t border-primary/20">
                  <button
                    onClick={handleSearch}
                    className="w-full bg-primary hover:bg-red-600 text-white py-2 rounded font-bold flex items-center justify-center gap-2 transition"
                  >
                    <Search size={18} />
                    Search
                  </button>
                  <button
                    onClick={handleReset}
                    className="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 rounded font-bold transition"
                  >
                    Reset
                  </button>
                </div>
              </div>
            </div>

            {/* Toggle button for mobile */}
            {!showFilters && (
              <button
                onClick={() => setShowFilters(true)}
                className="md:hidden w-full bg-primary hover:bg-red-600 text-white py-2 rounded font-bold mb-4 flex items-center justify-center gap-2"
              >
                <Filter size={18} />
                Show Filters
              </button>
            )}
          </div>

          {/* Results */}
          <div className="lg:col-span-3">
            {/* Results Header */}
            <div className="mb-6 flex justify-between items-center">
              <h2 className="text-2xl font-bold">
                {totalResults > 0
                  ? `${totalResults} Movie${totalResults !== 1 ? "s" : ""} Found`
                  : "No movies found"}
              </h2>
              {movies.length > 0 && (
                <p className="text-gray-400 text-sm">
                  Page {currentPage} of {totalPages}
                </p>
              )}
            </div>

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
                      onFavoriteChange={() => {}}
                    />
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex justify-center gap-2 mt-8">
                    <button
                      onClick={() => performSearch(Math.max(1, currentPage - 1))}
                      disabled={currentPage === 1}
                      className="bg-primary disabled:opacity-50 hover:bg-red-600 text-white px-4 py-2 rounded transition"
                    >
                      Previous
                    </button>

                    <div className="flex items-center gap-2">
                      {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                        let pageNum;
                        if (totalPages <= 5) {
                          pageNum = i + 1;
                        } else if (currentPage <= 3) {
                          pageNum = i + 1;
                        } else if (currentPage >= totalPages - 2) {
                          pageNum = totalPages - 4 + i;
                        } else {
                          pageNum = currentPage - 2 + i;
                        }
                        return (
                          <button
                            key={pageNum}
                            onClick={() => performSearch(pageNum)}
                            className={`px-3 py-2 rounded transition ${
                              currentPage === pageNum
                                ? "bg-primary text-white"
                                : "bg-gray-700 hover:bg-gray-600 text-white"
                            }`}
                          >
                            {pageNum}
                          </button>
                        );
                      })}
                    </div>

                    <button
                      onClick={() => performSearch(Math.min(totalPages, currentPage + 1))}
                      disabled={currentPage === totalPages}
                      className="bg-primary disabled:opacity-50 hover:bg-red-600 text-white px-4 py-2 rounded transition"
                    >
                      Next
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-400 text-lg mb-4">No movies match your filters</p>
                <button
                  onClick={handleReset}
                  className="bg-primary hover:bg-red-600 text-white px-6 py-2 rounded font-bold transition"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdvancedFilterPage;
