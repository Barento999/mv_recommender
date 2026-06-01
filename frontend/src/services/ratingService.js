import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const ratingService = {
  addRating: async (movieId, rating, token) => {
    const response = await api.post(
      "/ratings/add",
      { movie_id: movieId, rating },
      { headers: { Authorization: `Bearer ${token}` } },
    );
    return response.data;
  },

  getUserRatings: async (token) => {
    const response = await api.get("/ratings", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getMovieRating: async (movieId, token) => {
    const response = await api.get(`/ratings/${movieId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default ratingService;
