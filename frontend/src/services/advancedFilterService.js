import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

const advancedFilterService = {
  /**
   * Advanced movie search with filters
   */
  search: async (filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.query) params.append("query", filters.query);
    if (filters.genres && filters.genres.length > 0) {
      params.append("genres", filters.genres.join(","));
    }
    if (filters.min_rating !== undefined) params.append("min_rating", filters.min_rating);
    if (filters.max_rating !== undefined) params.append("max_rating", filters.max_rating);
    if (filters.min_year !== undefined) params.append("min_year", filters.min_year);
    if (filters.max_year !== undefined) params.append("max_year", filters.max_year);
    if (filters.sort_by) params.append("sort_by", filters.sort_by);
    if (filters.sort_order) params.append("sort_order", filters.sort_order);
    if (filters.skip !== undefined) params.append("skip", filters.skip);
    if (filters.limit !== undefined) params.append("limit", filters.limit);
    
    const response = await api.get(`/movies/search/advanced?${params.toString()}`);
    return response.data;
  },

  /**
   * Get filter metadata (genres, year range, rating range)
   */
  getMetadata: async () => {
    const response = await api.get("/movies/filters/metadata");
    return response.data;
  },
};

export default advancedFilterService;
