#!/usr/bin/env python
"""
Smoke Test - Quick Health Checks
Tests only endpoints not covered in other test files
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8081/api/v1"
FASTAPI_URL = "http://localhost:8000"

print("=" * 70)
print("           STARTHUB - SMOKE TEST (HEALTH CHECKS)")
print("=" * 70)

# Test 1: FastAPI Health Check
print("\n1️⃣  FASTAPI HEALTH CHECK")
print("-" * 70)

try:
    response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ FastAPI is running!")
        print(f"Response: {response.json()}")
    else:
        print(f"⚠️  FastAPI response: {response.status_code}")
except Exception as e:
    print(f"❌ FastAPI error: {e}")

print("\n" + "=" * 70)
print("                   SMOKE TEST COMPLETE!")
print("=" * 70)
print("\nNote: For comprehensive tests, run:")
print("  - test_users_startups.py")
print("  - test_votes_comments.py")
print("  - test_search.py")
print("  - test_crud_complete.py")
