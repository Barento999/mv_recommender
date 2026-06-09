#!/usr/bin/env python3
"""Test script to verify all analytics endpoints are working."""

import requests
import json

BASE_URL = "http://localhost:8000"

endpoints = [
    "/analytics/overview",
    "/analytics/ratings-distribution",
    "/analytics/genre-analytics",
    "/analytics/user-engagement",
    "/analytics/top-movies-analytics",
    "/analytics/timeline-stats",
]

print("🧪 Testing Analytics Endpoints\n")
print("=" * 60)

all_passed = True

for endpoint in endpoints:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        status = response.status_code
        
        if status == 200:
            data = response.json()
            print(f"✅ {endpoint}")
            print(f"   Status: {status}")
            print(f"   Data keys: {list(data.keys())}")
        else:
            print(f"❌ {endpoint}")
            print(f"   Status: {status}")
            print(f"   Error: {response.text}")
            all_passed = False
    except Exception as e:
        print(f"❌ {endpoint}")
        print(f"   Error: {str(e)}")
        all_passed = False
    
    print()

print("=" * 60)

if all_passed:
    print("✅ All endpoints are working correctly!")
else:
    print("❌ Some endpoints failed. Check the output above.")

print("\n📝 Note: Make sure the backend is running on http://localhost:8000")
