@echo off
REM MCP Servers Startup Script
REM This script helps start all your custom MCP servers for VS Code integration

echo 🚀 Starting MCP Servers for VS Code Integration...
echo.

cd /d "c:\wizr\mcp Server POC\python-sdk-Mcp"

echo ✅ MCP Servers configured in VS Code:
echo    • weather - Weather information service
echo    • vscode-assistant - VS Code development tools  
echo    • echo - Text echo and resource server
echo    • github-tools - GitHub repository tools
echo.

echo 🔧 To test individual servers manually:
echo.
echo Weather Service:
echo uv run python examples/fastmcp/weather_structured.py --server
echo.
echo VS Code Assistant:
echo uv run python examples/custom_servers/vscode_assistant.py --server
echo.
echo Echo Server:
echo uv run python examples/fastmcp/echo.py --server
echo.
echo GitHub Tools:
echo uv run python examples/custom_servers/github_mcp_server.py --server
echo.

echo 📋 Your MCP servers should now appear in VS Code Extensions panel under "MCP SERVERS - INSTALLED"
echo 💬 Use them in Copilot Chat with: @mcp [your request]
echo.

echo Examples:
echo   @mcp what's the weather in London?
echo   @mcp analyze my workspace
echo   @mcp echo "Hello World"
echo   @mcp get repository information
echo.

pause
