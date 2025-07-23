import requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in3e
import time

# Configuration
LATITUDE = X  # Replace with your latitude
LONGITUDE = Y  # Replace with your longitude
API_KEY = '1234567890'  # Your OpenWeather API key
WEATHER_API_URL = f'https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric'

def fetch_weather():
    response = requests.get(WEATHER_API_URL)
    response.raise_for_status()
    return response.json()

def create_weather_image(weather_data):
    # Create a blank image in RGB mode
    width, height = 800, 600  # Adjust as necessary based on your display resolution
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Fetch weather info
    weather = weather_data['weather'][0]
    main = weather_data['main']
    temp = main['temp']
    description = weather['description'].capitalize()
    icon_code = weather['icon']
    
    # Draw background based on weather condition
    if 'rain' in description.lower():
        bg_color = (0, 0, 255)  # Blue for rain
    elif 'cloud' in description.lower():
        bg_color = (192, 192, 192)  # Gray for clouds
    elif 'clear' in description.lower():
        bg_color = (255, 223, 0)  # Yellow for clear sky
    elif 'snow' in description.lower():
        bg_color = (255, 255, 255)  # White for snow
    else:
        bg_color = (135, 206, 250)  # Light blue for other conditions
    
    # Fill background
    draw.rectangle((0, 0, width, height), fill=bg_color)
    
    # Add weather icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_response = requests.get(icon_url, stream=True)
    icon_image = Image.open(icon_response.raw).convert('RGBA')
    icon_image = icon_image.resize((100, 100))
    image.paste(icon_image, (50, 50), icon_image)
    
    # Add temperature Text
    font = ImageFont.load_default()
    draw.text((50, 170), f'Temperature: {temp}°C', font=font, fill='black')
    draw.text((50, 200), f'Description: {description}', font=font, fill='black')
    draw.text((50, 230), f'Location: {LATITUDE}, {LONGITUDE}', font=font, fill='black')
    
    return image

def display_image_on_epd(image):
    epd = epd7in3e.EPD()
    epd.init()
    epd.Clear()
    # Convert PIL Image to the format needed by the display
    # For Waveshare epd7in3e, use getbuffer()
    buf = epd.getbuffer(image)
    epd.display(buf)
    epd.sleep()

def main():
    try:
        weather_data = fetch_weather()
        weather_image = create_weather_image(weather_data)
        display_image_on_epd(weather_image)
        print("Weather display updated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()