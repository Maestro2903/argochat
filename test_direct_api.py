#!/usr/bin/env python3
"""
Direct API test for NVIDIA models
Tests the API keys directly without going through the FloatChat router
"""

import asyncio
import aiohttp
import json

# NVIDIA API configuration
NVIDIA_API_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Test models with their API keys
MODELS_TO_TEST = [
    {
        "name": "Qwen3 Coder 480B",
        "model": "qwen/qwen3-coder-480b-a35b-instruct",
        "api_key": "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"
    },
    {
        "name": "Kimi K2 Instruct",
        "model": "moonshotai/kimi-k2-instruct-0905",
        "api_key": "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"
    },
    {
        "name": "DeepSeek R1",
        "model": "deepseek-ai/deepseek-r1-0528",
        "api_key": "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"
    }
]

async def test_model_direct(model_info):
    """Test a model directly via NVIDIA API"""
    print(f"\n🧪 Testing {model_info['name']} ({model_info['model']})")
    
    headers = {
        "Authorization": f"Bearer {model_info['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "model": model_info['model'],
        "messages": [
            {"role": "user", "content": "Hello! Please respond with just 'API test successful'."}
        ],
        "temperature": 0.7,
        "max_tokens": 50,
        "stream": False
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=30)  # 30 second timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{NVIDIA_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                
                print(f"   Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    content = data.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
                    print(f"   ✅ Success: {content.strip()}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"   ❌ Error: {error_text}")
                    return False
                    
    except asyncio.TimeoutError:
        print(f"   ⏰ Timeout: Request took longer than 30 seconds")
        return False
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")
        return False

async def main():
    print("🚀 Direct NVIDIA API Test")
    print("=" * 50)
    
    results = []
    for model_info in MODELS_TO_TEST:
        success = await test_model_direct(model_info)
        results.append((model_info['name'], success))
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = 0
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {name}: {status}")
        if success:
            passed += 1
    
    print(f"\nResult: {passed}/{len(results)} models working")
    
    if passed == len(results):
        print("🎉 All API keys are working!")
    else:
        print("⚠️  Some API keys may have issues")

if __name__ == "__main__":
    asyncio.run(main())
