#!/usr/bin/env python3
"""
Test the Website Prompt Library tools
"""
import sys
import os

# Add the FastMCP path
sys.path.insert(0, 'examples/fastmcp')

# Import the tools
from echo import get_football_website_prompt, get_movie_website_prompt, get_book_website_prompt

def main():
    print("🎯 Website Prompt Library Demo")
    print("=" * 50)
    
    print("\n🏈 FOOTBALL WEBSITE PROMPT:")
    football = get_football_website_prompt()
    print(f"Category: {football['category']}")
    print(f"Type: {football['website_type']}")
    print(f"Colors: {football['color_scheme']}")
    print("\nFull Prompt:")
    print("-" * 30)
    print(football['prompt'])
    
    print("\n\n🎬 MOVIE WEBSITE PROMPT:")
    movie = get_movie_website_prompt()
    print(f"Site Name: {movie['site_name']}")
    print(f"Category: {movie['category']}")
    print(f"Colors: {movie['color_scheme']}")
    print("\nFull Prompt:")
    print("-" * 30)
    print(movie['prompt'])
    
    print("\n\n📚 BOOK WEBSITE PROMPT:")
    book = get_book_website_prompt()
    print(f"Site Name: {book['site_name']}")
    print(f"Category: {book['category']}")
    print(f"Colors: {book['color_scheme']}")
    print("\nFull Prompt:")
    print("-" * 30)
    print(book['prompt'])

if __name__ == "__main__":
    main()
