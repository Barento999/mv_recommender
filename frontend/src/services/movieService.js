import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const movieService = {
  getAllMovies: async (skip = 0, limit = 10, genre = null, year = null) => {
    const params = { skip, limit };
    if (genre) params.genre = genre;
    if (year) params.year = year;
    const response = await api.get("/movies", { params });
    return response.data;
  },

  searchMovies: async (query, skip = 0, limit = 10) => {
    const response = await api.get("/movies/search", {
      params: { q: query, skip, limit },
    });
    return response.data;
  },

  getMovieById: async (movieId) => {
    const response = await api.get(`/movies/${movieId}`);
    return response.data;
  },

  createMovie: async (movieData, token) => {
    const response = await api.post("/movies", movieData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  updateMovie: async (movieId, movieData, token) => {
    const response = await api.put(`/movies/${movieId}`, movieData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  deleteMovie: async (movieId, token) => {
    const response = await api.delete(`/movies/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getMoviesByRating: async (minRating, skip = 0, limit = 10) => {
    const response = await api.get("/movies", {
      params: { min_rating: minRating, skip, limit },
    });
    return response.data;
  },
};

export default movieService;
