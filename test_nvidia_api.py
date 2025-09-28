#!/usr/bin/env python3
"""
Test script for NVIDIA API integration in FloatChat
Tests all three configured models with both streaming and non-streaming requests
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from open_webui.routers.nvidia import (
    generate_nvidia_chat_completion,
    ChatCompletionRequest,
    NVIDIA_MODELS
)
from fastapi import Request
from unittest.mock import Mock

# Color codes for output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'  # No Color

def log(message, color=Colors.BLUE):
    print(f"{color}[TEST] {message}{Colors.NC}")

def success(message):
    log(f"✅ {message}", Colors.GREEN)

def error(message):
    log(f"❌ {message}", Colors.RED)

def info(message):
    log(f"ℹ️  {message}", Colors.BLUE)

def warning(message):
    log(f"⚠️  {message}", Colors.YELLOW)

async def test_model(model_id, test_streaming=True):
    """Test a specific NVIDIA model"""
    info(f"Testing model: {model_id}")
    
    # Create a mock request object
    mock_request = Mock(spec=Request)
    
    # Test data
    test_messages = [
        {"role": "user", "content": "Hello! Please respond with a simple greeting."}
    ]
    
    try:
        # Test non-streaming first
        info(f"Testing non-streaming response for {model_id}")
        request_data = ChatCompletionRequest(
            model=model_id,
            messages=test_messages,
            temperature=0.7,
            max_tokens=100,
            stream=False
        )
        
        response = await generate_nvidia_chat_completion(
            request=mock_request,
            form_data=request_data,
            user=None
        )
        
        if hasattr(response, 'body'):
            # Handle StreamingResponse
            content = b""
            async for chunk in response.body_iterator:
                content += chunk
            response_text = content.decode('utf-8')
        else:
            response_text = str(response)
        
        success(f"Non-streaming response received for {model_id}")
        print(f"{Colors.PURPLE}Response preview: {response_text[:200]}...{Colors.NC}")
        
        if test_streaming:
            # Test streaming
            info(f"Testing streaming response for {model_id}")
            streaming_request = ChatCompletionRequest(
                model=model_id,
                messages=test_messages,
                temperature=0.7,
                max_tokens=100,
                stream=True
            )
            
            streaming_response = await generate_nvidia_chat_completion(
                request=mock_request,
                form_data=streaming_request,
                user=None
            )
            
            success(f"Streaming response initiated for {model_id}")
            
            # Read first few chunks
            chunk_count = 0
            async for chunk in streaming_response.body_iterator:
                chunk_count += 1
                if chunk_count <= 3:  # Only show first 3 chunks
                    chunk_text = chunk.decode('utf-8')
                    print(f"{Colors.PURPLE}Chunk {chunk_count}: {chunk_text.strip()}{Colors.NC}")
                if chunk_count >= 5:  # Stop after 5 chunks to avoid long output
                    break
            
            success(f"Streaming test completed for {model_id} ({chunk_count} chunks received)")
        
        return True
        
    except Exception as e:
        error(f"Test failed for {model_id}: {str(e)}")
        return False

async def main():
    """Main test function"""
    log("🚀 Starting NVIDIA API Tests", Colors.GREEN)
    print()
    
    # Display available models
    info("Available NVIDIA models:")
    for i, model in enumerate(NVIDIA_MODELS, 1):
        print(f"  {i}. {model['id']} ({model['name']})")
    print()
    
    # Test each model
    results = {}
    for model in NVIDIA_MODELS:
        model_id = model['id']
        print(f"\n{'='*60}")
        log(f"Testing {model['name']}", Colors.YELLOW)
        print(f"{'='*60}")
        
        try:
            success_result = await test_model(model_id, test_streaming=True)
            results[model_id] = success_result
        except Exception as e:
            error(f"Critical error testing {model_id}: {str(e)}")
            results[model_id] = False
        
        print()
    
    # Summary
    print(f"\n{'='*60}")
    log("TEST SUMMARY", Colors.GREEN)
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for model_id, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {model_id}: {status}")
    
    print(f"\nOverall: {passed}/{total} models passed")
    
    if passed == total:
        success("All tests passed! 🎉")
        return 0
    else:
        error(f"{total - passed} tests failed")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        warning("Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        error(f"Test runner failed: {str(e)}")
        sys.exit(1)
