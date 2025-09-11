#!/usr/bin/env python3
"""
Get weather information for Barcelona using the weather MCP server
"""
import sys
import os

# Add the FastMCP path
sys.path.insert(0, 'examples/fastmcp')

# Import the weather module
from weather_structured import get_weather, get_weather_summary, get_temperature

def main():
    print("=== Weather Information for Barcelona ===\n")
    
    try:
        # Get detailed weather
        print("🌤️ Current Weather:")
        weather = get_weather("Barcelona")
        print(f"Temperature: {weather.temperature}°C")
        print(f"Condition: {weather.condition}")
        print(f"Humidity: {weather.humidity}%")
        print(f"Wind Speed: {weather.wind_speed} km/h")
        print(f"Last Updated: {weather.timestamp}")
        
        print("\n📋 Weather Summary:")
        summary = get_weather_summary("Barcelona")
        print(f"Description: {summary.description}")
        
        print("\n🌡️ Just Temperature:")
        temp = get_temperature("Barcelona")
        print(f"Temperature: {temp}°C")
        
    except Exception as e:
        print(f"Error getting weather data: {e}")

if __name__ == "__main__":
    main()
