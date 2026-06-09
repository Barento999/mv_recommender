import { Link, useNavigate } from "react-router-dom";
import { Menu, X, LogOut, User, ChevronDown } from "lucide-react";
import { useState } from "react";
import useAuth from "../hooks/useAuth";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
    setIsOpen(false);
  };

  return (
    <nav className="bg-darkGray border-b border-primary sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-primary">🎬</span>
            <span className="text-xl font-bold hidden sm:inline">
              MovieReco
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <Link to="/movies" className="hover:text-primary transition">
              Movies
            </Link>
            <Link to="/search" className="hover:text-primary transition">
              Search
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  to="/recommendations"
                  className="hover:text-primary transition"
                >
                  Recommendations
                </Link>
                <Link to="/favorites" className="hover:text-primary transition">
                  Favorites
                </Link>
                <Link to="/wishlist" className="hover:text-primary transition">
                  Wishlist
                </Link>

                {/* More Menu Dropdown */}
                <div className="relative">
                  <button
                    onClick={() => setDropdownOpen(!dropdownOpen)}
                    className="flex items-center gap-1 hover:text-primary transition"
                  >
                    More <ChevronDown size={16} />
                  </button>
                  {dropdownOpen && (
                    <div className="absolute top-full right-0 mt-2 w-48 bg-darkGray border border-primary/20 rounded-lg shadow-lg z-50">
                      <Link
                        to="/watch-history"
                        className="block px-4 py-2 hover:bg-dark hover:text-primary transition first:rounded-t-lg"
                        onClick={() => setDropdownOpen(false)}
                      >
                        Watch History
                      </Link>
                      <Link
                        to="/user-dashboard"
                        className="block px-4 py-2 hover:bg-dark hover:text-primary transition"
                        onClick={() => setDropdownOpen(false)}
                      >
                        Dashboard
                      </Link>
                      <Link
                        to="/preferences"
                        className="block px-4 py-2 hover:bg-dark hover:text-primary transition"
                        onClick={() => setDropdownOpen(false)}
                      >
                        Preferences
                      </Link>
                      {user?.role === "moderator" && (
                        <Link
                          to="/moderation"
                          className="block px-4 py-2 hover:bg-dark text-yellow-400 font-bold transition"
                          onClick={() => setDropdownOpen(false)}
                        >
                          🛡️ Moderation
                        </Link>
                      )}
                      {user?.role === "admin" && (
                        <>
                          <Link
                            to="/analytics"
                            className="block px-4 py-2 hover:bg-dark hover:text-primary transition"
                            onClick={() => setDropdownOpen(false)}
                          >
                            Analytics
                          </Link>
                          <Link
                            to="/admin-dashboard"
                            className="block px-4 py-2 hover:bg-dark hover:text-primary transition"
                            onClick={() => setDropdownOpen(false)}
                          >
                            System Admin
                          </Link>
                          <Link
                            to="/admin/users"
                            className="block px-4 py-2 hover:bg-dark text-red-400 font-bold transition last:rounded-b-lg"
                            onClick={() => setDropdownOpen(false)}
                          >
                            👥 Manage Users
                          </Link>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </>
            )}
          </div>

          {/* Auth Section */}
          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/profile"
                  className="flex items-center gap-2 hover:text-primary transition"
                >
                  <User size={20} />
                  <span>{user?.name}</span>
                  {user?.role && (
                    <span className={`text-xs font-bold px-2 py-1 rounded ${
                      user.role === "admin" ? "bg-red-600 text-white" :
                      user.role === "moderator" ? "bg-yellow-600 text-white" :
                      "bg-blue-600 text-white"
                    }`}>
                      {user.role.toUpperCase()}
                    </span>
                  )}
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 bg-primary px-4 py-2 rounded hover:bg-red-600 transition"
                >
                  <LogOut size={20} />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-primary transition">
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-primary px-4 py-2 rounded hover:bg-red-600 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-dark border-t border-primary">
          <div className="px-4 py-4 space-y-4">
            <Link
              to="/movies"
              className="block hover:text-primary transition"
              onClick={() => setIsOpen(false)}
            >
              Movies
            </Link>
            <Link
              to="/search"
              className="block hover:text-primary transition"
              onClick={() => setIsOpen(false)}
            >
              Search
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  to="/recommendations"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Recommendations
                </Link>
                <Link
                  to="/favorites"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Favorites
                </Link>
                <Link
                  to="/wishlist"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Wishlist
                </Link>
                <Link
                  to="/watch-history"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Watch History
                </Link>
                <Link
                  to="/user-dashboard"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/preferences"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Preferences
                </Link>
                {user?.role === "moderator" && (
                  <Link
                    to="/moderation"
                    className="block hover:text-primary transition text-yellow-400 font-bold"
                    onClick={() => setIsOpen(false)}
                  >
                    🛡️ Moderation
                  </Link>
                )}
                {user?.role === "admin" && (
                  <>
                    <Link
                      to="/analytics"
                      className="block hover:text-primary transition"
                      onClick={() => setIsOpen(false)}
                    >
                      Analytics
                    </Link>
                    <Link
                      to="/admin-dashboard"
                      className="block hover:text-primary transition"
                      onClick={() => setIsOpen(false)}
                    >
                      System Admin
                    </Link>
                    <Link
                      to="/admin/users"
                      className="block hover:text-primary transition text-red-400 font-bold"
                      onClick={() => setIsOpen(false)}
                    >
                      👥 Manage Users
                    </Link>
                  </>
                )}
                <Link
                  to="/profile"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full bg-primary px-4 py-2 rounded hover:bg-red-600 transition text-left"
                >
                  Logout
                </button>
              </>
            )}
            {!isAuthenticated && (
              <>
                <Link
                  to="/login"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block bg-primary px-4 py-2 rounded hover:bg-red-600 transition"
                  onClick={() => setIsOpen(false)}
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
