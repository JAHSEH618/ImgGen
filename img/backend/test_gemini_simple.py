#!/usr/bin/env python3
# Simple test script for Gemini API
import os
import time
from google import genai
from google.genai import types

def test_gemini():
    """Test basic Gemini API functionality"""
    print("Testing Gemini API...")
    
    # Clear proxy variables
    for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
        if proxy_var in os.environ:
            print(f"Clearing proxy variable: {proxy_var}")
            del os.environ[proxy_var]
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found")
        return False
    
    try:
        # Create client
        client = genai.Client(api_key=api_key)
        print("✅ Client created successfully")
        
        # Test simple text generation (non-image)
        print("Testing simple text generation...")
        start_time = time.time()
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=["Say hello in one word"]
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Simple text generation completed in {elapsed:.1f}s")
        print(f"Response: {response.text}")
        
        # Test image generation model
        print("\nTesting image generation model...")
        start_time = time.time()
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Generate a simple red circle"),
                ],
            ),
        ]
        
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        )
        
        # Try non-streaming first
        print("Trying non-streaming approach...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents,
            config=config
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Image generation completed in {elapsed:.1f}s")
        
        # Check response parts
        if response.candidates and response.candidates[0].content:
            for i, part in enumerate(response.candidates[0].content.parts):
                if part.text:
                    print(f"Text part {i}: {part.text}")
                elif part.inline_data:
                    print(f"Image part {i}: {part.inline_data.mime_type}, size: {len(part.inline_data.data)} bytes")
        
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error after {elapsed:.1f}s: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini()
    exit(0 if success else 1)