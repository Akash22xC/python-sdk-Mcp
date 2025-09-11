"""
Example of how to make it use REAL weather data
"""
import httpx
import os

async def get_real_temperature(city: str, unit: str = "celsius") -> float:
    """Get REAL temperature from weather API"""
    # Example using OpenWeatherMap API
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key,
                "units": "metric" if unit == "celsius" else "imperial"
            }
        )
        data = response.json()
        return data["main"]["temp"]  # Real temperature!

# Your current server returns the same value every time:
def current_fake_temperature(city: str, unit: str = "celsius") -> float:
    return 22.5  # Same for Tokyo, Mumbai, London, etc!
