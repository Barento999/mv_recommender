import { ChevronLeft, ChevronRight } from "lucide-react";

function Pagination({ currentPage, totalPages, onPageChange }) {
  return (
    <div className="flex justify-center items-center gap-2 mt-8">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded bg-darkGray disabled:opacity-50 hover:bg-primary transition"
      >
        <ChevronLeft size={20} />
      </button>

      {Array.from({ length: Math.min(5, totalPages) }).map((_, i) => {
        let pageNum;
        if (totalPages <= 5) {
          pageNum = i + 1;
        } else if (currentPage <= 3) {
          pageNum = i + 1;
        } else if (currentPage >= totalPages - 2) {
          pageNum = totalPages - 4 + i;
        } else {
          pageNum = currentPage - 2 + i;
        }

        return (
          <button
            key={pageNum}
            onClick={() => onPageChange(pageNum)}
            className={`w-10 h-10 rounded transition ${
              currentPage === pageNum
                ? "bg-primary text-white"
                : "bg-darkGray hover:bg-primary"
            }`}
          >
            {pageNum}
          </button>
        );
      })}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded bg-darkGray disabled:opacity-50 hover:bg-primary transition"
      >
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

export default Pagination;
