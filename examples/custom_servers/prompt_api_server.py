#!/usr/bin/env python3
"""
Dynamic Prompt API MCP Server

This server fetches prompts from your API and dynamically creates tools for each prompt.
Each prompt becomes a separate tool that can be called from GitHub Copilot Chat.
"""

import asyncio
import httpx
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Prompt API Server")

# Configuration
PROMPT_API_URL = "http://34.74.137.80/prompt-storage/files"
CACHE_DURATION = 300  # 5 minutes cache
_cached_prompts = {}
_cache_timestamp = None

class PromptCache:
    """Simple cache for prompt data"""
    
    @staticmethod
    async def get_cached_prompts() -> Optional[List[Dict]]:
        global _cached_prompts, _cache_timestamp
        
        # Check if cache is still valid
        if _cache_timestamp and _cached_prompts:
            age = (datetime.now(timezone.utc) - _cache_timestamp).total_seconds()
            if age < CACHE_DURATION:
                return _cached_prompts
        
        return None
    
    @staticmethod
    async def update_cache(prompts: List[Dict]):
        global _cached_prompts, _cache_timestamp
        _cached_prompts = prompts
        _cache_timestamp = datetime.now(timezone.utc)

async def fetch_prompts_from_api() -> List[Dict]:
    """Fetch prompt list from the API"""
    try:
        # Check cache first
        cached = await PromptCache.get_cached_prompts()
        if cached:
            return cached
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(PROMPT_API_URL)
            response.raise_for_status()
            
            data = response.json()
            if data.get("status") == 200 and "data" in data:
                prompts = data["data"]
                await PromptCache.update_cache(prompts)
                return prompts
            else:
                return []
                
    except Exception as e:
        print(f"Error fetching prompts from API: {e}")
        return []

async def fetch_prompt_content(signed_url: str) -> str:
    """Fetch the actual prompt content from the signed URL"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(signed_url)
            response.raise_for_status()
            return response.text
    except Exception as e:
        print(f"Error fetching prompt content: {e}")
        return f"Error loading prompt: {str(e)}"

def sanitize_tool_name(file_name: str) -> str:
    """Convert file name to valid tool name"""
    # Remove .txt extension and convert to snake_case
    name = file_name.replace('.txt', '').replace('-', '_').replace(' ', '_')
    # Remove any non-alphanumeric characters except underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    # Ensure it starts with a letter
    if name and name[0].isdigit():
        name = f"prompt_{name}"
    return name or "unknown_prompt"

def create_tool_description(file_name: str, size: int, updated: str) -> str:
    """Create a descriptive tool description"""
    # Parse the file name to create a meaningful description
    base_name = file_name.replace('.txt', '').replace('-', ' ').replace('_', ' ').title()
    
    # Create contextual descriptions based on file names
    if 'test' in file_name.lower():
        category = "Testing & Quality Assurance"
    elif 'ui' in file_name.lower() or 'frontend' in file_name.lower() or 'fes' in file_name.lower():
        category = "Frontend Development"
    elif 'be' in file_name.lower() or 'backend' in file_name.lower():
        category = "Backend Development"
    elif 'api' in file_name.lower():
        category = "API Development"
    else:
        category = "General Development"
    
    return f"Get {base_name} prompt for {category}. Size: {size} bytes. Last updated: {updated[:10]}"

# Core MCP Tools
@mcp.tool()
async def list_available_prompts() -> Dict[str, Any]:
    """List all available prompts from the API with their metadata"""
    try:
        prompts = await fetch_prompts_from_api()
        
        if not prompts:
            return {
                "status": "error",
                "message": "No prompts available or API error",
                "prompts": []
            }
        
        formatted_prompts = []
        for prompt in prompts:
            tool_name = sanitize_tool_name(prompt["file_name"])
            formatted_prompts.append({
                "file_name": prompt["file_name"],
                "tool_name": tool_name,
                "size": prompt["size"],
                "content_type": prompt["content_type"],
                "updated": prompt["updated"],
                "expires_at": prompt["expires_at"],
                "description": create_tool_description(
                    prompt["file_name"], 
                    prompt["size"], 
                    prompt["updated"]
                )
            })
        
        return {
            "status": "success",
            "total_prompts": len(formatted_prompts),
            "prompts": formatted_prompts,
            "cache_info": {
                "cached": _cache_timestamp is not None,
                "cache_age": (datetime.now(timezone.utc) - _cache_timestamp).total_seconds() if _cache_timestamp else 0
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list prompts: {str(e)}",
            "prompts": []
        }

@mcp.tool()
async def get_prompt_by_name(file_name: str) -> Dict[str, Any]:
    """Get a specific prompt content by file name"""
    try:
        prompts = await fetch_prompts_from_api()
        
        # Find the prompt
        target_prompt = None
        for prompt in prompts:
            if prompt["file_name"].lower() == file_name.lower():
                target_prompt = prompt
                break
        
        if not target_prompt:
            available_files = [p["file_name"] for p in prompts]
            return {
                "status": "error",
                "message": f"Prompt '{file_name}' not found",
                "available_files": available_files
            }
        
        # Fetch the content
        content = await fetch_prompt_content(target_prompt["signed_url"])
        
        return {
            "status": "success",
            "file_name": target_prompt["file_name"],
            "content": content,
            "metadata": {
                "size": target_prompt["size"],
                "updated": target_prompt["updated"],
                "content_type": target_prompt["content_type"]
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get prompt: {str(e)}"
        }

# Dynamic prompt tools - these will be created based on API response
@mcp.tool()
async def get_fes_prompt() -> Dict[str, Any]:
    """Get Frontend (FES) development prompt for React/Vue.js projects"""
    return await get_prompt_by_name("fes-prompt.txt")

@mcp.tool()
async def get_fes_unit_test_prompt() -> Dict[str, Any]:
    """Get Frontend unit testing prompt for Jest/Vitest/Cypress testing"""
    return await get_prompt_by_name("fes-unit-test-prompt.txt")

@mcp.tool()
async def get_wizr_be_prompt() -> Dict[str, Any]:
    """Get Backend development prompt for Node.js/Python/Java APIs"""
    return await get_prompt_by_name("wizr-be-prompt.txt")

@mcp.tool()
async def get_wizr_ui_api_integration_prompt() -> Dict[str, Any]:
    """Get UI API integration prompt for connecting frontend to backend services"""
    return await get_prompt_by_name("wizr-ui-api-integration-prompt.txt")

@mcp.tool()
async def get_wizr_ui_prompt() -> Dict[str, Any]:
    """Get UI development prompt for modern web interfaces and components"""
    return await get_prompt_by_name("wizr-ui-prompt.txt")

@mcp.tool()
async def refresh_prompt_cache() -> Dict[str, Any]:
    """Force refresh the prompt cache to get latest prompts from API"""
    try:
        global _cached_prompts, _cache_timestamp
        _cached_prompts = {}
        _cache_timestamp = None
        
        prompts = await fetch_prompts_from_api()
        
        return {
            "status": "success",
            "message": "Cache refreshed successfully",
            "total_prompts": len(prompts),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to refresh cache: {str(e)}"
        }

@mcp.tool()
async def search_prompts(keyword: str) -> Dict[str, Any]:
    """Search for prompts by keyword in file names"""
    try:
        prompts = await fetch_prompts_from_api()
        
        # Search in file names
        matching_prompts = []
        for prompt in prompts:
            if keyword.lower() in prompt["file_name"].lower():
                tool_name = sanitize_tool_name(prompt["file_name"])
                matching_prompts.append({
                    "file_name": prompt["file_name"],
                    "tool_name": tool_name,
                    "size": prompt["size"],
                    "updated": prompt["updated"],
                    "description": create_tool_description(
                        prompt["file_name"],
                        prompt["size"],
                        prompt["updated"]
                    )
                })
        
        return {
            "status": "success",
            "keyword": keyword,
            "matches_found": len(matching_prompts),
            "prompts": matching_prompts
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search prompts: {str(e)}"
        }

# Resource endpoints for prompt metadata
@mcp.resource("prompt://metadata")
async def get_prompt_metadata() -> str:
    """Get metadata about all available prompts"""
    try:
        result = await list_available_prompts()
        if result["status"] == "success":
            metadata = {
                "total_prompts": result["total_prompts"],
                "prompts": result["prompts"],
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "api_endpoint": PROMPT_API_URL
            }
            return f"Prompt Metadata:\n{metadata}"
        else:
            return f"Error getting metadata: {result['message']}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    if "--server" in sys.argv:
        print("Prompt API MCP Server starting...")
        print(f"API Endpoint: {PROMPT_API_URL}")
        print(f"Cache Duration: {CACHE_DURATION} seconds")
        print("Available tools:")
        print("  - list_available_prompts: List all prompts from API")
        print("  - get_prompt_by_name: Get specific prompt by file name")
        print("  - get_fes_prompt: Frontend development prompt")
        print("  - get_fes_unit_test_prompt: Frontend testing prompt")
        print("  - get_wizr_be_prompt: Backend development prompt")
        print("  - get_wizr_ui_api_integration_prompt: API integration prompt")
        print("  - get_wizr_ui_prompt: UI development prompt")
        print("  - refresh_prompt_cache: Refresh prompt cache")
        print("  - search_prompts: Search prompts by keyword")
        print("Server ready for connections!")
        
        mcp.run(transport="stdio")
    else:
        print("Usage: python prompt_api_server.py --server")
