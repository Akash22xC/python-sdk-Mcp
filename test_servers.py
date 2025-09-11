#!/usr/bin/env python3
"""
Test script to verify MCP servers are working correctly
"""
import subprocess
import sys
import time

def test_server(name, script_path):
    """Test if a server starts without errors"""
    print(f"\n=== Testing {name} ===")
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, script_path, "--server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="."
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if process is still running (good sign)
        if process.poll() is None:
            print(f"✅ {name} started successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {name} failed to start")
            if stdout:
                print(f"STDOUT: {stdout}")
            if stderr:
                print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {name}: {e}")
        return False

def main():
    print("Testing MCP Servers...")
    
    servers = [
        ("Weather Server", "examples/fastmcp/weather_structured.py"),
        ("Echo Server", "examples/fastmcp/echo.py"),
        ("VS Code Assistant", "examples/custom_servers/vscode_assistant.py")
    ]
    
    results = []
    for name, path in servers:
        results.append(test_server(name, path))
    
    print("\n=== Summary ===")
    for i, (name, _) in enumerate(servers):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{name}: {status}")
    
    if all(results):
        print("\n🎉 All servers are working correctly!")
        print("You can now use them with VS Code MCP integration.")
    else:
        print("\n⚠️ Some servers had issues. Check the output above.")

if __name__ == "__main__":
    main()
