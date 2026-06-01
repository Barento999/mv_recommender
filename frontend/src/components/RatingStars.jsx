import { Star } from "lucide-react";
import { useState } from "react";

function RatingStars({
  initialRating = 0,
  onRate,
  disabled = false,
  interactive = true,
}) {
  const [hoverRating, setHoverRating] = useState(0);
  const [rating, setRating] = useState(initialRating);

  const handleClick = (value) => {
    if (!disabled && interactive) {
      setRating(value);
      onRate?.(value);
    }
  };

  const displayRating = hoverRating || rating;

  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((value) => (
        <button
          key={value}
          onClick={() => handleClick(value)}
          onMouseEnter={() => interactive && setHoverRating(value)}
          onMouseLeave={() => setHoverRating(0)}
          disabled={disabled}
          className={`${interactive ? "cursor-pointer" : "cursor-default"} ${disabled ? "opacity-50" : ""}`}
        >
          <Star
            size={20}
            className={
              displayRating >= value
                ? "fill-yellow-400 text-yellow-400"
                : "text-gray-400"
            }
          />
        </button>
      ))}
      <span className="ml-2 text-lg">{displayRating.toFixed(1)}</span>
    </div>
  );
}

export default RatingStars;
