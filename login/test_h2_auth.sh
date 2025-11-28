#!/bin/bash
set -e

BASE_URL="http://localhost:8081/api/v1"

echo "Starting quick H2 auth test..."
EMAIL="dev_$(date +%s)@mail.com"
PASS="Secret123!"

curl -s -X POST "$BASE_URL/registration" -H "Content-Type: application/json" -d '{
  "firstName":"Dev",
  "lastName":"User",
  "email":"'"$EMAIL"'",
  "password":"'"$PASS"'",
  "isAdmin":false
}' | cat

echo "\nLogin:"
curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{
  "email":"'"$EMAIL"'",
  "password":"'"$PASS"'"
}' | cat

echo "\nDone."