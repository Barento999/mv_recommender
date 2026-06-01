import { Link } from "react-router-dom";
import { AlertTriangle, ArrowLeft } from "lucide-react";

function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark via-darkGray to-dark flex items-center justify-center px-4">
      <div className="text-center">
        <AlertTriangle className="w-24 h-24 text-primary mx-auto mb-6" />
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <p className="text-2xl text-gray-300 mb-2">Page Not Found</p>
        <p className="text-gray-400 mb-8">
          Sorry, the page you're looking for doesn't exist.
        </p>

        <Link
          to="/"
          className="inline-flex items-center gap-2 bg-primary px-8 py-3 rounded-lg font-semibold hover:bg-red-600 transition"
        >
          <ArrowLeft size={20} />
          Back to Home
        </Link>
      </div>
    </div>
  );
}

export default NotFoundPage;
