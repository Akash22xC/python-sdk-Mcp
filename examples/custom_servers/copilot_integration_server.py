"""
GitHub Copilot Integration MCP Server
=====================================

A comprehensive MCP server designed for GitHub Copilot Chat integration.
Provides useful development tools and utilities.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

# Create server optimized for GitHub Copilot
mcp = FastMCP(
    name="GitHub Copilot Assistant",
    instructions="Development tools and utilities for GitHub Copilot Chat integration",
)


@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    """Get system information useful for development"""
    import platform
    import psutil
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "cpu_count": psutil.cpu_count(),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "timestamp": datetime.now().isoformat()
    }


@mcp.tool()
def run_git_command(command: str, directory: str = ".") -> Dict[str, Any]:
    """Run a git command and return the result"""
    try:
        full_command = f"git {command}"
        result = subprocess.run(
            full_command,
            shell=True,
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "command": full_command,
            "directory": directory,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "command": full_command,
            "directory": directory,
            "error": "Command timed out after 30 seconds",
            "success": False
        }
    except Exception as e:
        return {
            "command": full_command,
            "directory": directory,
            "error": str(e),
            "success": False
        }


@mcp.tool()
def analyze_project_structure(directory: str = ".") -> Dict[str, Any]:
    """Analyze project structure and return key information"""
    try:
        path = Path(directory)
        if not path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        files = []
        dirs = []
        config_files = []
        
        # Common config file patterns
        config_patterns = [
            "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml",
            "pom.xml", "build.gradle", "composer.json", "Gemfile", "go.mod",
            ".gitignore", "README.md", "README.txt", "LICENSE", "Dockerfile",
            "docker-compose.yml", ".env", ".env.example"
        ]
        
        for item in path.iterdir():
            if item.is_file():
                files.append(item.name)
                if item.name.lower() in [p.lower() for p in config_patterns]:
                    config_files.append(item.name)
            elif item.is_dir() and not item.name.startswith('.'):
                dirs.append(item.name)
        
        return {
            "directory": str(path.absolute()),
            "total_files": len(files),
            "total_directories": len(dirs),
            "config_files_found": config_files,
            "directories": dirs[:20],  # Limit to first 20
            "files": files[:20],  # Limit to first 20
            "analysis_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def read_file_content(file_path: str, max_lines: int = 100) -> Dict[str, Any]:
    """Read file content with optional line limit"""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File {file_path} does not exist"}
        
        if not path.is_file():
            return {"error": f"{file_path} is not a file"}
            
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        content_lines = lines[:max_lines] if max_lines > 0 else lines
        
        return {
            "file_path": str(path.absolute()),
            "total_lines": total_lines,
            "displayed_lines": len(content_lines),
            "content": ''.join(content_lines),
            "truncated": total_lines > max_lines if max_lines > 0 else False
        }
        
    except UnicodeDecodeError:
        return {"error": f"Cannot read {file_path} - binary file or encoding issue"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_in_files(pattern: str, directory: str = ".", file_extension: str = None) -> Dict[str, Any]:
    """Search for a pattern in files within a directory"""
    try:
        import re
        
        path = Path(directory)
        if not path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        matches = []
        files_searched = 0
        
        # Build file pattern
        if file_extension:
            file_pattern = f"**/*.{file_extension.lstrip('.')}"
        else:
            file_pattern = "**/*"
        
        for file_path in path.glob(file_pattern):
            if file_path.is_file():
                try:
                    files_searched += 1
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if re.search(pattern, line, re.IGNORECASE):
                                matches.append({
                                    "file": str(file_path.relative_to(path)),
                                    "line_number": line_num,
                                    "line_content": line.strip(),
                                    "match": pattern
                                })
                            
                            # Limit matches per file
                            if len([m for m in matches if m["file"] == str(file_path.relative_to(path))]) >= 10:
                                break
                                
                except (UnicodeDecodeError, PermissionError):
                    continue
                    
                # Limit total matches
                if len(matches) >= 50:
                    break
        
        return {
            "pattern": pattern,
            "directory": str(path.absolute()),
            "file_extension": file_extension,
            "files_searched": files_searched,
            "matches_found": len(matches),
            "matches": matches
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_package_info(directory: str = ".") -> Dict[str, Any]:
    """Get package/dependency information from common config files"""
    try:
        path = Path(directory)
        info = {"directory": str(path.absolute()), "packages": {}}
        
        # Check package.json (Node.js)
        package_json = path / "package.json"
        if package_json.exists():
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                info["packages"]["nodejs"] = {
                    "name": data.get("name"),
                    "version": data.get("version"),
                    "dependencies": data.get("dependencies", {}),
                    "devDependencies": data.get("devDependencies", {})
                }
        
        # Check pyproject.toml (Python)
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                import tomllib
            except ImportError:
                try:
                    import tomli as tomllib
                except ImportError:
                    info["packages"]["python"] = "Could not parse pyproject.toml - missing tomllib/tomli"
                    return info
                    
            with open(pyproject, 'rb') as f:
                data = tomllib.load(f)
                project = data.get("project", {})
                info["packages"]["python"] = {
                    "name": project.get("name"),
                    "version": project.get("version"),
                    "dependencies": project.get("dependencies", []),
                    "optional_dependencies": project.get("optional-dependencies", {})
                }
        
        # Check requirements.txt (Python)
        requirements = path / "requirements.txt"
        if requirements.exists():
            with open(requirements, 'r', encoding='utf-8') as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                if "python" not in info["packages"]:
                    info["packages"]["python"] = {}
                info["packages"]["python"]["requirements_txt"] = deps
        
        return info
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Run the server
    import sys
    
    transport = "streamable-http"
    port = 8090
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if "--server" in sys.argv:
            transport = "stdio"
            print("🚀 GitHub Copilot Integration MCP Server starting...")
            print("📋 Available tools: get_system_info, run_git_command, analyze_project_structure, read_file_content, search_in_files, get_package_info")
            mcp.run(transport="stdio")
            exit(0)
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])
        if "--transport" in sys.argv:
            idx = sys.argv.index("--transport")
            if idx + 1 < len(sys.argv):
                transport = sys.argv[idx + 1]
    
    print(f"🚀 GitHub Copilot Integration MCP Server starting on port {port}")
    print(f"🔗 Transport: {transport}")
    print(f"📋 Available tools: get_system_info, run_git_command, analyze_project_structure, read_file_content, search_in_files, get_package_info")
    
    # Configure the server with port and host
    mcp.host = "localhost"
    mcp.port = port
    mcp.run(transport=transport)
