import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LogOut, User, Mail, Calendar } from "lucide-react";
import useAuth from "../hooks/useAuth";

function ProfilePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const formattedDate = new Date(user?.created_at).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="min-h-screen bg-dark">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-8">Profile</h1>

        <div className="bg-darkGray rounded-lg p-8 border border-primary/20">
          {/* User Info */}
          <div className="space-y-6 mb-8">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                <User size={32} />
              </div>
              <div>
                <h2 className="text-2xl font-bold">{user?.name}</h2>
                <p className="text-gray-400">Member</p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6 pt-6 border-t border-primary/20">
              {/* Email */}
              <div>
                <div className="flex items-center gap-2 text-gray-400 mb-2">
                  <Mail size={18} />
                  <span>Email</span>
                </div>
                <p className="text-lg">{user?.email}</p>
              </div>

              {/* Member Since */}
              <div>
                <div className="flex items-center gap-2 text-gray-400 mb-2">
                  <Calendar size={18} />
                  <span>Member Since</span>
                </div>
                <p className="text-lg">{formattedDate}</p>
              </div>
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="w-full bg-primary hover:bg-red-600 py-3 rounded-lg font-semibold transition flex items-center justify-center gap-2"
          >
            <LogOut size={20} />
            Logout
          </button>
        </div>

        {/* Quick Links */}
        <div className="mt-12 grid md:grid-cols-2 gap-6">
          <a
            href="/favorites"
            className="bg-darkGray rounded-lg p-6 border border-primary/20 hover:border-primary transition cursor-pointer"
          >
            <h3 className="text-xl font-bold mb-2">My Favorites</h3>
            <p className="text-gray-400">View all your favorite movies</p>
          </a>

          <a
            href="/recommendations"
            className="bg-darkGray rounded-lg p-6 border border-primary/20 hover:border-primary transition cursor-pointer"
          >
            <h3 className="text-xl font-bold mb-2">Recommendations</h3>
            <p className="text-gray-400">
              Get personalized movie recommendations
            </p>
          </a>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
