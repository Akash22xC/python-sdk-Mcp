"""
FastMCP Echo Server
"""

from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")


@mcp.tool()
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text


@mcp.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    return text


if __name__ == "__main__":
    import sys
    
    # Check for server mode
    if "--server" in sys.argv:
        print("Echo MCP Server starting...")
        print("Available tools: echo_tool")
        print("Available resources: echo://static, echo://{text}")
        print("Available prompts: echo")
        mcp.run(transport="stdio")
    else:
        # Run in test mode
        print("Echo Server Test Mode")
        print("Use --server to run as MCP server")
        
        # Test the tools
        print("\nTesting echo_tool:")
        result = echo_tool("Hello, MCP!")
        print(f"Result: {result}")
        
        print("\nTesting echo_resource:")
        static_result = echo_resource()
        print(f"Static resource: {static_result}")
        
        template_result = echo_template("World")
        print(f"Template resource: {template_result}")
