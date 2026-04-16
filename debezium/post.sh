#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../.env"

curl -i -X POST \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data @"$CONNECTOR_JSON" \
  "$CONNECT_URL"