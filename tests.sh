#!/bin/bash

# Usage: ./tests.sh local|prod ADMIN_KEY

if [ $# -lt 2 ]; then
    echo "Usage: $0 local|prod ADMIN_KEY"
    exit 1
fi

ENVIRONMENT="$1"
ADMIN_KEY="$2"

if [ "$ENVIRONMENT" == "local" ]; then
    BASE_URL="http://localhost:5000"
elif [ "$ENVIRONMENT" == "prod" ]; then
    BASE_URL="https://kixote.typemill.net"
else
    echo "First parameter must be 'local' or 'prod'"
    exit 1
fi

echo "Testing Kixote API at $BASE_URL with ADMIN_KEY=$ADMIN_KEY"
echo "--------------------------------"

echo "1) List Clients:"
curl -s -X GET "$BASE_URL/auth/list_clients" \
     -H "X-ADMIN-KEY: $ADMIN_KEY"
echo -e "\n"

echo "2) Create Client:"
curl -s -X POST "$BASE_URL/auth/create_client" \
     -H "Content-Type: application/json" \
     -H "X-ADMIN-KEY: $ADMIN_KEY" \
     -d '{"client_id": "autoclient", "license": "business"}'
echo -e "\n"

echo "3) Get Client:"
curl -s -X GET "$BASE_URL/auth/get_client" \
     -H "Content-Type: application/json" \
     -H "X-ADMIN-KEY: $ADMIN_KEY" \
     -d '{"client_id": "autoclient"}'
echo -e "\n"

echo "4) Revoke Client Key:"
curl -s -X POST "$BASE_URL/auth/revoke_client_key" \
     -H "Content-Type: application/json" \
     -H "X-ADMIN-KEY: $ADMIN_KEY" \
     -d '{"client_id": "autoclient"}'
echo -e "\n"

echo "5) Recreate Client Key:"
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/recreate_client_key" \
     -H "Content-Type: application/json" \
     -H "X-ADMIN-KEY: $ADMIN_KEY" \
     -d '{"client_id": "autoclient"}')
echo "$CREATE_RESPONSE"
echo -e "\n"

# Extract API key from step 5
API_KEY=$(echo "$CREATE_RESPONSE" | jq -r '.api_key')

if [ "$API_KEY" == "null" ] || [ -z "$API_KEY" ]; then
    echo "❌ Could not extract API key from recreate_client_key response. Skipping /check tests."
else
    echo "✅ API key acquired: $API_KEY"

    # Login to get JWT
    echo "Login to get JWT token..."
    JWT_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
         -H "Content-Type: application/json" \
         -d "{\"api_key\": \"$API_KEY\"}" | jq -r '.access_token')

    if [ "$JWT_TOKEN" == "null" ] || [ -z "$JWT_TOKEN" ]; then
        echo "❌ Failed to obtain JWT token, skipping /check tests."
    else
        echo "✅ JWT token acquired."

        echo "--------------------------------"
        echo "Testing /check routes"
        echo "--------------------------------"

        echo "6) /check/"
        curl -s -X GET "$BASE_URL/check/"
        echo -e "\n"

        echo "7) /check/auth"
        curl -s -X GET "$BASE_URL/check/auth" \
             -H "Authorization: Bearer $JWT_TOKEN"
        echo -e "\n"

        echo "8) /check/limit"
        curl -s -X GET "$BASE_URL/check/limit" \
             -H "Authorization: Bearer $JWT_TOKEN"
        echo -e "\n"

        echo "9) /check/rate"
        curl -s -X GET "$BASE_URL/check/rate" \
             -H "Authorization: Bearer $JWT_TOKEN"
        echo -e "\n"
    fi
fi

echo "10) List Clients:"
curl -s -X GET "$BASE_URL/auth/list_clients" \
     -H "X-ADMIN-KEY: $ADMIN_KEY"
echo -e "\n"

echo "11) Delete Client:"
curl -s -X DELETE "$BASE_URL/auth/delete_client" \
     -H "Content-Type: application/json" \
     -H "X-ADMIN-KEY: $ADMIN_KEY" \
     -d '{"client_id": "autoclient"}'
echo -e "\n"

echo "--------------------------------"
echo "Tests finished."
