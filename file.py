import tkinter as tk
import time
import requests
import datetime 

def getweather(event=None):
    try:
        city = textField.get().strip()
        if not city:
            label1.config(text="Please enter a valid city name")
            label2.config(text="")
            return

        api_key = "b986e059c0eaa6ef34ae5996cdefe150"
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        # Fetch weather data
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            label1.config(text="Error retrieving data")
            label2.config(text=weather_response.json().get("message", "Unknown error"))
            return
        
        weather_data = weather_response.json()

        # Extract coordinates
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']

        # Fetch AQI data
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_response = requests.get(aqi_url)
        if aqi_response.status_code != 200:
            label1.config(text="Error retrieving AQI data")
            label2.config(text=aqi_response.json().get("message", "Unknown error"))
            return
        
        aqi_data = aqi_response.json()

        # Extract AQI
        aqi = aqi_data['list'][0]['main']['aqi']
        aqi_description = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        aqi_text = aqi_description.get(aqi, "Unknown")

        # Extract weather data
        condition = weather_data['weather'][0]['main']
        temp = int(weather_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
        min_temp = int(weather_data['main']['temp_min'] - 273.15)
        max_temp = int(weather_data['main']['temp_max'] - 273.15)
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        timezone_offset = weather_data['timezone']  # seconds
        sunrise = time.strftime("%H:%M:%S", time.gmtime(weather_data['sys']['sunrise'] + timezone_offset))
        sunset = time.strftime("%H:%M:%S", time.gmtime(weather_data['sys']['sunset'] + timezone_offset))

        #rain_info = "No rain data available"
        #if "rain" in weather_data:
         #   if "1h" in weather_data["rain"]:
          #      rain_info = f"Rain in the last hour: {weather_data['rain']['1h']} mm"
           # elif "4h" in weather_data["rain"]:
            #    rain_info = f"Rain in the last 3 hours: {weather_data['rain']['4h']} mm"

        # Displaying data
        final_info = f"{condition}\n{temp}°C\nAir Quality: {aqi_text} (AQI {aqi})"
        final_data = (f"Maximum Temperature: {max_temp}°C\n"
                      f"Minimum Temperature: {min_temp}°C\n"
                      f"Pressure: {pressure} hPa\n"
                      f"Humidity: {humidity}%\n"
                      f"Wind Speed: {wind} m/s\n"
                      f"Sunrise: {sunrise}\n"
                      f"Sunset: {sunset}")
        
        label1.config(text=final_info)
        label2.config(text=final_data)

    except requests.exceptions.RequestException as e:
        label1.config(text="Network Error")
        label2.config(text="Please check your internet connection")
    except KeyError:
        label1.config(text="Invalid response")
        label2.config(text="Please check the city name or API key")
    except Exception as e:
        label1.config(text="Error")
        label2.config(text=str(e))
        # Tkinter setup
canvas = tk.Tk()
canvas.geometry("600x600")
canvas.title("Weather Application")

# Fonts
body_font = ("arial", 15, "normal")
title_font = ("italic", 30, "bold")

# Input Field
textField = tk.Entry(canvas, justify='center', width=18, font=title_font)
textField.pack(pady=21)
textField.focus()
textField.bind('<Return>', getweather)

# Labels
label1 = tk.Label(canvas, font=title_font)
label1.pack()
label2 = tk.Label(canvas, text="Enter your City", font=body_font)
label2.pack()

# Main loop
canvas.mainloop()

