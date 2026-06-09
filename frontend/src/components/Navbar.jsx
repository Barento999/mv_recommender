import { Link, useNavigate } from "react-router-dom";
import { Menu, X, LogOut, User } from "lucide-react";
import { useState } from "react";
import useAuth from "../hooks/useAuth";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
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
                <Link
                  to="/user-dashboard"
                  className="hover:text-primary transition"
                >
                  Dashboard
                </Link>
                <Link
                  to="/analytics"
                  className="hover:text-primary transition"
                >
                  Analytics
                </Link>
                <Link
                  to="/preferences"
                  className="hover:text-primary transition"
                >
                  Preferences
                </Link>
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
                  {user?.name}
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
                  to="/user-dashboard"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/analytics"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Analytics
                </Link>
                <Link
                  to="/preferences"
                  className="block hover:text-primary transition"
                  onClick={() => setIsOpen(false)}
                >
                  Preferences
                </Link>
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
