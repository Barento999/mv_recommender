import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const reviewService = {
  createReview: async (movieId, reviewData, token) => {
    const response = await api.post(`/reviews/movie/${movieId}`, reviewData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getMovieReviews: async (movieId, skip = 0, limit = 10, sortBy = "helpful") => {
    const response = await api.get(`/reviews/movie/${movieId}`, {
      params: { skip, limit, sort_by: sortBy },
    });
    return response.data;
  },

  getMovieReviewStats: async (movieId) => {
    const response = await api.get(`/reviews/movie/${movieId}/stats`);
    return response.data;
  },

  getUserReview: async (movieId, token) => {
    const response = await api.get(`/reviews/movie/${movieId}/user-review`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  deleteReview: async (movieId, token) => {
    const response = await api.delete(`/reviews/movie/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  markHelpful: async (reviewId, token) => {
    const response = await api.post(
      `/reviews/${reviewId}/helpful`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  },

  getMyReviews: async (limit = 10, token) => {
    const response = await api.get("/reviews/user/my-reviews", {
      params: { limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default reviewService;
