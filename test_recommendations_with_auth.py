#!/usr/bin/env python3
"""Test recommendations endpoint with proper authentication."""

import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Testing Recommendations Endpoints\n")
print("=" * 70)

# Step 1: Login to get token
print("\n1️⃣ Attempting to login with test credentials...")
print("-" * 70)

login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "alice@example.com",
        "password": "password123"
    }
)

if login_response.status_code == 200:
    auth_data = login_response.json()
    token = auth_data.get("access_token")
    print(f"✅ Login successful!")
    print(f"   Token: {token[:20]}...")
    
    # Step 2: Test basic recommendations
    print("\n2️⃣ Testing GET /recommendations (basic)...")
    print("-" * 70)
    
    rec_response = requests.get(
        f"{BASE_URL}/recommendations",
        params={"limit": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if rec_response.status_code == 200:
        data = rec_response.json()
        print(f"✅ Basic recommendations working!")
        print(f"   Count: {data.get('count', 0)}")
        print(f"   Message: {data.get('message', 'N/A')}")
    else:
        print(f"❌ Error: {rec_response.status_code}")
        print(f"   {rec_response.text}")
    
    # Step 3: Test recommendations with explanations
    print("\n3️⃣ Testing GET /recommendations/explained...")
    print("-" * 70)
    
    explained_response = requests.get(
        f"{BASE_URL}/recommendations/explained",
        params={"limit": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if explained_response.status_code == 200:
        data = explained_response.json()
        print(f"✅ Explained recommendations working!")
        print(f"   Count: {data.get('count', 0)}")
        print(f"   Message: {data.get('message', 'N/A')}")
        print(f"   Total favorites: {data.get('total_favorites', 0)}")
        
        # Show detailed info for first recommendation
        if data.get('recommendations'):
            first_rec = data['recommendations'][0]
            print(f"\n   📌 First Recommendation:")
            print(f"      Title: {first_rec.get('title', 'Unknown')}")
            print(f"      Rating: {first_rec.get('rating', 0)}/10")
            
            if first_rec.get('explanation'):
                exp = first_rec['explanation']
                print(f"      \n      Explanation:")
                print(f"      Type: {exp.get('type', 'Unknown')}")
                print(f"      Confidence: {exp.get('confidence', 0)}%")
                print(f"      Rank: {exp.get('rank', 0)}")
                print(f"      Reasons:")
                for reason in exp.get('reasons', []):
                    print(f"        • {reason}")
    else:
        print(f"❌ Error: {explained_response.status_code}")
        print(f"   {explained_response.text}")
    
    # Step 4: Test getting a specific explanation
    if data.get('recommendations'):
        movie_id = data['recommendations'][0]['_id']
        print(f"\n4️⃣ Testing GET /recommendations/explanation/{{movie_id}}...")
        print("-" * 70)
        
        exp_response = requests.get(
            f"{BASE_URL}/recommendations/explanation/{movie_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if exp_response.status_code == 200:
            exp_data = exp_response.json()
            print(f"✅ Movie explanation working!")
            print(f"   Title: {exp_data.get('title', 'Unknown')}")
            if exp_data.get('recommendation_factors'):
                factors = exp_data['recommendation_factors']
                print(f"   \n   Recommendation Factors:")
                if factors.get('genre_match'):
                    gm = factors['genre_match']
                    print(f"     Genre Match: {gm.get('score', 0):.1f}%")
                if factors.get('rating_analysis'):
                    ra = factors['rating_analysis']
                    print(f"     Movie Rating: {ra.get('movie_rating', 0)}/10")
                    print(f"     User Avg: {ra.get('user_average_rating', 0)}/10")
        else:
            print(f"❌ Error: {exp_response.status_code}")
            print(f"   {exp_response.text}")

else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(f"   Response: {login_response.text}")
    print("\n💡 Try using different test credentials if available")

print("\n" + "=" * 70)
print("\n✅ Recommendations page features:")
print("   • GET /recommendations - Basic recommendations")
print("   • GET /recommendations/explained - With explanations")
print("   • GET /recommendations/explanation/{id} - Detailed explanation")
print("   • RecommendationCard component shows badges with reasons")
print("   • Confidence scores indicate recommendation strength")
