#!/usr/bin/env python3
"""Test script to verify recommendation explanations are working."""

import requests
import json

BASE_URL = "http://localhost:8000"

# First, get auth token (you may need to adjust this based on your test user)
print("🧪 Testing Recommendation Explanation Features\n")
print("=" * 60)

# Test 1: Get recommendations with explanations (requires auth)
print("\n1️⃣ Getting recommendations with explanations...")
print("-" * 60)

# You'll need to set a valid token here or use test credentials
# This is just a demonstration of the endpoint structure
test_token = "your-test-token-here"  # Replace with actual test token

headers = {"Authorization": f"Bearer {test_token}"}

try:
    response = requests.get(
        f"{BASE_URL}/recommendations/explained",
        params={"limit": 5},
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Request successful!")
        print(f"   Found {data.get('count', 0)} recommendations")
        print(f"   Message: {data.get('message', 'N/A')}")
        
        # Show first recommendation details
        if data.get('recommendations'):
            first_rec = data['recommendations'][0]
            print(f"\n   📌 First Recommendation:")
            print(f"      Title: {first_rec.get('title', 'Unknown')}")
            print(f"      Rating: {first_rec.get('rating', 0)}/10")
            
            if first_rec.get('explanation'):
                exp = first_rec['explanation']
                print(f"      Why: {exp.get('type', 'Unknown')} ({exp.get('confidence', 0)}% confidence)")
                print(f"      Reasons:")
                for reason in exp.get('reasons', []):
                    print(f"        • {reason}")
    elif response.status_code == 401:
        print(f"⚠️  Authentication required (401)")
        print(f"   Please use a valid auth token to test this endpoint")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("\n📝 Recommendation Explanation Features:")
print("   • Each recommendation includes an explanation type")
print("   • Types include: Genre Match, High Rated, Recent & Popular")
print("   • Includes confidence percentage (0-100%)")
print("   • Shows specific reasons for the recommendation")
print("   • Based on user's favorite movies and ratings")
print("\n💡 Frontend Features:")
print("   • RecommendationCard component shows explanation badges")
print("   • Click badge to expand detailed reasons")
print("   • Visual icons indicate explanation type")
print("   • Responsive design for all screen sizes")
