"""
Website Prompt Library MCP Server
Provides ready-to-use prompts for generating different types of websites
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Create server with new name
mcp = FastMCP("Website Prompt Library")


@mcp.tool()
def get_football_website_prompt() -> Dict[str, Any]:
    """Get a complete prompt for generating FC Barcelona fan community website"""
    prompt = """Create a responsive single-page static website for FC Barcelona fan community.
Design: deep red (#DC143C) header, black (#000000) highlights, bold sans-serif (Montserrat).
Club: FC Barcelona - "Més que un club" (More than a club)
Sections: sticky nav (Home, News, Fixtures, Squad, Gallery, Join), hero banner with Camp Nou stadium background, Latest News (3 cards with recent Barça updates), Upcoming La Liga Fixtures, Squad grid (current Barcelona players), Gallery (Camp Nou & match photos), newsletter sign-up for Culer updates, and social footer with official Barça social links.
Mobile-first layout, lazy-loaded images, smooth hover effects with red/black transitions, and SEO/Open-Graph meta tags.
Use these image URLs:

Hero Camp Nou: https://images.unsplash.com/photo-1505682634904-d7caccf9d6c4?auto=format&fit=crop&w=1600&q=80

Barcelona match action: https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=1600&q=80

Player placeholder: https://images.unsplash.com/photo-1599940824399-14d0f86f4793?auto=format&fit=crop&w=800&q=80

Include FC Barcelona logo placeholder, "Visca el Barça!" motto, and sections for:
- Latest transfer news
- Match highlights
- Player statistics
- Upcoming Champions League fixtures
- Fan forum access
- Official merchandise links
Output pure HTML + CSS plus minimal JS for the lightbox and mobile nav."""
    
    return {
        "category": "Football/Sports",
        "club_name": "FC Barcelona",
        "website_type": "Fan Community Site",
        "color_scheme": "Deep red (#DC143C), black (#000000) highlights",
        "fonts": "Montserrat (sans-serif)",
        "motto": "Més que un club (More than a club)",
        "stadium": "Camp Nou",
        "prompt": prompt,
        "features": [
            "FC Barcelona branding",
            "Camp Nou hero banner",
            "La Liga fixtures", 
            "Current squad grid",
            "Transfer news section",
            "Champions League updates",
            "Fan forum integration",
            "Official merchandise links",
            "Red/black hover effects"
        ]
    }


@mcp.tool()
def get_movie_website_prompt() -> Dict[str, Any]:
    """Get a complete prompt for generating John Wick 7 movie promotional website"""
    prompt = """Build a sleek, action-packed promotional website for "John Wick 7: The Final Chapter".
Theme: deep blue (#1e3a8a) background, vibrant orange (#f97316) accents, sharp white text, Bebas Neue headlines, Inter body text.
Movie Details: John Wick 7: The Final Chapter - Keanu Reeves returns for the ultimate revenge saga.
Sections: hero feature (John Wick 7 poster + explosive trailer), Cast & Crew (Keanu Reeves, Halle Berry, Ian McShane), Action Sequences gallery, Behind the Scenes content, Theater Locations & Showtimes, exclusive clips section, Subscribe for updates CTA, and social media footer.
Add JSON-LD Movie markup, countdown timer to release date, and responsive video embeds.
Use these images:

Action hero poster style: https://images.unsplash.com/photo-1607746882042-944635dfe10e?auto=format&fit=crop&w=1600&q=80

Behind the scenes: https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=800&q=80

Cinema/theater: https://images.unsplash.com/photo-1497032205916-ac775f0649ae?auto=format&fit=crop&w=1600&q=80

Include:
- Movie rating: R (Restricted)
- Release date: Summer 2024
- Director: Chad Stahelski
- Genre: Action/Thriller
- Runtime: 142 minutes
- Tagline: "Every action has consequences. Every choice has a price."
- Ticket booking integration
- IMAX/Dolby showings
- Official merchandise store
Provide static HTML/CSS and JavaScript for trailer modal, countdown timer, and ticket booking."""
    
    return {
        "category": "Entertainment/Media",
        "movie_title": "John Wick 7: The Final Chapter",
        "website_type": "Movie Promotional Site",
        "color_scheme": "Deep blue (#1e3a8a), vibrant orange (#f97316) accents",
        "fonts": "Bebas Neue (headlines), Inter (body)",
        "tagline": "Every action has consequences. Every choice has a price.",
        "rating": "R (Restricted)",
        "director": "Chad Stahelski",
        "runtime": "142 minutes",
        "prompt": prompt,
        "features": [
            "Action-packed design",
            "Movie poster hero",
            "Cast & crew section",
            "Action sequences gallery",
            "Behind the scenes content",
            "Theater showtimes",
            "Countdown timer",
            "Ticket booking",
            "IMAX/Dolby listings",
            "Merchandise store"
        ]
    }


@mcp.tool()
def get_book_website_prompt() -> Dict[str, Any]:
    """Get a complete prompt for generating Atomic Habits book promotional website"""
    prompt = """Design a clean, minimalist promotional website for "Atomic Habits" by James Clear.
Style: pristine white (#ffffff) background, warm cream (#f5f5dc) sections, elegant typography with Playfair Display headings, Source Sans Pro body text.
Book Details: "Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones" by James Clear
Sections: header/nav (Book, Author, Reviews, Resources, Buy), hero section (book cover + key message), Chapter Highlights, Reader Reviews & Testimonials, Author Bio (James Clear), Habit Tracker download, Book Clubs & Discussion Groups, Purchase Links (Amazon, Barnes & Noble, etc.), email sign-up for habit tips, and clean footer.
Ensure excellent readability, print-friendly CSS, and structured data for book information.
Use these images:

Book cover showcase: https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=800&q=80

Reading/study aesthetic: https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1600&q=80

Author portrait: https://images.unsplash.com/photo-1544723795-3fb6469f5b39?auto=format&fit=crop&w=800&q=80

Include:
- Book ISBN: 978-0735211292
- Publisher: Avery (Penguin Random House)
- Pages: 320 pages
- Publication Date: October 16, 2018
- Key concepts: 1% better every day, habit stacking, environment design
- Quote: "You do not rise to the level of your goals. You fall to the level of your systems."
- Free habit tracker PDF download
- Book club discussion guides
- James Clear's newsletter signup
- Related articles and resources
Output clean HTML and CSS (no framework) with optional light JS for book preview modal and habit tracker."""
    
    return {
        "category": "Literature/Self-Help",
        "book_title": "Atomic Habits",
        "author": "James Clear",
        "subtitle": "An Easy & Proven Way to Build Good Habits & Break Bad Ones",
        "website_type": "Book Promotional Site",
        "color_scheme": "Pristine white (#ffffff), warm cream (#f5f5dc)",
        "fonts": "Playfair Display (headings), Source Sans Pro (body)",
        "isbn": "978-0735211292",
        "publisher": "Avery (Penguin Random House)",
        "pages": "320 pages",
        "key_quote": "You do not rise to the level of your goals. You fall to the level of your systems.",
        "prompt": prompt,
        "features": [
            "Clean minimalist design",
            "Book cover hero",
            "Chapter highlights",
            "Reader testimonials",
            "Author bio section",
            "Free habit tracker download",
            "Book club resources",
            "Purchase links",
            "Newsletter signup",
            "Discussion guides"
        ]
    }


# Keep one resource for demonstration
@mcp.resource("prompts://all")
def list_all_prompts() -> str:
    """List all available website prompts"""
    return """Available Website Prompts:
1. FC Barcelona Fan Community - Deep red and black theme with Camp Nou imagery
2. John Wick 7: The Final Chapter - Blue and orange action movie promotional site
3. Atomic Habits by James Clear - Clean white and cream book promotional site

Use the respective tools to get the complete prompts with all details and configurations."""


# Add a prompt template for custom requests
@mcp.prompt("website_generator")
def website_generator_prompt(site_type: str, theme: str = "modern") -> str:
    """Generate a custom website prompt based on site type and theme"""
    return f"""Create a {theme} {site_type} website with the following requirements:
- Responsive design optimized for mobile-first approach
- Clean, professional layout with intuitive navigation
- SEO-optimized structure with proper meta tags
- Accessibility features (ARIA labels, keyboard navigation)
- Performance optimization (compressed images, minimal CSS/JS)
- Cross-browser compatibility
- Contact/CTA sections
- Social media integration points

Please provide complete HTML, CSS, and any necessary JavaScript code."""


if __name__ == "__main__":
    import sys
    
    # Check for server mode
    if "--server" in sys.argv:
        print("Website Prompt Library MCP Server starting...")
        print("Available tools: get_football_website_prompt, get_movie_website_prompt, get_book_website_prompt")
        print("Available resources: prompts://all")
        print("Available prompts: website_generator")
        mcp.run(transport="stdio")
    elif "--schemas" in sys.argv:
        print("Website Prompt Library Tool Schemas")
        print("=" * 50)
        print("\n🏈 Tool: get_football_website_prompt")
        print("Description: Get a complete prompt for generating FC Barcelona fan community website")
        print("Input: None required")
        print("Output: Dictionary with club details, color scheme, stadium info, and complete prompt")
        
        print("\n🎬 Tool: get_movie_website_prompt") 
        print("Description: Get a complete prompt for generating John Wick 7 promotional website")
        print("Input: None required")
        print("Output: Dictionary with movie details, cast info, rating, and complete prompt")
        
        print("\n📚 Tool: get_book_website_prompt")
        print("Description: Get a complete prompt for generating Atomic Habits promotional website") 
        print("Input: None required")
        print("Output: Dictionary with book details, author info, ISBN, and complete prompt")
    else:
        # Run in test mode
        print("Website Prompt Library Server Test Mode")
        print("Use --server to run as MCP server")
        
        # Test the tools
        print("\nTesting FC Barcelona Website Prompt:")
        result = get_football_website_prompt()
        print(f"Club: {result['club_name']}")
        print(f"Stadium: {result['stadium']}")
        print(f"Colors: {result['color_scheme']}")
        
        print("\nTesting John Wick 7 Website Prompt:")
        result = get_movie_website_prompt()
        print(f"Movie: {result['movie_title']}")
        print(f"Director: {result['director']}")
        print(f"Theme: {result['color_scheme']}")
        
        print("\nTesting Atomic Habits Website Prompt:")
        result = get_book_website_prompt()
        print(f"Book: {result['book_title']}")
        print(f"Author: {result['author']}")
        print(f"ISBN: {result['isbn']}")
        
        print("\nTesting Resource:")
        resource_result = list_all_prompts()
        print(f"Available prompts:\n{resource_result}")
        
        print("\nTesting Custom Prompt:")
        custom_prompt = website_generator_prompt("portfolio", "minimal")
        print(f"Custom prompt preview: {custom_prompt[:100]}...")
