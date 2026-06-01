import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, Heart, TrendingUp } from "lucide-react";
import useAuth from "../hooks/useAuth";

function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark via-dark to-darkGray">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-20 sm:py-32">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-red-500 to-primary bg-clip-text text-transparent">
            Discover Your Next Favorite Movie
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Personalized movie recommendations based on your preferences.
            Explore, rate, and save your favorite films.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/movies"
              className="bg-primary px-8 py-3 rounded-lg font-semibold hover:bg-red-600 transition inline-flex items-center justify-center gap-2"
            >
              Explore Movies
              <ArrowRight size={20} />
            </Link>
            {!isAuthenticated && (
              <Link
                to="/register"
                className="border-2 border-primary px-8 py-3 rounded-lg font-semibold hover:bg-primary transition"
              >
                Get Started
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16">
          Why Choose MovieReco?
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-darkGray p-8 rounded-lg border border-primary/20 hover:border-primary transition">
            <Sparkles className="text-primary mb-4" size={32} />
            <h3 className="text-xl font-bold mb-3">Smart Recommendations</h3>
            <p className="text-gray-400">
              Get personalized movie recommendations based on your favorite
              films and ratings.
            </p>
          </div>

          <div className="bg-darkGray p-8 rounded-lg border border-primary/20 hover:border-primary transition">
            <Heart className="text-primary mb-4" size={32} />
            <h3 className="text-xl font-bold mb-3">Manage Favorites</h3>
            <p className="text-gray-400">
              Save your favorite movies and quickly access them anytime you
              want.
            </p>
          </div>

          <div className="bg-darkGray p-8 rounded-lg border border-primary/20 hover:border-primary transition">
            <TrendingUp className="text-primary mb-4" size={32} />
            <h3 className="text-xl font-bold mb-3">Explore Trends</h3>
            <p className="text-gray-400">
              Discover trending movies and top-rated films in various genres.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      {!isAuthenticated && (
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <div className="bg-gradient-to-r from-primary/10 via-primary/5 to-primary/10 p-12 rounded-lg border border-primary/30">
            <h2 className="text-3xl font-bold mb-4">
              Ready to Find Your Next Favorite?
            </h2>
            <p className="text-gray-300 mb-8">
              Sign up now to get personalized movie recommendations and manage
              your favorites.
            </p>
            <Link
              to="/register"
              className="bg-primary px-8 py-3 rounded-lg font-semibold hover:bg-red-600 transition inline-flex items-center gap-2"
            >
              Create Account
              <ArrowRight size={20} />
            </Link>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-primary/20 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
          <p>&copy; 2024 Movie Recommendation System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
