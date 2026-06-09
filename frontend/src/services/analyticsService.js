import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const getAuthToken = () => localStorage.getItem("token");

const getHeaders = () => ({
  headers: {
    Authorization: `Bearer ${getAuthToken()}`,
  },
});

const analyticsService = {
  /**
   * Get overall analytics overview
   */
  getOverview: async () => {
    const response = await axios.get(`${API_URL}/analytics/overview`, getHeaders());
    return response.data;
  },

  /**
   * Get ratings distribution (1-10)
   */
  getRatingsDistribution: async () => {
    const response = await axios.get(`${API_URL}/analytics/ratings-distribution`, getHeaders());
    return response.data;
  },

  /**
   * Get genre analytics
   */
  getGenreAnalytics: async () => {
    const response = await axios.get(`${API_URL}/analytics/genre-analytics`, getHeaders());
    return response.data;
  },

  /**
   * Get user engagement metrics
   */
  getUserEngagement: async () => {
    const response = await axios.get(`${API_URL}/analytics/user-engagement`, getHeaders());
    return response.data;
  },

  /**
   * Get top movies by various metrics
   */
  getTopMoviesAnalytics: async () => {
    const response = await axios.get(`${API_URL}/analytics/top-movies-analytics`, getHeaders());
    return response.data;
  },

  /**
   * Get timeline stats (last 30 days)
   */
  getTimelineStats: async () => {
    const response = await axios.get(`${API_URL}/analytics/timeline-stats`, getHeaders());
    return response.data;
  },
};

export default analyticsService;
