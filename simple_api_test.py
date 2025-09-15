#!/usr/bin/env python3
"""
Simple test for your Prompt API
"""

import asyncio
import httpx
import json

async def test_api():
    """Test the prompt API directly"""
    print("🧪 Testing Prompt API")
    print("=" * 30)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print("📡 Fetching prompts from API...")
            response = await client.get("http://34.74.137.80/prompt-storage/files")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API Response successful!")
                print(f"   Status: {data.get('status')}")
                print(f"   Message: {data.get('message')}")
                print(f"   Total files: {len(data.get('data', []))}")
                
                print("\n📁 Available Prompts:")
                for i, file_info in enumerate(data.get('data', []), 1):
                    print(f"   {i}. {file_info['file_name']}")
                    print(f"      Size: {file_info['size']} bytes")
                    print(f"      Updated: {file_info['updated'][:10]}")
                    print()
                
                # Test fetching one prompt content
                if data.get('data'):
                    first_prompt = data['data'][0]
                    print(f"🔍 Testing content fetch for: {first_prompt['file_name']}")
                    
                    content_response = await client.get(first_prompt['signed_url'])
                    if content_response.status_code == 200:
                        content = content_response.text
                        preview = content[:200] + "..." if len(content) > 200 else content
                        print("✅ Content fetched successfully!")
                        print(f"   Content preview: {preview}")
                    else:
                        print(f"❌ Failed to fetch content: {content_response.status_code}")
                
                return True
            else:
                print(f"❌ API returned status code: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api())
    
    if success:
        print("\n🎉 API Test Passed!")
        print("Your Prompt API is working correctly.")
        print("\n🚀 Next Steps:")
        print("1. Restart VS Code to load the new MCP server")
        print("2. In GitHub Copilot Chat, try:")
        print("   - 'List all available prompts'")
        print("   - 'Get the frontend development prompt'")
        print("   - 'Show me the UI prompt'")
    else:
        print("\n❌ API Test Failed!")
        print("Please check your API endpoint and try again.")
