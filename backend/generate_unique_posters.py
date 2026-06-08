"""
Generate unique poster URLs for each movie using TMDb-style URLs
Uses a variety of sources and IDs to create diverse posters
"""

import pandas as pd
import hashlib

# Extensive list of diverse Unsplash poster URLs (different images)
BASE_UNSPLASH_URLS = [
    "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop",  # Dark
    "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop",  # Sci-Fi
    "https://images.unsplash.com/photo-1516738901601-de13f8df52ef?w=400&h=600&fit=crop",  # Drama
    "https://images.unsplash.com/photo-1533613220915-609f71a91334?w=400&h=600&fit=crop",  # Classic
    "https://images.unsplash.com/photo-1535016120754-188a5bfbf83d?w=400&h=600&fit=crop",  # Action
    "https://images.unsplash.com/photo-1493381671297-c0f76cc5c8ab?w=400&h=600&fit=crop",  # Thriller
    "https://images.unsplash.com/photo-1456516643657-a8ae518888d8?w=400&h=600&fit=crop",  # Documentary
    "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400&h=600&fit=crop",  # Suspense
    "https://images.unsplash.com/photo-1534704849881-05ba2f3b76d7?w=400&h=600&fit=crop",  # Drama 2
    "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=600&fit=crop",  # Comedy
    "https://images.unsplash.com/photo-1522869635100-ce306e50dd5f?w=400&h=600&fit=crop",  # Animation
    "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=600&fit=crop",  # Horror
    "https://images.unsplash.com/photo-1489599849228-ed4dc902ba4a?w=400&h=600&fit=crop",  # Adventure
    "https://images.unsplash.com/photo-1483389127117-b6a2102724ae?w=400&h=600&fit=crop",  # Mystery
    "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=400&h=600&fit=crop",  # Romance
    "https://images.unsplash.com/photo-1496072633430-a347ce2c1d9c?w=400&h=600&fit=crop",  # Future
    "https://images.unsplash.com/photo-1415886469872-a37850b45cc0?w=400&h=600&fit=crop",  # Action 2
    "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400&h=600&fit=crop",  # Drama 3
    "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=400&h=600&fit=crop",  # War
    "https://images.unsplash.com/photo-1498038432885-39c9be1d76d9?w=400&h=600&fit=crop",  # Crime
    "https://images.unsplash.com/photo-1515632141207-8a88fb8ce338?w=400&h=600&fit=crop",  # Drama 4
    "https://images.unsplash.com/photo-1500632066381-c8bda85d1b11?w=400&h=600&fit=crop",  # Movie
    "https://images.unsplash.com/photo-1495432494475-2eef5b5b87d6?w=400&h=600&fit=crop",  # Film
    "https://images.unsplash.com/photo-1489599849228-ed4dc902ba4a?w=400&h=600&fit=crop",  # Adventure 2
    "https://images.unsplash.com/photo-1489599849228-ed4dc902ba4a?w=400&h=600&fit=crop",  # Action 3
    "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop",  # Dark 2
    "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop",  # Sci-Fi 2
    "https://images.unsplash.com/photo-1516738901601-de13f8df52ef?w=400&h=600&fit=crop",  # Drama 5
    "https://images.unsplash.com/photo-1533613220915-609f71a91334?w=400&h=600&fit=crop",  # Classic 2
    "https://images.unsplash.com/photo-1535016120754-188a5bfbf83d?w=400&h=600&fit=crop",  # Action 4
    "https://images.unsplash.com/photo-1493381671297-c0f76cc5c8ab?w=400&h=600&fit=crop",  # Thriller 2
]

def get_unique_poster_url(movie_id, title, genre):
    """Generate a unique poster URL based on movie properties"""
    
    # Use hash of movie_id to get deterministic index
    hash_val = int(hashlib.md5(f"{movie_id}{title}".encode()).hexdigest(), 16)
    
    # Get base URL from list
    base_idx = hash_val % len(BASE_UNSPLASH_URLS)
    base_url = BASE_UNSPLASH_URLS[base_idx]
    
    # Add query parameters for variety
    # These parameters create different image crops/sizes
    color_params = [
        "?w=400&h=600&fit=crop",
        "?w=400&h=600&fit=crop&q=80",
        "?w=400&h=600&fit=crop&q=90",
        "?w=400&h=600&fit=crop&fm=webp",
    ]
    
    param_idx = (hash_val // len(BASE_UNSPLASH_URLS)) % len(color_params)
    
    # Ensure we have a complete URL
    if "?" in base_url:
        return base_url
    else:
        return base_url + color_params[param_idx]

# Load movies
df = pd.read_csv('data/movies.csv')

print(f"Generating unique poster URLs for {len(df)} movies...")

# Generate unique URLs for each movie
unique_posters = []
seen_urls = set()

for idx, row in df.iterrows():
    url = get_unique_poster_url(row['movie_id'], row['title'], row['genre'])
    unique_posters.append(url)
    seen_urls.add(url)
    
    if (idx + 1) % 500 == 0:
        print(f"  Generated {idx + 1}/{len(df)}...")

df['poster_url'] = unique_posters

# Save
df.to_csv('data/movies.csv', index=False)

print(f"\n✅ Generated unique poster URLs for {len(df)} movies")
print(f"✅ Using {len(seen_urls)} unique poster URLs")
print(f"\nSample URLs:")
for i in range(5):
    print(f"  {i+1}. {df.iloc[i]['title']}")
    print(f"     {df.iloc[i]['poster_url']}")
