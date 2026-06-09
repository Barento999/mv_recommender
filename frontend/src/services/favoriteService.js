import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const favoriteService = {
  addFavorite: async (movieId, token) => {
    const response = await api.post(
      `/favorites/add/${movieId}`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  },

  removeFavorite: async (movieId, token) => {
    const response = await api.delete(`/favorites/remove/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getFavorites: async (skip = 0, limit = 10, token, sortBy = "created_at", sortOrder = "desc") => {
    const response = await api.get("/favorites", {
      params: { skip, limit, sort_by: sortBy, sort_order: sortOrder },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  checkFavorite: async (movieId, token) => {
    const response = await api.get(`/favorites/check/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default favoriteService;
