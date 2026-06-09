import { useState, useEffect } from "react";
import { Users, Trash2, Shield } from "lucide-react";
import userManagementService from "../services/userManagementService";
import LoadingSkeleton from "../components/LoadingSkeleton";
import Pagination from "../components/Pagination";
import useAuth from "../hooks/useAuth";

function UserManagementPage() {
  const { token, user } = useAuth();
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState("");
  const [roles, setRoles] = useState({});
  const [selectedRole, setSelectedRole] = useState({});

  const itemsPerPage = 10;

  useEffect(() => {
    if (user?.role !== "admin") {
      window.location.href = "/";
      return;
    }
    loadUsers();
    loadStats();
    loadRoles();
  }, [currentPage, roleFilter]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const data = await userManagementService.listUsers(
        skip,
        itemsPerPage,
        roleFilter || null,
        token,
      );
      setUsers(data.users || []);
      setTotal(data.total);
    } catch (error) {
      console.error("Error loading users:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await userManagementService.getUserStats(token);
      setStats(data.stats);
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  const loadRoles = async () => {
    try {
      const data = await userManagementService.getAllRoles(token);
      setRoles(data.roles || {});
    } catch (error) {
      console.error("Error loading roles:", error);
    }
  };

  const handleUpdateRole = async (userId, newRole) => {
    try {
      await userManagementService.updateUserRole(userId, newRole, token);
      alert("User role updated");
      loadUsers();
      loadStats();
    } catch (error) {
      alert("Error updating role: " + error.response?.data?.detail);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm("Are you sure? This action cannot be undone.")) {
      try {
        await userManagementService.deleteUser(userId, token);
        alert("User deleted");
        loadUsers();
        loadStats();
      } catch (error) {
        alert("Error deleting user: " + error.response?.data?.detail);
      }
    }
  };

  const totalPages = Math.ceil(total / itemsPerPage);
  const roleEntries = Object.entries(roles);

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-8 flex items-center gap-2">
          <Users size={40} className="text-primary" />
          User Management
        </h1>

        {/* Stats */}
        {stats && (
          <div className="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-darkGray rounded-lg p-4 border border-primary/20">
              <p className="text-gray-400 text-sm">Total Users</p>
              <p className="text-2xl font-bold">{stats.total_users}</p>
            </div>
            {Object.entries(stats.by_role || {}).map(([role, count]) => (
              <div
                key={role}
                className="bg-darkGray rounded-lg p-4 border border-primary/20"
              >
                <p className="text-gray-400 text-sm capitalize">{role}s</p>
                <p className="text-2xl font-bold">{count}</p>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="mb-8 flex gap-4">
          <select
            value={roleFilter}
            onChange={(e) => {
              setRoleFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="px-4 py-2 rounded-lg bg-darkGray border border-primary/20 focus:border-primary focus:outline-none"
          >
            <option value="">All Roles</option>
            {roleEntries.map(([role]) => (
              <option key={role} value={role}>
                {role.charAt(0).toUpperCase() + role.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Users Table */}
        {loading ? (
          <LoadingSkeleton count={5} />
        ) : users.length > 0 ? (
          <>
            <div className="bg-darkGray rounded-lg border border-primary/20 overflow-hidden mb-8">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-primary/20 bg-dark/50">
                      <th className="px-6 py-4 text-left text-sm font-semibold">Name</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold">Email</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold">Role</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold">Permissions</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u.user_id} className="border-b border-primary/20 hover:bg-dark/50 transition">
                        <td className="px-6 py-4">{u.name}</td>
                        <td className="px-6 py-4 text-gray-400">{u.email}</td>
                        <td className="px-6 py-4">
                          <select
                            value={u.role}
                            onChange={(e) => handleUpdateRole(u.user_id, e.target.value)}
                            className="px-3 py-1 rounded bg-dark border border-primary/20 text-sm"
                          >
                            {roleEntries.map(([role]) => (
                              <option key={role} value={role}>
                                {role.charAt(0).toUpperCase() + role.slice(1)}
                              </option>
                            ))}
                          </select>
                        </td>
                        <td className="px-6 py-4">
                          <button
                            onClick={() => alert(u.permissions.join(", "))}
                            className="text-primary hover:text-red-600 transition text-sm flex items-center gap-1"
                          >
                            <Shield size={14} />
                            {u.permissions.length}
                          </button>
                        </td>
                        <td className="px-6 py-4">
                          {u.user_id !== user?._id && (
                            <button
                              onClick={() => handleDeleteUser(u.user_id)}
                              className="text-red-600 hover:text-red-700 transition"
                            >
                              <Trash2 size={18} />
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            )}
          </>
        ) : (
          <div className="text-center py-12 text-gray-400">No users found</div>
        )}

        {/* Role Information */}
        <div className="mt-12 border-t border-primary/20 pt-8">
          <h2 className="text-2xl font-bold mb-6">Role Permissions</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {roleEntries.map(([role, data]) => (
              <div
                key={role}
                className="bg-darkGray rounded-lg p-6 border border-primary/20"
              >
                <h3 className="text-lg font-bold mb-2 capitalize">{role}</h3>
                <p className="text-gray-400 text-sm mb-4">{data.description}</p>
                <div className="space-y-1">
                  {data.permissions.slice(0, 5).map((perm) => (
                    <p key={perm} className="text-xs text-gray-300">
                      ✓ {perm}
                    </p>
                  ))}
                  {data.permissions.length > 5 && (
                    <p className="text-xs text-gray-400 mt-2">
                      +{data.permissions.length - 5} more permissions
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserManagementPage;
