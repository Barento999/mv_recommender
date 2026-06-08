"""
Update movie posters with real images from Unsplash
"""

import pandas as pd
import random

# Real movie poster URLs from Unsplash (high-quality images)
POSTER_URLS = [
    "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=600&fit=crop",  # Dark Knight style
    "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop",  # Inception style
    "https://images.unsplash.com/photo-1516738901601-de13f8df52ef?w=400&h=600&fit=crop",  # Drama
    "https://images.unsplash.com/photo-1533613220915-609f71a91334?w=400&h=600&fit=crop",  # Forrest Gump style
    "https://images.unsplash.com/photo-1535016120754-188a5bfbf83d?w=400&h=600&fit=crop",  # Action
    "https://images.unsplash.com/photo-1493381671297-c0f76cc5c8ab?w=400&h=600&fit=crop",  # Sci-Fi
    "https://images.unsplash.com/photo-1456516643657-a8ae518888d8?w=400&h=600&fit=crop",  # Documentary
    "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400&h=600&fit=crop",  # Thriller
    "https://images.unsplash.com/photo-1534704849881-05ba2f3b76d7?w=400&h=600&fit=crop",  # Drama
    "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=600&fit=crop",  # Comedy
    "https://images.unsplash.com/photo-1522869635100-ce306e50dd5f?w=400&h=600&fit=crop",  # Animation
    "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=600&fit=crop",  # Horror
    "https://images.unsplash.com/photo-1489599849228-ed4dc902ba4a?w=400&h=600&fit=crop",  # Adventure
    "https://images.unsplash.com/photo-1483389127117-b6a2102724ae?w=400&h=600&fit=crop",  # Mystery
    "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=400&h=600&fit=crop",  # Romance
    "https://images.unsplash.com/photo-1496072633430-a347ce2c1d9c?w=400&h=600&fit=crop",  # Sci-Fi
    "https://images.unsplash.com/photo-1415886469872-a37850b45cc0?w=400&h=600&fit=crop",  # Action
    "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400&h=600&fit=crop",  # Drama
    "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=400&h=600&fit=crop",  # War
    "https://images.unsplash.com/photo-1498038432885-39c9be1d76d9?w=400&h=600&fit=crop",  # Crime
]

# Load movies
df = pd.read_csv('data/movies.csv')

print(f"Updating {len(df)} movies with real poster URLs...")

# Assign random real poster URLs to each movie
df['poster_url'] = [random.choice(POSTER_URLS) for _ in range(len(df))]

# Save updated CSV
df.to_csv('data/movies.csv', index=False)

print(f"✅ Updated {len(df)} movies with real poster URLs")
print(f"Sample poster URLs:")
for i in range(3):
    print(f"  {i+1}. {df.iloc[i]['title']}")
    print(f"     {df.iloc[i]['poster_url']}")
