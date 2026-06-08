"""
Verify that all movies in the database have valid poster URLs
"""

import asyncio
from app.database import connect_to_mongo, close_mongo_connection, get_database

async def verify_posters():
    await connect_to_mongo()
    db = get_database()
    
    # Get all movies
    movies = await db.movies.find({}).to_list(length=None)
    
    print(f"Checking {len(movies)} movies...\n")
    
    # Check for issues
    empty_posters = 0
    null_posters = 0
    valid_posters = 0
    unique_urls = set()
    
    for movie in movies:
        poster = movie.get('poster_url', '')
        
        if poster is None:
            null_posters += 1
        elif poster == '':
            empty_posters += 1
        else:
            valid_posters += 1
            unique_urls.add(poster)
    
    print(f"✅ Valid posters: {valid_posters}")
    print(f"❌ Null posters: {null_posters}")
    print(f"❌ Empty posters: {empty_posters}")
    print(f"\nUnique poster URLs: {len(unique_urls)}")
    print(f"Movies: {len(movies)}")
    print(f"Poster coverage: {(valid_posters / len(movies) * 100):.1f}%")
    
    if null_posters > 0 or empty_posters > 0:
        print(f"\n❌ ERROR: Found {null_posters + empty_posters} movies without posters!")
        # Show examples
        for i, movie in enumerate(movies):
            if movie.get('poster_url') is None or movie.get('poster_url') == '':
                print(f"  - {movie.get('title')} (poster_url: {repr(movie.get('poster_url'))})")
                if i >= 5:
                    print(f"  ... and more")
                    break
    else:
        print(f"\n✅ ALL {len(movies)} movies have valid posters!")
    
    # Show sample URLs
    print(f"\nSample URLs:")
    for i, url in enumerate(list(unique_urls)[:5]):
        print(f"  {i+1}. {url}")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(verify_posters())
