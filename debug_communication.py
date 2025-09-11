"""
Debug script to show MCP communication flow
"""
import json

# This is what VS Code sends to your weather server
request_example = {
    "jsonrpc": "2.0",
    "id": 123,
    "method": "tools/call",
    "params": {
        "name": "get_temperature",
        "arguments": {
            "city": "Tokyo",
            "unit": "celsius"
        }
    }
}

# This is what your weather server responds with  
response_example = {
    "jsonrpc": "2.0",
    "id": 123,
    "result": {
        "content": [
            {
                "type": "text", 
                "text": "22.5"
            }
        ],
        "isError": False,
        "structuredContent": {
            "result": 22.5
        }
    }
}

print("🔄 MCP JSON-RPC Communication Flow")
print("=" * 50)
print("\n📤 VS Code → Weather Server:")
print(json.dumps(request_example, indent=2))
print("\n📥 Weather Server → VS Code:")
print(json.dumps(response_example, indent=2))
print("\n🎯 Result: 22.5°C temperature for Tokyo!")
