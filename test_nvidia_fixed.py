#!/usr/bin/env python3
"""
Fixed test script for NVIDIA API with actual content
"""

from openai import OpenAI
import json

# Test 1: Kimi K2 with actual content
print("🧪 Testing Kimi K2 with actual content...")
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion = client.chat.completions.create(
    model="moonshotai/kimi-k2-instruct-0905",
    messages=[{"role": "user", "content": "Write a simple Python function that adds two numbers"}],
    temperature=0.6,
    top_p=0.9,
    max_tokens=200,
    stream=True
)

print("📡 Kimi K2 Response:")
for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

print("\n" + "="*50)

# Test 2: Qwen3 Coder with actual content
print("🧪 Testing Qwen3 Coder with actual content...")
client2 = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion2 = client2.chat.completions.create(
    model="qwen/qwen3-coder-480b-a35b-instruct",
    messages=[{"role": "user", "content": "Explain what a Python function is in simple terms"}],
    temperature=0.7,
    top_p=0.8,
    max_tokens=200,
    stream=True
)

print("📡 Qwen3 Coder Response:")
for chunk in completion2:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

print("\n" + "="*50)

# Test 3: DeepSeek R1 with actual content and reasoning
print("🧪 Testing DeepSeek R1 with actual content...")
client3 = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion3 = client3.chat.completions.create(
    model="deepseek-ai/deepseek-r1-0528",
    messages=[{"role": "user", "content": "What is 2 + 2? Think step by step."}],
    temperature=0.6,
    top_p=0.7,
    max_tokens=200,
    stream=True
)

print("📡 DeepSeek R1 Response:")
for chunk in completion3:
    reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
    if reasoning:
        print(f"🤔 Reasoning: {reasoning}", end="")
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

print("\n\n✅ All tests completed!")