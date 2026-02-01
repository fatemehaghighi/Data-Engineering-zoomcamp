#!/bin/bash

echo "Deploying flows to Kestra..."

for flow_file in flows/*.yaml; do
  if [ -f "$flow_file" ]; then
    echo "Deploying $(basename $flow_file)..."
    curl -X POST \
      -u "admin@kestra.io:Admin1234" \
      -H "Content-Type: application/x-yaml" \
      --data-binary @"$flow_file" \
      "http://localhost:8080/api/v1/flows"
    echo ""
  fi
done

echo "Deployment complete!"