#!/usr/bin/env bash
set -euo pipefail
BASE="http://localhost:8080/api"
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "1) Signup"
UNIQ=$(date +%s)
EMAIL="e2e+${UNIQ}@example.com"
RESP=$(curl -s -X POST "$BASE/auth/signup" -H "Content-Type: application/json" -d "{\"email\":\"$EMAIL\",\"password\":\"password123\"}")
# Extract JSON object from response (handles possible server logs)
extract_json(){
  local s="$1"
  # find first '{' and last '}' and extract between
  local start=$(echo "$s" | awk '{idx = index($0, "{"); if (idx>0) {print idx; exit}}')
  if [ -z "$start" ]; then echo ""; return; fi
  # last occurrence of '}'
  local last=$(echo "$s" | awk 'BEGIN{pos=0} {i=index($0,"}"); if(i>0){pos=pos+length($0)}} END{print pos}')
  # fallback: simple grep for first json-like line
  local jqline=$(echo "$s" | awk '/^{/{print; exit}')
  if [ -n "$jqline" ]; then echo "$jqline"; return; fi
  echo ""
}
JSON=$(extract_json "$RESP")
TOKEN=$(echo "$JSON" | jq -r .token)
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "Signup failed: $RESP"; exit 1
fi

echo "2) Create vegetable without unit"
VEGNAME="E2ETestVeg-${UNIQ}"
CREATERESP=$(curl -s -X POST "$BASE/vegetables" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"name\":\"$VEGNAME\"}")
echo "Create response raw: $CREATERESP"
# find the created veg via listing (more robust against mixed output)
LIST=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/vegetables")
ID=$(echo "$LIST" | jq -r --arg name "$VEGNAME" '.[] | select(.name==$name) | .id' | head -n1)
UNIT=$(echo "$LIST" | jq -r --arg name "$VEGNAME" '.[] | select(.name==$name) | .unit' | head -n1)
if [ -z "$ID" ]; then echo "Could not find created vegetable in list"; exit 6; fi
if [ "$UNIT" != "kg" ]; then
  echo "Unit defaulting failed, expected kg, got: $UNIT"; exit 2
fi

echo "3) Download CSV and check header"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/vegetables/$ID/export" -D "$TMPDIR/headers.txt" -o "/tmp/e2e_prices.csv"
cat "$TMPDIR/headers.txt"
head -n 5 "/tmp/e2e_prices.csv"
if ! head -n1 "/tmp/e2e_prices.csv" | grep -q "# name:"; then
  echo "CSV missing metadata name line"; exit 3
fi
if ! head -n2 "/tmp/e2e_prices.csv" | tail -n1 | grep -q "# unit:"; then
  echo "CSV missing metadata unit line"; exit 4
fi
if ! sed -n '3p' "/tmp/e2e_prices.csv" | grep -q "unit"; then
  echo "CSV header missing unit"; exit 5
fi

echo "E2E smoke test passed"
