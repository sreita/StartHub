#!/usr/bin/env python
"""
Smoke Test - Quick Health Checks
Tests only endpoints not covered in other test files
"""

import requests
import json

# Configuration
AUTH_API_URL = "http://localhost:8081/api/v1"
FASTAPI_BASE_URL = "http://localhost:8000"

print("=" * 70)
print("           STARTHUB - SMOKE TEST (HEALTH CHECKS)")
print("=" * 70)

# Test 1: FastAPI Health Check
print("\n1️⃣  FASTAPI HEALTH CHECKS")
print("-" * 70)

try:
    response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
    print(f"/health -> Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ FastAPI app reachable")
    else:
        print(f"⚠️  FastAPI /health returned {response.status_code}")
except Exception as e:
    print(f"❌ FastAPI error: {e}")

# Test 1b: FastAPI DB Health Check
try:
    response = requests.get(f"{FASTAPI_BASE_URL}/health/db", timeout=5)
    print(f"/health/db -> Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Database reachable")
    else:
        print(f"⚠️  FastAPI /health/db returned {response.status_code}")
except Exception as e:
    print(f"❌ FastAPI error: {e}")

print("\n" + "=" * 70)
print("                   SMOKE TEST COMPLETE!")
print("=" * 70)
print("\nNote: For comprehensive tests, run:")
print("  - scripts/test/unit/test_users_startups.py")
print("  - scripts/test/unit/test_votes_comments.py")
print("  - scripts/test/unit/test_search.py")
print("  - scripts/test/unit/test_crud_complete.py")
