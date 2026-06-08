"""
Test the favorites endpoint to ensure it works
"""

import requests
import json

# Test data
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123456"
TEST_NAME = "Test User"

def test_favorites():
    print("🧪 TESTING FAVORITES FUNCTIONALITY\n")
    
    # 1. Create test user via API
    print("1️⃣ Registering user...")
    try:
        reg_response = requests.post(
            "http://localhost:8000/auth/register",
            json={
                "name": TEST_NAME,
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        print(f"   Status: {reg_response.status_code}")
        if reg_response.status_code == 200:
            print(f"   ✅ User registered")
        else:
            print(f"   Response: {reg_response.text}")
        
        # 2. Login
        print("\n2️⃣ Logging in...")
        login_response = requests.post(
            "http://localhost:8000/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        print(f"   Status: {login_response.status_code}")
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get("access_token")
            user_id = login_data.get("user", {}).get("_id")
            print(f"   ✅ Logged in")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"   Response: {login_response.text}")
            return
        
        # 3. Get a movie to favorite
        print("\n3️⃣ Getting a movie...")
        movies_response = requests.get(
            "http://localhost:8000/movies?limit=1"
        )
        if movies_response.status_code == 200:
            movies_data = movies_response.json()
            movie_id = movies_data["movies"][0]["_id"]
            movie_title = movies_data["movies"][0]["title"]
            print(f"   ✅ Got movie: {movie_title}")
            print(f"   Movie ID: {movie_id}")
        else:
            print(f"   Response: {movies_response.text}")
            return
        
        # 4. Add to favorites
        print("\n4️⃣ Adding to favorites...")
        fav_response = requests.post(
            f"http://localhost:8000/favorites/add/{movie_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {fav_response.status_code}")
        if fav_response.status_code == 200:
            print(f"   ✅ Added to favorites")
            print(f"   Response: {fav_response.json()}")
        else:
            print(f"   ❌ Failed to add favorite")
            print(f"   Response: {fav_response.text}")
        
        # 5. Check if favorite
        print("\n5️⃣ Checking if favorited...")
        check_response = requests.get(
            f"http://localhost:8000/favorites/check/{movie_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {check_response.status_code}")
        if check_response.status_code == 200:
            check_data = check_response.json()
            is_fav = check_data.get("is_favorite")
            print(f"   Is favorite: {is_fav} ✅")
        else:
            print(f"   Response: {check_response.text}")
        
        # 6. Get favorites list
        print("\n6️⃣ Getting favorites list...")
        list_response = requests.get(
            "http://localhost:8000/favorites",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {list_response.status_code}")
        if list_response.status_code == 200:
            list_data = list_response.json()
            favorites = list_data.get("favorites", [])
            print(f"   Favorites count: {list_data.get('total')}")
            if favorites:
                print(f"   First favorite: {favorites[0].get('title')}")
                print(f"   ✅ Favorites list working")
        else:
            print(f"   Response: {list_response.text}")
        
        # 7. Remove from favorites
        print("\n7️⃣ Removing from favorites...")
        remove_response = requests.delete(
            f"http://localhost:8000/favorites/remove/{movie_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {remove_response.status_code}")
        if remove_response.status_code == 200:
            print(f"   ✅ Removed from favorites")
        else:
            print(f"   Response: {remove_response.text}")
    
        print("\n✅ FAVORITES TEST COMPLETE")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_favorites()
