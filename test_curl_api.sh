#!/bin/bash

# Test NVIDIA API with curl
echo "🚀 Testing NVIDIA API with curl"
echo "================================"

# Test Qwen3 Coder
echo ""
echo "🧪 Testing Qwen3 Coder 480B..."
curl -s -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3-coder-480b-a35b-instruct",
    "messages": [{"role": "user", "content": "Hello! Say just: API working"}],
    "temperature": 0.7,
    "max_tokens": 20
  }' | jq -r '.choices[0].message.content // "Error: " + (.error.message // "Unknown error")'

# Test DeepSeek R1
echo ""
echo "🧪 Testing DeepSeek R1..."
curl -s -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/deepseek-r1-0528",
    "messages": [{"role": "user", "content": "Hello! Say just: API working"}],
    "temperature": 0.7,
    "max_tokens": 20
  }' | jq -r '.choices[0].message.content // "Error: " + (.error.message // "Unknown error")'

echo ""
echo "✅ API tests completed!"
