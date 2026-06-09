import { useState, useEffect } from "react";
import { Save, X, Plus, Loader } from "lucide-react";
import useAuth from "../hooks/useAuth";
import preferencesService from "../services/preferencesService";

function UserPreferencesPage() {
  const { token } = useAuth();
  const [preferences, setPreferences] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [availableGenres, setAvailableGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  // Form state
  const [formData, setFormData] = useState({
    favorite_genres: [],
    disliked_genres: [],
    min_rating: 5.0,
    max_year: 2026,
    min_year: 1900,
    language: "en",
    notifications_enabled: true,
    recommendations_frequency: "weekly",
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [prefsData, analysisData, genresData] = await Promise.all([
        preferencesService.getPreferences(token),
        preferencesService.getPreferenceAnalysis(token),
        preferencesService.getAvailableGenres(),
      ]);

      setPreferences(prefsData);
      setAnalysis(analysisData);
      setAvailableGenres(genresData.genres || []);

      setFormData({
        favorite_genres: prefsData.favorite_genres || [],
        disliked_genres: prefsData.disliked_genres || [],
        min_rating: prefsData.min_rating || 5.0,
        max_year: prefsData.max_year || 2026,
        min_year: prefsData.min_year || 1900,
        language: prefsData.language || "en",
        notifications_enabled: prefsData.notifications_enabled ?? true,
        recommendations_frequency: prefsData.recommendations_frequency || "weekly",
      });
    } catch (err) {
      console.error("Error loading preferences:", err);
      setError("Failed to load preferences");
    } finally {
      setLoading(false);
    }
  };

  const handleGenreToggle = (genre, type) => {
    setFormData((prev) => {
      const genres = [...prev[type]];
      const index = genres.indexOf(genre);

      if (index > -1) {
        genres.splice(index, 1);
      } else {
        genres.push(genre);
      }

      return { ...prev, [type]: genres };
    });
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccessMessage("");

    try {
      await preferencesService.updatePreferences(formData, token);
      setSuccessMessage("Preferences saved successfully!");
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      console.error("Error saving preferences:", err);
      setError("Failed to save preferences");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <p className="text-gray-400">Loading preferences...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">⚙️ Your Preferences</h1>
          <p className="text-gray-400">Customize your recommendation experience</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded text-red-400">
            {error}
          </div>
        )}

        {/* Success Message */}
        {successMessage && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/30 rounded text-green-400">
            ✅ {successMessage}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Preferences Form */}
          <div className="lg:col-span-2">
            {/* Genre Preferences */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20 mb-6">
              <h2 className="text-2xl font-bold mb-4">📽️ Genre Preferences</h2>

              {/* Favorite Genres */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-primary mb-3">
                  ❤️ Favorite Genres
                </h3>
                <div className="flex flex-wrap gap-2 mb-3">
                  {formData.favorite_genres.map((genre) => (
                    <button
                      key={genre}
                      onClick={() => handleGenreToggle(genre, "favorite_genres")}
                      className="flex items-center gap-2 bg-primary text-white px-3 py-1 rounded-full text-sm hover:bg-red-600 transition"
                    >
                      {genre}
                      <X size={14} />
                    </button>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  {availableGenres
                    .filter((g) => !formData.favorite_genres.includes(g))
                    .map((genre) => (
                      <button
                        key={genre}
                        onClick={() => handleGenreToggle(genre, "favorite_genres")}
                        className="flex items-center gap-1 bg-gray-700 hover:bg-primary text-white px-3 py-1 rounded-full text-sm transition"
                      >
                        <Plus size={14} />
                        {genre}
                      </button>
                    ))}
                </div>
              </div>

              {/* Disliked Genres */}
              <div>
                <h3 className="text-lg font-semibold text-red-400 mb-3">
                  ❌ Disliked Genres
                </h3>
                <div className="flex flex-wrap gap-2 mb-3">
                  {formData.disliked_genres.map((genre) => (
                    <button
                      key={genre}
                      onClick={() => handleGenreToggle(genre, "disliked_genres")}
                      className="flex items-center gap-2 bg-red-600/40 border border-red-500 text-red-300 px-3 py-1 rounded-full text-sm hover:bg-red-600 transition"
                    >
                      {genre}
                      <X size={14} />
                    </button>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2">
                  {availableGenres
                    .filter(
                      (g) =>
                        !formData.disliked_genres.includes(g) &&
                        !formData.favorite_genres.includes(g)
                    )
                    .map((genre) => (
                      <button
                        key={genre}
                        onClick={() => handleGenreToggle(genre, "disliked_genres")}
                        className="flex items-center gap-1 bg-gray-700 hover:bg-red-600/40 text-white px-3 py-1 rounded-full text-sm transition border border-transparent hover:border-red-500"
                      >
                        <Plus size={14} />
                        {genre}
                      </button>
                    ))}
                </div>
              </div>
            </div>

            {/* Filter Preferences */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20 mb-6">
              <h2 className="text-2xl font-bold mb-4">🎚️ Filter Preferences</h2>

              <div className="space-y-6">
                {/* Min Rating */}
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Minimum Rating: {formData.min_rating.toFixed(1)}/10
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    step="0.5"
                    value={formData.min_rating}
                    onChange={(e) =>
                      setFormData({ ...formData, min_rating: parseFloat(e.target.value) })
                    }
                    className="w-full accent-primary"
                  />
                </div>

                {/* Year Range */}
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Movie Year Range: {formData.min_year} - {formData.max_year}
                  </label>
                  <div className="flex gap-4">
                    <div className="flex-1">
                      <input
                        type="number"
                        min="1900"
                        max="2026"
                        value={formData.min_year}
                        onChange={(e) =>
                          setFormData({ ...formData, min_year: parseInt(e.target.value) })
                        }
                        className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white"
                        placeholder="Min Year"
                      />
                    </div>
                    <div className="flex-1">
                      <input
                        type="number"
                        min="1900"
                        max="2026"
                        value={formData.max_year}
                        onChange={(e) =>
                          setFormData({ ...formData, max_year: parseInt(e.target.value) })
                        }
                        className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white"
                        placeholder="Max Year"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Notification Preferences */}
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20 mb-6">
              <h2 className="text-2xl font-bold mb-4">🔔 Notifications</h2>

              <div className="space-y-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.notifications_enabled}
                    onChange={(e) =>
                      setFormData({ ...formData, notifications_enabled: e.target.checked })
                    }
                    className="w-5 h-5 accent-primary"
                  />
                  <span className="text-white">Enable recommendations notifications</span>
                </label>

                {formData.notifications_enabled && (
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      Recommendation Frequency
                    </label>
                    <select
                      value={formData.recommendations_frequency}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          recommendations_frequency: e.target.value,
                        })
                      }
                      className="w-full bg-dark border border-primary/20 rounded px-3 py-2 text-white"
                    >
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                      <option value="never">Never</option>
                    </select>
                  </div>
                )}
              </div>
            </div>

            {/* Save Button */}
            <button
              onClick={handleSave}
              disabled={saving}
              className="w-full bg-primary hover:bg-red-600 disabled:opacity-50 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition"
            >
              {saving ? (
                <>
                  <Loader size={20} className="animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save size={20} />
                  Save Preferences
                </>
              )}
            </button>
          </div>

          {/* Right Column - Analysis */}
          <div>
            <div className="bg-darkGray rounded-lg p-6 border border-primary/20 sticky top-4">
              <h2 className="text-xl font-bold mb-4">📊 Your Analysis</h2>

              {analysis && (
                <div className="space-y-4">
                  {/* Rating Stats */}
                  <div className="bg-dark p-4 rounded">
                    <p className="text-gray-400 text-sm">Average Rating</p>
                    <p className="text-2xl font-bold text-yellow-400">
                      {analysis.average_rating}/10
                    </p>
                  </div>

                  <div className="bg-dark p-4 rounded">
                    <p className="text-gray-400 text-sm">Total Ratings</p>
                    <p className="text-2xl font-bold text-primary">
                      {analysis.total_ratings}
                    </p>
                  </div>

                  {/* Top Genres */}
                  {analysis.top_genres && analysis.top_genres.length > 0 && (
                    <div className="bg-dark p-4 rounded">
                      <p className="text-gray-400 text-sm font-semibold mb-2">
                        Top Genres
                      </p>
                      <div className="space-y-2">
                        {analysis.top_genres.map((item) => (
                          <div
                            key={item.genre}
                            className="flex justify-between items-center text-xs"
                          >
                            <span className="text-gray-300">{item.genre}</span>
                            <div className="text-right">
                              <p className="text-yellow-400 font-bold">
                                ★ {item.avg_rating}
                              </p>
                              <p className="text-gray-500">{item.count} movies</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Rating Distribution */}
                  {analysis.rating_distribution && (
                    <div className="bg-dark p-4 rounded">
                      <p className="text-gray-400 text-sm font-semibold mb-2">
                        Rating Distribution
                      </p>
                      <div className="space-y-1">
                        {Object.entries(analysis.rating_distribution)
                          .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
                          .map(([rating, count]) => (
                            <div key={rating} className="flex items-center gap-2 text-xs">
                              <span className="w-8 text-yellow-400">★{rating}</span>
                              <div className="flex-1 bg-dark/50 rounded h-2">
                                <div
                                  className="bg-primary h-2 rounded"
                                  style={{
                                    width: `${(count / Math.max(...Object.values(analysis.rating_distribution))) * 100}%`,
                                  }}
                                />
                              </div>
                              <span className="w-6 text-right text-gray-400">
                                {count}
                              </span>
                            </div>
                          ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {!analysis && (
                <p className="text-gray-400 text-sm">
                  Start rating movies to see your preferences analysis!
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserPreferencesPage;
