#!/bin/bash
BASE_URL=${BASE_URL:-http://localhost:8081/api/v1}

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <email> <password>"
  exit 1
fi

EMAIL="$1"
PASS="$2"

curl -s -X POST "$BASE_URL/auth/login" -H 'Content-Type: application/json' -d '{
  "email":"'"$EMAIL"'",
  "password":"'"$PASS"'"
}' | jq .