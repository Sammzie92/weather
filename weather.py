from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
from PIL import Image, ImageTk




url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsius, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, icon, weather)
        return final
    else:
        return None


# Define Search
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        icon_path = 'icons/{}.png'.format(weather[3])
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        image.configure(image=icon_photo)
        image.image = icon_photo
        temp_lbl['text'] = '{:.2f}°C'.format(weather[2])
        weather_lbl['text'] = weather[4]

    else:
        messagebox.showerror('Error', 'Cannot Find City {}'.format(city))


app = Tk()
app.title("Weather app")
app.geometry('700x350')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text="Search Weather", width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

image = Label(app)
image.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()

weather_lbl = Label(app, text='')
weather_lbl.pack()

app.mainloop()
