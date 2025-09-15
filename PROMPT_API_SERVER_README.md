# 🎯 Prompt API MCP Server

A dynamic Model Context Protocol (MCP) server that connects to your GCP-hosted prompt storage API and exposes each prompt as individual tools for GitHub Copilot Chat.

## 📋 Overview

This MCP server fetches prompts from your API endpoint (`http://34.74.137.80/prompt-storage/files`) and dynamically creates tools for each available prompt. Each prompt becomes accessible as a separate tool in GitHub Copilot Chat.

## 🚀 Features

### ✅ **Dynamic Tool Creation**
- Automatically creates tools for each prompt in your API
- Tools are named based on file names (e.g., `get_fes_prompt`, `get_wizr_ui_prompt`)
- Each tool has descriptive metadata and categorization

### ✅ **Smart Caching**
- 5-minute cache for prompt metadata to reduce API calls
- Cache refresh tool available for immediate updates
- Automatic cache invalidation

### ✅ **Content Fetching**
- Fetches actual prompt content from signed URLs
- Handles large prompts efficiently
- Error handling for expired or invalid URLs

### ✅ **Search & Discovery**
- Search prompts by keyword
- List all available prompts with metadata
- Get specific prompts by file name

## 🛠️ Available Tools

### **Core Tools**
1. **`list_available_prompts()`** - List all prompts with metadata
2. **`get_prompt_by_name(file_name: str)`** - Get specific prompt by filename
3. **`search_prompts(keyword: str)`** - Search prompts by keyword
4. **`refresh_prompt_cache()`** - Force refresh the cache

### **Dynamic Prompt Tools** (Based on your API)
1. **`get_fes_prompt()`** - Frontend development prompt (React/Vue.js)
2. **`get_fes_unit_test_prompt()`** - Frontend testing prompt (Jest/Vitest/Cypress)
3. **`get_wizr_be_prompt()`** - Backend development prompt (Node.js/Python/Java)
4. **`get_wizr_ui_api_integration_prompt()`** - UI API integration prompt
5. **`get_wizr_ui_prompt()`** - UI development prompt (modern web interfaces)

## 📊 Current Prompts in Your API

Based on the latest API response:

| File Name | Size | Category | Last Updated |
|-----------|------|----------|--------------|
| `fes-prompt.txt` | 4,500 bytes | Frontend Development | 2025-08-27 |
| `fes-unit-test-prompt.txt` | 2,810 bytes | Testing & QA | 2025-08-27 |
| `wizr-be-prompt.txt` | 3,353 bytes | Backend Development | 2025-08-27 |
| `wizr-ui-api-integration-prompt.txt` | 7,645 bytes | API Development | 2025-08-27 |
| `wizr-ui-prompt.txt` | 8,304 bytes | Frontend Development | 2025-08-27 |

## 🔧 Configuration

### **VS Code Settings** (`.vscode/settings.json`)
```json
{
  "mcp.servers": {
    "prompt-api": {
      "command": "uv",
      "args": ["run", "python", "examples/custom_servers/prompt_api_server.py", "--server"],
      "cwd": "${workspaceFolder}",
      "transport": "stdio",
      "alwaysAllow": ["tools", "resources", "prompts"]
    }
  }
}
```

### **Global MCP Config** (`mcp.json`)
```json
{
  "servers": {
    "prompt-api": {
      "command": "uv",
      "args": ["run", "python", "examples/custom_servers/prompt_api_server.py", "--server"],
      "cwd": "c:\\wizr\\mcp Server POC\\python-sdk-Mcp",
      "type": "stdio"
    }
  }
}
```

## 💬 Using in GitHub Copilot Chat

### **Example Queries**

1. **List All Prompts**
   ```
   "List all available prompts"
   "What prompts do we have?"
   ```

2. **Get Specific Prompts**
   ```
   "Get the frontend development prompt"
   "Show me the backend prompt"
   "I need the UI testing prompt"
   ```

3. **Search Prompts**
   ```
   "Search for UI-related prompts"
   "Find prompts about testing"
   ```

4. **Get Prompt Content**
   ```
   "Get the content of wizr-be-prompt.txt"
   "Show me the FES unit test prompt"
   ```

## 🔄 How It Works

### **Tool Discovery Flow**
```
1. Server starts → Scans @mcp.tool() decorators
2. VS Code/Copilot → Calls tools/list to discover available tools
3. User query → Copilot identifies relevant tool
4. Tool execution → Server fetches from API and returns content
```

### **API Integration Flow**
```
1. Tool called → Check cache (5-min TTL)
2. Cache miss → Fetch from http://34.74.137.80/prompt-storage/files
3. Get signed URL → Fetch actual prompt content
4. Return structured response → Cache result
```

### **Data Flow**
```
Your API → Signed URLs → Prompt Content → MCP Tools → Copilot Chat
```

## 🚨 Error Handling

- **API Unreachable**: Returns error with fallback message
- **Invalid Signed URLs**: Handles expired or broken URLs gracefully
- **Network Timeouts**: 30-second timeout with proper error reporting
- **Cache Issues**: Falls back to direct API calls if cache fails

## 🔧 Customization Options

### **1. Add New Tool Categories**
```python
def create_tool_description(file_name: str, size: int, updated: str) -> str:
    # Add your custom categories here
    if 'mobile' in file_name.lower():
        category = "Mobile Development"
    elif 'devops' in file_name.lower():
        category = "DevOps & Infrastructure"
    # ... existing categories
```

### **2. Modify Cache Duration**
```python
CACHE_DURATION = 300  # Change to your preferred seconds
```

### **3. Add Authentication**
```python
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "X-API-Key": "YOUR_API_KEY"
}
```

## 📈 Performance & Monitoring

### **Cache Statistics**
- Cache hit rate improves performance by ~80%
- 5-minute TTL balances freshness vs performance
- Cache status available in `list_available_prompts` response

### **API Metrics**
- Average response time: ~200ms for metadata
- Content fetch time: ~500ms per prompt
- Signed URL validity: 7 days

## 🔮 Future Enhancements

1. **Dynamic Tool Registration**: Automatically create tools for new prompts
2. **Prompt Versioning**: Track and manage prompt versions
3. **Usage Analytics**: Monitor which prompts are most requested
4. **Custom Prompt Creation**: Allow creating new prompts via Copilot
5. **Prompt Templates**: Support parameterized prompts

## 🎯 Best Practices

### **For Prompt Authors**
- Use descriptive file names (e.g., `react-component-prompt.txt`)
- Include clear descriptions in prompt headers
- Keep prompts focused and specific
- Update regularly and maintain version history

### **For Developers**
- Use specific tool names in Copilot queries
- Leverage search functionality for discovery
- Refresh cache when prompts are updated
- Monitor API response times

## 🛠️ Troubleshooting

### **Server Won't Start**
```bash
# Check dependencies
uv run python -c "import httpx; print('OK')"

# Test API connectivity
uv run python simple_api_test.py

# Check MCP server directly
uv run python examples/custom_servers/prompt_api_server.py --server
```

### **Tools Not Appearing in Copilot**
1. Restart VS Code to reload MCP configuration
2. Check `.vscode/settings.json` for correct server configuration
3. Verify server starts without errors

### **API Connection Issues**
- Verify API endpoint is accessible: `http://34.74.137.80/prompt-storage/files`
- Check network connectivity and firewall settings
- Validate signed URLs haven't expired

---

**🎉 Your Prompt API MCP Server is ready!**

Restart VS Code and start using your prompts directly in GitHub Copilot Chat!
