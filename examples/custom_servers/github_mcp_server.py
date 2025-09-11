#!/usr/bin/env python3
"""
GitHub MCP Server for Copilot Integration

This server provides GitHub-related tools that Copilot can use to:
- Search repositories
- Get repository information
- Fetch file contents
- List issues and PRs
- Get commit information

Usage:
    python github_mcp_server.py

Then configure in your MCP client (like Claude Desktop or Copilot)
"""

import asyncio
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

import httpx
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import create_connected_server_and_client_session


# Data models for structured responses
class Repository(BaseModel):
    """GitHub repository information"""
    name: str
    full_name: str
    description: Optional[str] = None
    url: str
    stars: int = Field(alias="stargazers_count")
    forks: int = Field(alias="forks_count")
    language: Optional[str] = None
    updated_at: str
    topics: List[str] = []


class Issue(BaseModel):
    """GitHub issue information"""
    number: int
    title: str
    body: Optional[str] = None
    state: str
    author: str
    created_at: str
    updated_at: str
    labels: List[str] = []
    
    @classmethod
    def from_github_api(cls, data: dict) -> "Issue":
        """Create Issue from GitHub API response"""
        labels = [label["name"] for label in data.get("labels", [])]
        return cls(
            number=data["number"],
            title=data["title"],
            body=data.get("body"),
            state=data["state"],
            author=data["user"]["login"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            labels=labels
        )


class Commit(BaseModel):
    """GitHub commit information"""
    sha: str
    message: str
    author: str
    date: str
    url: str
    
    @classmethod
    def from_github_api(cls, data: dict) -> "Commit":
        """Create Commit from GitHub API response"""
        return cls(
            sha=data["sha"],
            message=data["commit"]["message"],
            author=data["commit"]["author"]["name"],
            date=data["commit"]["author"]["date"],
            url=data["html_url"]
        )


# Create MCP server
mcp = FastMCP("GitHub API Server")

# GitHub API client
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


@mcp.tool()
async def search_repositories(query: str, limit: int = 10) -> List[Repository]:
    """
    Search GitHub repositories by query string
    
    Args:
        query: Search query (e.g., "python machine learning", "language:typescript", "user:microsoft")
        limit: Maximum number of results to return (default: 10, max: 100)
    
    Returns:
        List of repository information
    """
    limit = min(limit, 100)  # GitHub API limitation
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "per_page": limit, "sort": "stars"},
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        return [Repository.model_validate(repo) for repo in data["items"]]


@mcp.tool()
async def get_repository_info(owner: str, repo: str) -> Repository:
    """
    Get detailed information about a specific repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
    
    Returns:
        Detailed repository information
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=headers
        )
        response.raise_for_status()
        
        return Repository.model_validate(response.json())


@mcp.tool()
async def get_file_content(owner: str, repo: str, path: str, branch: str = "main") -> str:
    """
    Fetch the content of a file from a GitHub repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        path: File path within the repository
        branch: Branch name (default: main)
    
    Returns:
        File content as string
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            params={"ref": branch},
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        if data.get("encoding") == "base64":
            import base64
            return base64.b64decode(data["content"]).decode("utf-8")
        else:
            return data.get("content", "")


@mcp.tool()
async def list_repository_issues(owner: str, repo: str, state: str = "open", limit: int = 20) -> List[Issue]:
    """
    List issues from a GitHub repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        state: Issue state (open, closed, all)
        limit: Maximum number of issues to return
    
    Returns:
        List of repository issues
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            params={"state": state, "per_page": min(limit, 100)},
            headers=headers
        )
        response.raise_for_status()
        
        issues_data = response.json()
        return [Issue.from_github_api(issue_data) for issue_data in issues_data]


@mcp.tool()
async def get_recent_commits(owner: str, repo: str, limit: int = 10) -> List[Commit]:
    """
    Get recent commits from a GitHub repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        limit: Maximum number of commits to return
    
    Returns:
        List of recent commits
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits",
            params={"per_page": min(limit, 100)},
            headers=headers
        )
        response.raise_for_status()
        
        return [Commit.from_github_api(commit) for commit in response.json()]


@mcp.tool()
async def get_repository_languages(owner: str, repo: str) -> Dict[str, int]:
    """
    Get programming languages used in a repository with byte counts
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
    
    Returns:
        Dictionary of languages and their byte counts
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/languages",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()


@mcp.tool()
async def search_code(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for code across GitHub repositories
    
    Args:
        query: Code search query (e.g., "function language:python", "class AsyncClient")
        limit: Maximum number of results to return
    
    Returns:
        List of code search results
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/search/code",
            params={"q": query, "per_page": min(limit, 100)},
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        for item in data["items"]:
            results.append({
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"],
                "score": item.get("score", 0)
            })
        
        return results


# Add a resource for README files
@mcp.resource("github://readme/{owner}/{repo}")
async def get_readme(owner: str, repo: str) -> str:
    """Get the README file content from a repository"""
    try:
        return await get_file_content(owner, repo, "README.md")
    except:
        try:
            return await get_file_content(owner, repo, "README.rst")
        except:
            try:
                return await get_file_content(owner, repo, "README.txt")
            except:
                return "No README file found"


if __name__ == "__main__":
    # For testing: run some example calls
    async def test_server():
        print("🔧 Testing GitHub MCP Server...")
        
        # Test repository search
        print("\n1. Searching for Python repositories...")
        repos = await search_repositories("python machine learning", 3)
        for repo in repos:
            print(f"  - {repo.full_name}: {repo.stars} stars")
        
        # Test getting repo info
        if repos:
            first_repo = repos[0]
            owner, repo_name = first_repo.full_name.split("/")
            print(f"\n2. Getting info for {first_repo.full_name}...")
            
            # Get languages
            languages = await get_repository_languages(owner, repo_name)
            print(f"  Languages: {list(languages.keys())}")
            
            # Get recent commits
            commits = await get_recent_commits(owner, repo_name, 3)
            print(f"  Recent commits:")
            for commit in commits:
                print(f"    - {commit.message[:50]}... by {commit.author}")
    
    # Run tests if executed directly
    asyncio.run(test_server())
    
    # Note: To run as MCP server, use:
    # mcp.run()  # This would start the MCP server
