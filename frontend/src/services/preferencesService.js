import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

const preferencesService = {
  /**
   * Get user's preferences
   */
  getPreferences: async (token) => {
    const response = await api.get("/preferences", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  /**
   * Update user's preferences
   */
  updatePreferences: async (preferencesData, token) => {
    const response = await api.put("/preferences", preferencesData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  /**
   * Get available genres
   */
  getAvailableGenres: async () => {
    const response = await api.get("/preferences/genres/available");
    return response.data;
  },

  /**
   * Get preference analysis based on user's activity
   */
  getPreferenceAnalysis: async (token) => {
    const response = await api.get("/preferences/analysis", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default preferencesService;
