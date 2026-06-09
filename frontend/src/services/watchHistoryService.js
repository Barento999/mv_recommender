import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const watchHistoryService = {
  addToHistory: async (movieId, token) => {
    const response = await api.post(
      `/watch-history/add/${movieId}`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  },

  getWatchHistory: async (skip = 0, limit = 10, token) => {
    const response = await api.get("/watch-history", {
      params: { skip, limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getRecentWatches: async (days = 7, limit = 10, token) => {
    const response = await api.get("/watch-history/recent", {
      params: { days, limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  checkWatched: async (movieId, token) => {
    const response = await api.get(`/watch-history/check/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  removeFromHistory: async (movieId, token) => {
    const response = await api.delete(`/watch-history/remove/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  clearHistory: async (token) => {
    const response = await api.delete("/watch-history/clear", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getStats: async (token) => {
    const response = await api.get("/watch-history/stats/overview", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getMostWatchedGenres: async (limit = 10, token) => {
    const response = await api.get("/watch-history/genres/most-watched", {
      params: { limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default watchHistoryService;
