import axios from "axios";
import API_URL from "../config/api";

const api = axios.create({
  baseURL: API_URL,
});

export const userManagementService = {
  listUsers: async (skip = 0, limit = 10, role = null, token) => {
    const params = { skip, limit };
    if (role) params.role = role;

    const response = await api.get("/admin/users", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getUser: async (userId, token) => {
    const response = await api.get(`/admin/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  updateUserRole: async (userId, role, token) => {
    const response = await api.put(
      `/admin/users/${userId}/role`,
      { role },
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return response.data;
  },

  deleteUser: async (userId, token) => {
    const response = await api.delete(`/admin/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getAllRoles: async (token) => {
    const response = await api.get("/admin/users/roles/all", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  getUserStats: async (token) => {
    const response = await api.get("/admin/users/stats/overview", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

export default userManagementService;
