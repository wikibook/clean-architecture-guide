#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_DEFAULT_REGION:-ap-northeast-2}"
STAGE="${STAGE:-dev}"

# Ensure dependencies: aws, jq, curl
if ! command -v jq >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -y && sudo apt-get install -y jq
  else
    echo "jq가 필요합니다. 설치 후 다시 실행하세요." >&2
    exit 1
  fi
fi

if ! command -v aws >/dev/null 2>&1; then
  python3 -m pip install --user awscli
  export PATH="$HOME/.local/bin:$PATH"
fi

# Resolve Service Endpoint
SERVICE_ENDPOINT="${SERVICE_ENDPOINT:-}"
if [ -z "$SERVICE_ENDPOINT" ]; then
  if command -v serverless >/dev/null 2>&1; then
    SERVICE_ENDPOINT=$(serverless info --verbose --stage "$STAGE" --region "$REGION" | awk '/ServiceEndpoint/ {print $2; exit}') || true
  fi
fi

if [ -z "${SERVICE_ENDPOINT:-}" ]; then
  echo "ServiceEndpoint를 찾을 수 없습니다. SERVICE_ENDPOINT 환경변수로 전달하거나 serverless info가 동작해야 합니다." >&2
  exit 1
fi

# Normalize base endpoint (no trailing slash)
SERVICE_ENDPOINT=${SERVICE_ENDPOINT%/}
ORDER_ENDPOINT="$SERVICE_ENDPOINT/order"

echo "Using endpoint: $ORDER_ENDPOINT"

ts=$(date +%s)
TEST_COFFEE_ID="ci-coffee-$ts"
TEST_CUSTOMER_ID="ci-cust-$ts"
TEST_ORDER_ITEM_ID="item-PLACEHOLDER"
PRICE=4500
QTY=2

# Seed Coffee item
aws dynamodb put-item \
  --table-name Coffees \
  --region "$REGION" \
  --item "{\"id\":{\"S\":\"$TEST_COFFEE_ID\"},\"name\":{\"S\":\"Americano CI\"},\"price\":{\"N\":\"$PRICE\"},\"currency\":{\"S\":\"KRW\"},\"description\":{\"S\":\"CI Test Coffee\"},\"stock\":{\"N\":\"100\"}}"

echo "Seeded coffee: $TEST_COFFEE_ID"

# Call API
REQ_BODY=$(jq -n --arg cust "$TEST_CUSTOMER_ID" --arg coffee "$TEST_COFFEE_ID" --argjson qty $QTY '{customer_id:$cust, coffee_id:$coffee, quantity:$qty}')

echo "Request: $REQ_BODY"
RESP=$(curl -sS -X POST "$ORDER_ENDPOINT" -H 'Content-Type: application/json' -d "$REQ_BODY")

echo "Response: $RESP"

STATUS=$(echo "$RESP" | jq -r '.status // empty')
if [ "$STATUS" != "success" ]; then
  echo "API 응답이 실패했습니다." >&2
  echo "$RESP" | jq . || true
  # Cleanup coffee before exit
  aws dynamodb delete-item --table-name Coffees --region "$REGION" --key "{\"id\":{\"S\":\"$TEST_COFFEE_ID\"}}" || true
  exit 1
fi

ORDER_ID=$(echo "$RESP" | jq -r '.data.orderId // empty')
if [ -z "$ORDER_ID" ]; then
  echo "응답에 orderId가 없습니다." >&2
  aws dynamodb delete-item --table-name Coffees --region "$REGION" --key "{\"id\":{\"S\":\"$TEST_COFFEE_ID\"}}" || true
  exit 1
fi

# Compute order item id (matches domain/entities/order.py pattern)
ORDER_ITEM_ID="item-$ORDER_ID-$TEST_COFFEE_ID"

echo "Created order: $ORDER_ID"

# Basic assertions
TOTAL=$(echo "$RESP" | jq -r '.data.totalAmount // empty')
if [ -z "$TOTAL" ] || [ "$TOTAL" = "null" ]; then
  echo "totalAmount가 없습니다." >&2
  exit_code=1
else
  exit_code=0
fi

# Cleanup created data
aws dynamodb delete-item --table-name Orders --region "$REGION" --key "{\"id\":{\"S\":\"$ORDER_ID\"}}" || true
aws dynamodb delete-item --table-name OrderItems --region "$REGION" --key "{\"id\":{\"S\":\"$ORDER_ITEM_ID\"}}" || true
aws dynamodb delete-item --table-name Coffees --region "$REGION" --key "{\"id\":{\"S\":\"$TEST_COFFEE_ID\"}}" || true

echo "Cleanup done."

exit $exit_code
