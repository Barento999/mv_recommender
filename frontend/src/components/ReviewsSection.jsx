import { useState, useEffect } from "react";
import { MessageSquare, ThumbsUp, Trash2 } from "lucide-react";
import reviewService from "../services/reviewService";
import RatingStars from "./RatingStars";
import useAuth from "../hooks/useAuth";

function ReviewsSection({ movieId, movieTitle }) {
  const { isAuthenticated, token } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [stats, setStats] = useState(null);
  const [userReview, setUserReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [sortBy, setSortBy] = useState("helpful");

  // Form state
  const [formData, setFormData] = useState({
    rating: 8,
    title: "",
    content: "",
  });
  const [formLoading, setFormLoading] = useState(false);
  const [formError, setFormError] = useState("");

  useEffect(() => {
    loadReviews();
    loadStats();
    if (isAuthenticated) {
      loadUserReview();
    }
  }, [movieId, sortBy, isAuthenticated]);

  const loadReviews = async () => {
    try {
      const data = await reviewService.getMovieReviews(movieId, 0, 10, sortBy);
      setReviews(data.reviews || []);
    } catch (error) {
      console.error("Error loading reviews:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await reviewService.getMovieReviewStats(movieId);
      setStats(data.stats);
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  const loadUserReview = async () => {
    try {
      const data = await reviewService.getUserReview(movieId, token);
      if (data.review) {
        setUserReview(data.review);
        setFormData({
          rating: data.review.rating,
          title: data.review.title,
          content: data.review.content,
        });
      }
    } catch (error) {
      console.error("Error loading user review:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    setFormLoading(true);

    try {
      await reviewService.createReview(movieId, formData, token);
      setShowForm(false);
      setFormError("");
      loadReviews();
      loadStats();
      loadUserReview();
    } catch (error) {
      setFormError(error.response?.data?.detail || "Failed to save review");
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Delete this review?")) {
      try {
        await reviewService.deleteReview(movieId, token);
        setUserReview(null);
        setFormData({ rating: 8, title: "", content: "" });
        setShowForm(false);
        loadReviews();
        loadStats();
      } catch (error) {
        console.error("Error deleting review:", error);
      }
    }
  };

  const handleMarkHelpful = async (reviewId) => {
    try {
      await reviewService.markHelpful(reviewId, token);
      loadReviews();
    } catch (error) {
      console.error("Error marking helpful:", error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  };

  return (
    <div className="mt-12 border-t border-primary/20 pt-8">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <MessageSquare size={24} />
        Reviews
      </h2>

      {/* Stats */}
      {stats && (
        <div className="mb-6 grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
            <p className="text-gray-400 text-sm">Total Reviews</p>
            <p className="text-2xl font-bold">{stats.total_reviews}</p>
          </div>
          <div className="bg-darkGray rounded-lg p-4 border border-yellow-500/20">
            <p className="text-gray-400 text-sm">Average Rating</p>
            <p className="text-2xl font-bold text-yellow-500">{stats.average_rating}</p>
          </div>
          <div className="hidden md:block bg-darkGray rounded-lg p-4 border border-primary/20">
            <p className="text-gray-400 text-sm">Your Review</p>
            <p className="text-lg font-bold">{userReview ? "✓ Posted" : "—"}</p>
          </div>
        </div>
      )}

      {/* User's Review Form */}
      {isAuthenticated && (
        <div className="mb-8 bg-darkGray rounded-lg p-6 border border-primary/20">
          {userReview && !showForm ? (
            <>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold mb-2">{userReview.title}</h3>
                  <RatingStars
                    rating={userReview.rating}
                    readOnly
                    size={20}
                  />
                  <p className="text-gray-400 text-sm mt-2">
                    {formatDate(userReview.created_at)}
                    {userReview.updated_at !== userReview.created_at && " (edited)"}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setShowForm(true)}
                    className="px-4 py-2 bg-primary hover:bg-red-600 rounded transition"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded transition"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
              <p className="text-gray-300">{userReview.content}</p>
            </>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <h3 className="text-lg font-bold mb-4">
                {userReview ? "Edit Your Review" : "Write a Review"}
              </h3>

              {formError && (
                <div className="p-3 bg-red-600/20 border border-red-600 rounded text-red-400 text-sm">
                  {formError}
                </div>
              )}

              <div>
                <label className="block text-sm font-semibold mb-2">Rating</label>
                <div className="flex gap-2 items-center">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setFormData({ ...formData, rating: star })}
                      className={`px-3 py-1 rounded transition ${
                        formData.rating >= star
                          ? "bg-yellow-500 text-black"
                          : "bg-darkGray border border-primary/20"
                      }`}
                    >
                      {star}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Summary of your review"
                  maxLength={100}
                  className="w-full bg-dark border border-primary/20 rounded px-4 py-2 focus:border-primary focus:outline-none"
                  required
                />
                <p className="text-xs text-gray-400 mt-1">{formData.title.length}/100</p>
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">Review</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  placeholder="Share your thoughts about this movie..."
                  maxLength={5000}
                  rows={5}
                  className="w-full bg-dark border border-primary/20 rounded px-4 py-2 focus:border-primary focus:outline-none resize-none"
                  required
                />
                <p className="text-xs text-gray-400 mt-1">{formData.content.length}/5000</p>
              </div>

              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={formLoading}
                  className="flex-1 bg-primary hover:bg-red-600 disabled:opacity-50 text-white py-2 rounded font-bold transition"
                >
                  {formLoading ? "Saving..." : userReview ? "Update Review" : "Post Review"}
                </button>
                {showForm && (
                  <button
                    type="button"
                    onClick={() => setShowForm(false)}
                    className="px-6 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded transition"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          )}

          {userReview && !showForm && (
            <button
              onClick={() => setShowForm(true)}
              className="mt-4 text-primary hover:text-red-600 transition"
            >
              Edit your review
            </button>
          )}
        </div>
      )}

      {!isAuthenticated && (
        <div className="mb-8 p-4 bg-primary/10 border border-primary/30 rounded text-center">
          <p className="text-gray-300">
            <a href="/login" className="text-primary hover:text-red-600">
              Login
            </a>
            {" "}to write a review
          </p>
        </div>
      )}

      {/* Reviews List */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold">All Reviews</h3>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-darkGray border border-primary/20 rounded px-3 py-2 focus:border-primary focus:outline-none"
          >
            <option value="helpful">Most Helpful</option>
            <option value="recent">Most Recent</option>
            <option value="rating_high">Highest Rated</option>
            <option value="rating_low">Lowest Rated</option>
          </select>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-400">Loading reviews...</div>
        ) : reviews.length > 0 ? (
          <div className="space-y-4">
            {reviews.map((review) => (
              <div key={review.review_id} className="bg-darkGray rounded-lg p-4 border border-primary/20">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="font-bold text-lg">{review.title}</h4>
                    <p className="text-gray-400 text-sm">
                      {review.user_name} • {formatDate(review.created_at)}
                    </p>
                  </div>
                  <RatingStars rating={review.rating} readOnly size={16} />
                </div>

                <p className="text-gray-300 mb-3">{review.content}</p>

                {isAuthenticated && (
                  <button
                    onClick={() => handleMarkHelpful(review.review_id)}
                    className="flex items-center gap-2 text-gray-400 hover:text-primary transition text-sm"
                  >
                    <ThumbsUp size={16} />
                    Helpful ({review.helpful_count})
                  </button>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-400">
            No reviews yet. Be the first to review!
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewsSection;
