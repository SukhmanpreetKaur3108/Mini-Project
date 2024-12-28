import tkinter as tk
import time
import requests

def getweather(event=None):
    try:
        city = textField.get().strip()
        if not city:
            label1.config(text="Please enter a valid city name")
            label2.config(text="")
            return

        api_key = "b986e059c0eaa6ef34ae5996cdefe150"
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        response = requests.get(api_url)
        if response.status_code != 200:
            label1.config(text="Error retrieving data")
            label2.config(text=response.json().get("message", "Unknown error"))
            return
        
        json_data = response.json()

        # Extracting data
        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure'] #unit is hPa(hectopascal); 1hPa = 1 mbar
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        #timezone of Mukerian,India is IST whise offset is GMT+5.5.  Therefore subtract 5.5 hrs,i.e, 19800 seconds because IST is ahead of GMT(Greenwich Mean Time) by 5.5 hours
        sunrise = time.strftime("%I:%M", time.gmtime(json_data['sys']['sunrise'] -19800))
        sunset = time.strftime("%I:%M", time.gmtime(json_data['sys']['sunset'] -19800))

        # Displaying data
        final_info = f"{condition}\n{temp}°C"
        final_data = (f"Maximum Temperature: {max_temp}°C\n"
                      f"Minimum Temperature: {min_temp}°C\n"
                      f"Pressure: {pressure} hPa\n"
                      f"Humidity: {humidity}%\n"
                      f"Wind Speed: {wind} m/s\n"
                      f"Sunrise: {sunrise}\n"
                      f"Sunset: {sunset}")
        
        label1.config(text=final_info)
        label2.config(text=final_data)

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
