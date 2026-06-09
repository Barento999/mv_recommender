import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const wishlistService = {
  addToWishlist: async (movieId, token, priority = "normal", notes = "") => {
    const response = await api.post(
      `/wishlist/add/${movieId}`,
      {},
      {
        params: { priority, notes },
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  },

  removeFromWishlist: async (movieId, token) => {
    const response = await api.delete(`/wishlist/remove/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getWishlist: async (skip = 0, limit = 10, token, sortBy = "created_at", sortOrder = "desc") => {
    const response = await api.get("/wishlist", {
      params: { skip, limit, sort_by: sortBy, sort_order: sortOrder },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  checkWishlist: async (movieId, token) => {
    const response = await api.get(`/wishlist/check/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  updateWishlistItem: async (movieId, token, priority = null, notes = null) => {
    const params = {};
    if (priority) params.priority = priority;
    if (notes) params.notes = notes;

    const response = await api.put(`/wishlist/update/${movieId}`, {}, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getWishlistByPriority: async (priority, token) => {
    const response = await api.get(`/wishlist/priority/${priority}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getWishlistStats: async (token) => {
    const response = await api.get("/wishlist/stats/overview", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getWishlistCount: async (token) => {
    const response = await api.get("/wishlist/count/total", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default wishlistService;
