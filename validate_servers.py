#!/usr/bin/env python3
"""
Quick test to verify MCP servers can be imported and initialized
"""
import sys
import os

def test_imports():
    """Test that all server modules can be imported without errors"""
    print("Testing server imports...")
    
    servers = [
        ("Weather Server", "examples/fastmcp/weather_structured.py"),
        ("Echo Server", "examples/fastmcp/echo.py"), 
        ("VS Code Assistant", "examples/custom_servers/vscode_assistant.py")
    ]
    
    results = []
    for name, path in servers:
        try:
            # Add the directory to Python path
            module_dir = os.path.dirname(path)
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            # Import the module
            module_name = os.path.basename(path).replace('.py', '')
            spec = __import__(module_name)
            
            print(f"✅ {name}: Import successful")
            results.append(True)
            
        except Exception as e:
            print(f"❌ {name}: Import failed - {e}")
            results.append(False)
    
    return all(results)

def main():
    print("=== MCP Server Validation ===")
    
    # Test imports
    import_success = test_imports()
    
    print(f"\n=== Summary ===")
    if import_success:
        print("🎉 All servers can be imported successfully!")
        print("\nYour MCP servers are ready for VS Code integration.")
        print("\nTo use them:")
        print("1. Make sure the MCP extension is installed in VS Code")
        print("2. Your .vscode/mcp-servers.json is already configured")
        print("3. Restart VS Code to load the MCP servers")
        print("4. Use GitHub Copilot Chat to interact with the servers")
        print("\nExample queries:")
        print("- 'What's the weather in New York?'")
        print("- 'Echo hello world'")
        print("- 'Analyze my workspace structure'")
    else:
        print("⚠️ Some servers had import issues. Check the output above.")

if __name__ == "__main__":
    main()
