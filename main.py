import tkinter as tk
import time
import requests 

def getweather():
    city = textField.get()
    api_key= "https://api.openweathermap.org/data/2.5/weather?q=" +city +"&appid=b986e059c0eaa6ef34ae5996cdefe150"

    json_data = requests.get(api_key).json() 
    condition = json_data['weather'][0]['main']

    # to get temperature in degree celsius
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data ['main']['pressure']
    humidity = json_data['main']['humidity']
    
    wind = json_data['wind']['speed']
    #timezone of Mukerian,India is IST whise offset is GMT+5.5.  Therefore subtract 5.5 hrs,i.e, 19800 seconds because IST is ahead of GMT(Greenwich Mean Time) by 5.5 hours
    sunrise = time.strftime("%H:%M:%S", time.gmtime(json_data ['sys']['sunrise']-19800))
    sunset = time.strftime("%H:%M:%S", time.gmtime(json_data ['sys']['sunset']-19800))
    
    final_info = condition + "\n" + str(temp) + "degree C"
    final_data = "\n" + "Maximum Temperature: " +str(max_temp) +"\n" +"Minimum Temperature: " +str(min_temp) +"\n" +"Pressure: " +str(pressure) +"\n" +"Humidity: "+ str(humidity)+ "\n" +"Wind Speed: " +str(wind) + "\n"+"Sunrise: " +str(sunrise) + "\n"+"Sunset"+str(sunset)
    label1.config(text = final_info)
    label2.config(text = final_data)
canvas = tk.Tk()
canvas.geometry("800x600")
canvas.title("Weather Application")
body_font = ("arial", 15, "normal")
title_font = ("italic", 30, "bold")

#textfied will get the city name from the user
textField = tk.Entry(canvas, justify='center', width = 18, font = title_font) #font = title_font applies a pre-defined font style stored in the variable title_font.
textField.pack(pady = 21)
# user can type the city name directy without moving the cursor
textField.focus()
textField.bind('<Return>', getweather)

#labels to show data
# tile label
label1 = tk.Label(canvas, font=title_font)
label1.pack()
#body label
label2 = tk.Label(canvas, text = "Enter your City", font=body_font)
label2.pack()

#Starts the main event loop of the application.Without this, the GUI window would appear and immediately close.
canvas.mainloop()