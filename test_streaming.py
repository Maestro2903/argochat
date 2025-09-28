#!/usr/bin/env python3
"""
Test streaming functionality for NVIDIA API
"""

import requests
import json

# Test with proper session handling
session = requests.Session()

# Sign in first
auth_data = {
    "email": "test@example.com",
    "password": "testpassword123"
}

signin_response = session.post("http://localhost:8080/api/v1/auths/signin", json=auth_data)
if signin_response.status_code != 200:
    print(f"Login failed: {signin_response.text}")
    exit(1)

print("✅ Logged in successfully")

# Test streaming NVIDIA API
nvidia_payload = {
    "model": "nvidia/qwen3-coder-480b-a35b-instruct",
    "messages": [
        {"role": "user", "content": "Write a simple Python function that adds two numbers"}
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "max_tokens": 100,
    "stream": True
}

print("\n🧪 Testing NVIDIA API Streaming...")
try:
    nvidia_response = session.post("http://localhost:8080/nvidia/api/chat", json=nvidia_payload, stream=True)
    print(f"NVIDIA API response status: {nvidia_response.status_code}")

    if nvidia_response.status_code == 200:
        print("📡 Streaming response:")
        full_response = ""

        for line in nvidia_response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        print("\n✅ Stream completed successfully!")
                        break
                    try:
                        chunk_data = json.loads(data_str)
                        if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                            delta = chunk_data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            reasoning = delta.get('reasoning_content', '')
                            if reasoning:
                                print(f"🤔 {reasoning}", end='')
                            if content:
                                print(content, end='')
                                full_response += content
                    except json.JSONDecodeError:
                        continue

        print(f"\n\n✅ Full response received: {len(full_response)} characters")
        print(f"🎯 Response: {full_response[:200]}...")

    else:
        print(f"❌ Failed: {nvidia_response.text}")

except Exception as e:
    print(f"❌ Error testing NVIDIA streaming API: {e}")

print("\n🎉 All tests completed!")