import kivy
kivy.require('2.1.0') # replace with your current kivy version !

import requests

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen

import sys
sys.path.insert(0, 'safe_sailing/Features')

Window.size = (310, 580)

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class WeatherNotificationApp(MDApp):
    def build(self):
        Builder.load_file("WeatherNotif.kv")
        sm = ScreenManager()
        screens = [FirstWindow(name="clickbelowweathernotif"), SecondWindow(name="weathernotif")]
        for screen in screens:
            sm.add_widget(screen)
        return sm
    
    
    def get_weather(self, location):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={config.weather_api_key}"
            response = requests.get(url)
            x = response.json()

            rainy = ["200", "201", "202", "210", "211", "212", "221", "230", "231", "232", "500", "501", "502",
                     "503", "504", "511", "520", "521", "522", "531", "300", "301", "302", "310", "311", "312",
                     "313", "314", "321"]
            cloudy = ["801", "802", "803", "804"]
            snowy = ["600", "601", "602", "611", "612", "613","615", "616", "620", "621", "622"]
            clear = ["800"]

            if x["cod"] != "404":
                temperature = round(x["main"]["temp"]-273.15) # convert from kelvin to celcius 
                humidity = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"]*18/5) # convert from m/s to km/s
                location = x["name"] + ", " + x["sys"]["country"]
                self.root.get_screen('weathernotif').ids.temperature.text = f"[b]{temperature}[/b]°"
                self.root.get_screen('weathernotif').ids.weather.text  = str(weather)
                self.root.get_screen('weathernotif').ids.humidity.text  = f"{humidity}%"
                self.root.get_screen('weathernotif').ids.wind_speed.text  = f"{wind_speed} km/h"
                self.root.get_screen('weathernotif').ids.location.text  = str(location)

                if id in clear:
                    self.root.get_screen('weathernotif').ids.weather_image.source =  "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/clear.png"
                elif id in cloudy: 
                    self.root.get_screen('weathernotif').ids.weather_image.source =  "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/cloudy.png"
                elif id in rainy: 
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/raining.png"
                elif id in snowy:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/snow.png"
                elif temperature > 24:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/sunny.png"
                elif wind_speed > 20:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/senior_proj/safe_sailing/Features/asset/windy.png"
            else:
                print("City Not Found")

        except requests.ConnectionError:
            print("No Internet Connection")

    def search_weather(self, location):
        self.get_weather(location)


    def change_screen(self, screen: str):
        self.root.current = screen



if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    WeatherNotificationApp().run()