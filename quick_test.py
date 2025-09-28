#!/usr/bin/env python3
"""
Quick test script to verify NVIDIA API is working
"""

import requests
import json

# Test with proper session handling
session = requests.Session()

# Register/login first
auth_data = {
    "email": "test@example.com",
    "password": "testpassword123",
    "name": "Test User"
}

# Try to sign up
try:
    signup_response = session.post("http://localhost:8080/api/v1/auths/signup", json=auth_data)
    print(f"Signup response: {signup_response.status_code}")
    if signup_response.status_code in [200, 409]:  # 409 if user already exists
        print("User created or already exists")
    else:
        print(f"Signup failed: {signup_response.text}")
except Exception as e:
    print(f"Signup error: {e}")

# Try to sign in
try:
    signin_response = session.post("http://localhost:8080/api/v1/auths/signin", json={
        "email": auth_data["email"],
        "password": auth_data["password"]
    })
    print(f"Signin response: {signin_response.status_code}")
    if signin_response.status_code == 200:
        auth_data = signin_response.json()
        print("Login successful")
        print(f"Token: {auth_data.get('token', 'No token')[:20]}...")
    else:
        print(f"Signin failed: {signin_response.text}")
        exit(1)
except Exception as e:
    print(f"Signin error: {e}")
    exit(1)

# Now test the NVIDIA API
nvidia_payload = {
    "model": "nvidia/qwen3-coder-480b-a35b-instruct",
    "messages": [
        {"role": "user", "content": "Hello! Can you help me write a simple Python function?"}
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "max_tokens": 100,
    "stream": False
}

print("\n🧪 Testing NVIDIA API...")
try:
    nvidia_response = session.post("http://localhost:8080/nvidia/api/chat", json=nvidia_payload)
    print(f"NVIDIA API response status: {nvidia_response.status_code}")

    if nvidia_response.status_code == 200:
        result = nvidia_response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(f"✅ Success! Response: {content[:100]}...")
        else:
            print(f"✅ Got response but unexpected format: {result}")
    else:
        print(f"❌ Failed: {nvidia_response.text}")

except Exception as e:
    print(f"❌ Error testing NVIDIA API: {e}")