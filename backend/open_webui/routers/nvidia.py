"""
NVIDIA API Router for FLOAT CHAT
Provides integration with NVIDIA's API endpoints using OpenAI-compatible interface
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Optional, Union, List, Dict, Any

import aiohttp
import requests
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    APIRouter,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict
from starlette.background import BackgroundTask

from open_webui.models.users import UserModel
from open_webui.utils.misc import calculate_sha256
from open_webui.utils.payload import (
    apply_model_params_to_body_openai,
    apply_system_prompt_to_body,
)
from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.constants import ERROR_MESSAGES

log = logging.getLogger(__name__)
router = APIRouter()

# NVIDIA API Configuration
NVIDIA_API_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Available NVIDIA models with hardcoded API keys for direct access
NVIDIA_MODELS = [
    {
        "id": "nvidia/qwen3-coder-480b-a35b-instruct",
        "name": "Qwen3 Coder 480B A35B Instruct",
        "object": "model",
        "created": int(time.time()),
        "owned_by": "nvidia",
        "provider": "nvidia",
        "api_key": "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",
        "model_name": "qwen/qwen3-coder-480b-a35b-instruct"
    },
    {
        "id": "nvidia/moonshotai-kimi-k2-instruct-0905",
        "name": "Moonshot AI Kimi K2 Instruct 0905",
        "object": "model",
        "created": int(time.time()),
        "owned_by": "nvidia",
        "provider": "nvidia",
        "api_key": "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",
        "model_name": "moonshotai/kimi-k2-instruct-0905"
    },
    {
        "id": "nvidia/deepseek-r1-0528",
        "name": "DeepSeek R1 0528",
        "object": "model",
        "created": int(time.time()),
        "owned_by": "nvidia",
        "provider": "nvidia",
        "api_key": "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",
        "model_name": "deepseek-ai/deepseek-r1-0528"
    }
]


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.8
    max_tokens: Optional[int] = 4096
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None


class GenerateEmbeddingsForm(BaseModel):
    model: str
    input: Union[str, List[str]]


def get_model_info(model_id: str):
    """Get model information including API key"""
    # Remove nvidia/ prefix if present for matching
    clean_model_id = model_id.replace("nvidia/", "") if model_id.startswith("nvidia/") else model_id
    
    for model in NVIDIA_MODELS:
        # Check multiple possible matches
        if (model["id"] == model_id or 
            model["model_name"] == model_id or
            model["id"] == f"nvidia/{clean_model_id}" or
            model["model_name"] == clean_model_id or
            model["id"].replace("nvidia/", "") == clean_model_id):
            return model
    return None


def get_nvidia_api_key(model_id: str = None):
    """Get NVIDIA API key from hardcoded values based on model"""
    if model_id:
        model_info = get_model_info(model_id)
        if model_info and "api_key" in model_info:
            return model_info["api_key"]

    # Fallback to first available model's API key
    if NVIDIA_MODELS:
        return NVIDIA_MODELS[0]["api_key"]

    raise HTTPException(
        status_code=500,
        detail="NVIDIA API key not configured."
    )


def get_nvidia_headers(model_id: str = None):
    """Get headers for NVIDIA API requests"""
    return {
        "Authorization": f"Bearer {get_nvidia_api_key(model_id)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


async def get_all_models(request: Request, user: UserModel = None) -> dict:
    """Get all available NVIDIA models (called from models utility)"""
    try:
        # Return all models since API keys are hardcoded
        return {
            "models": NVIDIA_MODELS
        }
    except Exception as e:
        log.exception(f"Error getting NVIDIA models: {e}")
        return {"models": []}


async def get_nvidia_models(
    request: Request,
    url_idx: Optional[int] = None,
    user: UserModel = None
):
    """Get available NVIDIA models (API endpoint)"""
    return await get_all_models(request, user)


@router.get("/api/tags")
@router.get("/api/tags/{url_idx}")
async def get_nvidia_models_endpoint(
    request: Request,
    url_idx: Optional[int] = None
):
    """Get available NVIDIA models endpoint"""
    return await get_nvidia_models(request, url_idx, None)


@router.get("/api/version")
@router.get("/api/version/{url_idx}")
async def get_nvidia_version(
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user)
):
    """Get NVIDIA API version info"""
    return {
        "version": "1.0.0",
        "provider": "nvidia",
        "api_base": NVIDIA_API_BASE_URL
    }


@router.post("/api/chat")
async def generate_nvidia_chat_completion(
    request: Request,
    form_data: ChatCompletionRequest,
    user: UserModel = None
):
    """Generate chat completion using NVIDIA API"""
    try:
        log.info(f"NVIDIA chat completion request for model: {form_data.model}")

        # Validate messages
        if not form_data.messages:
            raise HTTPException(
                status_code=400,
                detail="Messages cannot be empty"
            )

        # Check for empty content in messages and provide helpful error
        for i, message in enumerate(form_data.messages):
            content = message.get("content", "")
            if not content or not content.strip():
                log.warning(f"Message {i} has empty content, rejecting request")
                raise HTTPException(
                    status_code=400,
                    detail=f"Message content cannot be empty. Please provide a valid message for the AI to respond to."
                )

        # Get model info and determine the correct model name for API
        model_info = get_model_info(form_data.model)
        if not model_info:
            log.error(f"Model {form_data.model} not found in NVIDIA_MODELS")
            log.error(f"Available models: {[m['id'] for m in NVIDIA_MODELS]}")
            raise HTTPException(
                status_code=404,
                detail=f"Model {form_data.model} not found"
            )
        
        log.info(f"Using model info: {model_info['model_name']} with API key: {model_info['api_key'][:10]}...")
        
        # Prepare the request payload
        payload = {
            "model": model_info["model_name"],  # Use the correct model name for API
            "messages": form_data.messages,
            "temperature": form_data.temperature,
            "top_p": form_data.top_p,
            "max_tokens": form_data.max_tokens,
            "stream": form_data.stream
        }
        
        if form_data.stop:
            payload["stop"] = form_data.stop

        headers = get_nvidia_headers(form_data.model)
        
        # Make request to NVIDIA API with timeout
        timeout = aiohttp.ClientTimeout(total=120)  # 2 minute timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{NVIDIA_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    log.error(f"NVIDIA API error: {response.status} - {error_text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"NVIDIA API error: {error_text}"
                    )
                
                if form_data.stream:
                    # Handle streaming response with reasoning content support
                    async def stream_generator():
                        try:
                            buffer = ""
                            async for chunk in response.content.iter_any():
                                if chunk:
                                    try:
                                        chunk_text = chunk.decode('utf-8')
                                        buffer += chunk_text

                                        # Process complete lines
                                        while '\n' in buffer:
                                            line, buffer = buffer.split('\n', 1)
                                            line = line.strip()

                                            if line.startswith('data: '):
                                                data_str = line[6:]  # Remove 'data: ' prefix
                                                if data_str == '[DONE]':
                                                    yield f"data: [DONE]\n\n".encode('utf-8')
                                                    return
                                                elif data_str:  # Only process non-empty data
                                                    try:
                                                        chunk_data = json.loads(data_str)
                                                        # Handle reasoning content for DeepSeek R1
                                                        if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                                            delta = chunk_data['choices'][0].get('delta', {})
                                                            reasoning_content = delta.get('reasoning_content')
                                                            if reasoning_content:
                                                                # Add reasoning content to the response
                                                                chunk_data['choices'][0]['delta']['reasoning_content'] = reasoning_content

                                                        yield f"data: {json.dumps(chunk_data)}\n\n".encode('utf-8')
                                                    except json.JSONDecodeError as e:
                                                        log.warning(f"Failed to parse JSON chunk: {data_str[:100]}... - {e}")
                                                        continue
                                            elif line and not line.startswith(':'):  # Skip comment lines
                                                yield f"{line}\n".encode('utf-8')
                                    except UnicodeDecodeError as e:
                                        log.warning(f"Failed to decode chunk: {e}")
                                        continue

                            # Process any remaining buffer
                            if buffer.strip():
                                if buffer.strip().startswith('data: '):
                                    data_str = buffer.strip()[6:]
                                    if data_str and data_str != '[DONE]':
                                        try:
                                            chunk_data = json.loads(data_str)
                                            yield f"data: {json.dumps(chunk_data)}\n\n".encode('utf-8')
                                        except json.JSONDecodeError:
                                            pass

                        except asyncio.CancelledError:
                            log.info("Stream cancelled by client")
                            yield f"data: [DONE]\n\n".encode('utf-8')
                        except Exception as e:
                            log.error(f"Error in stream generator: {e}")
                            error_chunk = {
                                "error": {
                                    "message": f"Streaming error: {str(e)}",
                                    "type": "stream_error"
                                }
                            }
                            yield f"data: {json.dumps(error_chunk)}\n\n".encode('utf-8')
                            yield f"data: [DONE]\n\n".encode('utf-8')

                    return StreamingResponse(
                        stream_generator(),
                        media_type="text/plain"
                    )
                else:
                    # Handle non-streaming response
                    result = await response.json()
                    return result
                    
    except HTTPException:
        raise
    except Exception as e:
        log.exception(f"Error in NVIDIA chat completion: {e}")
        raise HTTPException(
            status_code=500,
            detail=ERROR_MESSAGES.DEFAULT(f"Error generating chat completion: {e}")
        )


@router.post("/api/generate")
async def generate_nvidia_completion(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user)
):
    """Generate text completion using NVIDIA API (Ollama-compatible endpoint)"""
    try:
        # Convert Ollama format to OpenAI format
        messages = []
        if "system" in form_data:
            messages.append({"role": "system", "content": form_data["system"]})
        
        messages.append({"role": "user", "content": form_data.get("prompt", "")})
        
        # Get model info to ensure we use a valid model
        model_id = form_data.get("model", "nvidia/llama-3.1-nemotron-70b-instruct")
        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(
                status_code=404,
                detail=f"Model {model_id} not found"
            )
        
        # Create chat completion request
        chat_request = ChatCompletionRequest(
            model=model_id,
            messages=messages,
            temperature=form_data.get("temperature", 0.7),
            top_p=form_data.get("top_p", 0.8),
            max_tokens=form_data.get("max_tokens", 4096),
            stream=form_data.get("stream", False)
        )
        
        return await generate_nvidia_chat_completion(request, chat_request, user)
        
    except Exception as e:
        log.exception(f"Error in NVIDIA text completion: {e}")
        raise HTTPException(
            status_code=500,
            detail=ERROR_MESSAGES.DEFAULT(f"Error generating completion: {e}")
        )


@router.post("/api/embeddings")
async def generate_nvidia_embeddings(
    request: Request,
    form_data: GenerateEmbeddingsForm,
    user=Depends(get_verified_user)
):
    """Generate embeddings using NVIDIA API"""
    try:
        # Get model info and determine the correct model name for API
        model_info = get_model_info(form_data.model)
        if not model_info:
            raise HTTPException(
                status_code=404,
                detail=f"Model {form_data.model} not found"
            )
        
        payload = {
            "model": model_info["model_name"],
            "input": form_data.input
        }
        
        headers = get_nvidia_headers(form_data.model)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{NVIDIA_API_BASE_URL}/embeddings",
                json=payload,
                headers=headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    log.error(f"NVIDIA embeddings API error: {response.status} - {error_text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"NVIDIA embeddings API error: {error_text}"
                    )
                
                result = await response.json()
                return result
                
    except HTTPException:
        raise
    except Exception as e:
        log.exception(f"Error generating NVIDIA embeddings: {e}")
        raise HTTPException(
            status_code=500,
            detail=ERROR_MESSAGES.DEFAULT(f"Error generating embeddings: {e}")
        )


@router.post("/api/pull")
async def pull_nvidia_model(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user)
):
    """Mock endpoint for model pulling (NVIDIA models are cloud-based)"""
    model_name = form_data.get("name", "")
    
    # Simulate successful pull for NVIDIA models
    if any(model["id"].endswith(model_name) for model in NVIDIA_MODELS):
        return {
            "status": "success",
            "message": f"NVIDIA model {model_name} is ready (cloud-based)"
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"NVIDIA model {model_name} not found"
        )


@router.post("/api/push")
async def push_nvidia_model(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user)
):
    """Mock endpoint for model pushing (not supported for NVIDIA)"""
    raise HTTPException(
        status_code=501,
        detail="Model pushing is not supported for NVIDIA cloud models"
    )


@router.delete("/api/delete")
async def delete_nvidia_model(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user)
):
    """Mock endpoint for model deletion (not supported for NVIDIA)"""
    raise HTTPException(
        status_code=501,
        detail="Model deletion is not supported for NVIDIA cloud models"
    )
