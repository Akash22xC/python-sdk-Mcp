#!/usr/bin/env python3
"""
Test script for Prompt API MCP Server
Tests all the tools and API integration
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

async def test_prompt_api_server():
    """Test the Prompt API MCP server tools"""
    print("🧪 Testing Prompt API MCP Server")
    print("=" * 50)
    
    # Test commands
    test_commands = [
        {
            "name": "List Available Prompts",
            "request": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "list_available_prompts",
                    "arguments": {}
                }
            }
        },
        {
            "name": "Get FES Prompt",
            "request": {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_fes_prompt",
                    "arguments": {}
                }
            }
        },
        {
            "name": "Search UI Prompts",
            "request": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_prompts",
                    "arguments": {"keyword": "ui"}
                }
            }
        },
        {
            "name": "Get Specific Prompt by Name",
            "request": {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_prompt_by_name",
                    "arguments": {"file_name": "wizr-be-prompt.txt"}
                }
            }
        }
    ]
    
    # Test each command
    for i, test in enumerate(test_commands, 1):
        print(f"\n🔸 Test {i}: {test['name']}")
        print("-" * 30)
        
        try:
            # Start the server process
            process = subprocess.Popen(
                ["uv", "run", "python", "examples/custom_servers/prompt_api_server.py", "--server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send the request
            request_json = json.dumps(test["request"])
            stdout, stderr = process.communicate(input=request_json, timeout=30)
            
            if process.returncode == 0:
                try:
                    # Parse the response
                    response = json.loads(stdout.strip())
                    
                    if "result" in response:
                        result = response["result"]
                        
                        # Print summary based on test type
                        if test["name"] == "List Available Prompts":
                            if result.get("status") == "success":
                                print(f"✅ Found {result.get('total_prompts', 0)} prompts")
                                for prompt in result.get("prompts", [])[:3]:  # Show first 3
                                    print(f"   - {prompt['file_name']} ({prompt['size']} bytes)")
                            else:
                                print(f"❌ Error: {result.get('message', 'Unknown error')}")
                        
                        elif "get_" in test["name"].lower():
                            if result.get("status") == "success":
                                content_preview = result.get("content", "")[:100] + "..." if len(result.get("content", "")) > 100 else result.get("content", "")
                                print(f"✅ Prompt loaded successfully")
                                print(f"   File: {result.get('file_name', 'Unknown')}")
                                print(f"   Size: {result.get('metadata', {}).get('size', 'Unknown')} bytes")
                                print(f"   Preview: {content_preview}")
                            else:
                                print(f"❌ Error: {result.get('message', 'Unknown error')}")
                        
                        elif test["name"] == "Search UI Prompts":
                            if result.get("status") == "success":
                                print(f"✅ Found {result.get('matches_found', 0)} matches for '{result.get('keyword', '')}'")
                                for prompt in result.get("prompts", []):
                                    print(f"   - {prompt['file_name']}")
                            else:
                                print(f"❌ Error: {result.get('message', 'Unknown error')}")
                    else:
                        print(f"❌ Unexpected response format")
                        print(f"   Response: {stdout[:200]}...")
                        
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON response")
                    print(f"   Raw output: {stdout[:200]}...")
            else:
                print(f"❌ Process failed with return code {process.returncode}")
                if stderr:
                    print(f"   Error: {stderr[:200]}...")
                    
        except subprocess.TimeoutExpired:
            process.kill()
            print("❌ Test timed out")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")

def test_api_connectivity():
    """Test direct API connectivity"""
    print("\n🌐 Testing Direct API Connectivity")
    print("=" * 40)
    
    try:
        import httpx
        import asyncio
        
        async def check_api():
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("http://34.74.137.80/prompt-storage/files")
                return response.status_code, response.json()
        
        status_code, data = asyncio.run(check_api())
        
        if status_code == 200:
            print("✅ API is accessible")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Total files: {len(data.get('data', []))}")
            
            # Show first few files
            for file_info in data.get('data', [])[:3]:
                print(f"   - {file_info['file_name']} ({file_info['size']} bytes)")
        else:
            print(f"❌ API returned status code: {status_code}")
            
    except ImportError:
        print("❌ httpx not installed - cannot test direct API connectivity")
        print("   Run: uv add httpx")
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 Prompt API MCP Server Test Suite")
    print("=" * 50)
    
    # Test API connectivity first
    test_api_connectivity()
    
    # Test MCP server tools
    asyncio.run(test_prompt_api_server())
    
    print("\n📊 Test Summary")
    print("=" * 20)
    print("✅ If all tests passed, your Prompt API MCP server is ready!")
    print("📝 To use in VS Code:")
    print("   1. Restart VS Code to load the new server")
    print("   2. In Copilot Chat, you can now use:")
    print("      - 'List all available prompts'")
    print("      - 'Get the frontend development prompt'")
    print("      - 'Show me the backend prompt'")
    print("      - 'Search for UI-related prompts'")
