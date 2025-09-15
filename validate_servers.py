#!/usr/bin/env python3
"""
Validation script for Prompt API MCP Server
Tests all configurations and functionality
"""

import json
import subprocess
import asyncio
import httpx
from pathlib import Path

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("🔧 Testing Dependencies")
    print("-" * 25)
    
    try:
        import httpx
        print("✅ httpx installed")
    except ImportError:
        print("❌ httpx missing - run: uv add httpx")
        return False
    
    try:
        from mcp.server.fastmcp import FastMCP
        print("✅ FastMCP available")
    except ImportError:
        print("❌ FastMCP missing - check MCP SDK installation")
        return False
    
    return True

async def test_api_connectivity():
    """Test API connectivity"""
    print("\n🌐 Testing API Connectivity")
    print("-" * 30)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://34.74.137.80/prompt-storage/files")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API accessible")
                print(f"   Found {len(data.get('data', []))} prompts")
                return True
            else:
                print(f"❌ API returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False

def test_server_startup():
    """Test if the MCP server starts correctly"""
    print("\n🚀 Testing Server Startup")
    print("-" * 27)
    
    try:
        # Test server startup with a timeout
        process = subprocess.Popen(
            ["uv", "run", "python", "examples/custom_servers/prompt_api_server.py", "--server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # Wait a bit for startup
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
        
        if "Server ready for connections!" in stdout:
            print("✅ Server starts successfully")
            return True
        else:
            print(f"❌ Server startup issue")
            if stderr:
                print(f"   Error: {stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Server test failed: {str(e)}")
        return False

def test_vs_code_config():
    """Test VS Code configuration"""
    print("\n⚙️ Testing VS Code Config")
    print("-" * 26)
    
    # Check project config
    project_config = Path(".vscode/settings.json")
    if project_config.exists():
        try:
            with open(project_config, 'r') as f:
                config = json.load(f)
            
            if "prompt-api" in config.get("mcp.servers", {}):
                print("✅ Project MCP config found")
            else:
                print("❌ prompt-api server not found in project config")
                return False
                
        except Exception as e:
            print(f"❌ Error reading project config: {e}")
            return False
    else:
        print("❌ .vscode/settings.json not found")
        return False
    
    # Check global config
    global_config = Path.home() / "AppData/Roaming/Code/User/mcp.json"
    if global_config.exists():
        try:
            with open(global_config, 'r') as f:
                config = json.load(f)
            
            if "prompt-api" in config.get("servers", {}):
                print("✅ Global MCP config found")
            else:
                print("❌ prompt-api server not found in global config")
                return False
                
        except Exception as e:
            print(f"❌ Error reading global config: {e}")
            return False
    else:
        print("❌ Global mcp.json not found")
        return False
    
    return True

async def main():
    """Run all validation tests"""
    print("🧪 Prompt API MCP Server Validation")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("API Connectivity", lambda: asyncio.run(test_api_connectivity())),
        ("VS Code Config", test_vs_code_config),
        ("Server Startup", test_server_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Validation Summary")
    print("=" * 20)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        print("Your Prompt API MCP Server is ready to use!")
        print("\n🚀 Next steps:")
        print("1. Restart VS Code")
        print("2. In Copilot Chat, try: 'List all available prompts'")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
