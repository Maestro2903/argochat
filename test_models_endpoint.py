#!/usr/bin/env python3
"""
Test the main models endpoint to see if NVIDIA models are included
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from open_webui.utils.models import get_all_base_models, fetch_nvidia_models
from fastapi import Request
from unittest.mock import Mock

async def test_models():
    """Test model fetching"""
    print("🧪 Testing model fetching...")
    
    # Create a mock request object
    mock_request = Mock(spec=Request)
    mock_request.app.state.config.ENABLE_OPENAI_API = False
    mock_request.app.state.config.ENABLE_OLLAMA_API = False
    
    print("\n1. Testing NVIDIA models fetch directly:")
    nvidia_models = await fetch_nvidia_models(mock_request, None)
    print(f"   Found {len(nvidia_models)} NVIDIA models")
    for model in nvidia_models:
        print(f"   - {model['id']} ({model['name']})")
    
    print("\n2. Testing all base models:")
    try:
        all_models = await get_all_base_models(mock_request, None)
        print(f"   Found {len(all_models)} total models")
        
        nvidia_count = sum(1 for model in all_models if model.get('provider') == 'nvidia')
        print(f"   NVIDIA models in base models: {nvidia_count}")
        
        for model in all_models:
            if model.get('provider') == 'nvidia':
                print(f"   - {model['id']} ({model['name']})")
                
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_models())
