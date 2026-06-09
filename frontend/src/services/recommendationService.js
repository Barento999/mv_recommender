import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const recommendationService = {
  getRecommendations: async (limit = 10, token) => {
    const response = await api.get("/recommendations", {
      params: { limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getRecommendationsWithExplanations: async (limit = 10, token, sortBy = "rating", sortOrder = "desc") => {
    const response = await api.get("/recommendations/explained", {
      params: { limit, sort_by: sortBy, sort_order: sortOrder },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getMovieExplanation: async (movieId, token) => {
    const response = await api.get(`/recommendations/explanation/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getSimilarMovies: async (movieId, limit = 5) => {
    const response = await api.get(`/recommendations/similar/${movieId}`, {
      params: { limit },
    });
    return response.data;
  },
};

export default recommendationService;
