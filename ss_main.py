import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from firebase import firebase
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, DictProperty, OptionProperty, ObjectProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy_garden.mapview import MapMarker, MapView, MapMarkerPopup, MapMarker
from kivymd.uix.dialog import MDDialog, MDInputDialog

from gps3 import gps3
from geopy.geocoders import Nominatim, GoogleV3
from kivy.animation import Animation
# For snackbar
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock


# For snackbar
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

from kivy.graphics import Color, Line


from demo import profiles
# import DisplayMap.config as config 
import config 
import json
import datetime
import requests
import re

Window.size = (310, 580)
curr_user = ""

class FirstWindow(Screen):
    pass

class LoginWindow(Screen):
    pass

class CreateAccWindow(Screen):
    pass

class DisplayMapWindow(Screen):
    lat = 40.6931479
    lon =  -73.9874499

class RateCommentWindow(Screen):
    selected_rating = ""

class ViewSafetyNotifWindow(Screen):
    pass

class SafetyNotifWindow(Screen):
    pass

class ViewWeatherNotifWindow(Screen):
    pass

class WeatherNotifWindow(Screen):
    pass

class CallWindow(Screen):
    pass

class MessageScreen(Screen):
    # A screen that display the story fleets and all message histories.
    pass

class ChatScreen(Screen):
    # A screen that display messages with a user
    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(defaultvalue=False)

class ChatListItem(MDCard):
    # Clickable chat item for the chat screen
    isRead = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    username = StringProperty()
    msg = StringProperty()
    timestamp = StringProperty()
    profile = DictProperty()

class ChatBubble(MDBoxLayout):
    # A chat bubble for the chat screen messages.

    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    isRead = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])

class Message(MDLabel):
    # A adaptive text for the chat bubble.'''
    pass 

class ImageButton(ButtonBehavior, Image):
    pass
 
class LabelButton(ButtonBehavior, Label):
    pass

class HomeMapView(MapView):
    pass

class WindowManager(ScreenManager):
    pass

class HomeGpsHelper():
    has_centered_map = False
    dialog = None
    def run(self):
        # Get a reference to GpsBlinker, then call blink()
        # home_gps_blinker = App.get_running_app().root.ids.home_screen.ids.mapview.ids.blinker
        home_gps_blinker = App.get_running_app().sm.get_screen('displaymap').ids.mapview.ids.blinker 
 
        # Start blinking the GpsBlinker
        home_gps_blinker.blink()
         
        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    from plyer import gps
                    gps.configure(on_location=self.update_blinker_position, on_status=self.on_auth_status)
                    gps.start(minTime=1000, minDistance=1)
                else:
                    print("Did not get all permissions")
 
            request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], callback)
        
 
    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position
        # home_gps_blinker = App.get_running_app().root.ids.home_screen.ids.mapview.ids.blinker
        home_gps_blinker = App.get_running_app().sm.get_screen("displaymap").ids.mapview.ids.blinker
        home_gps_blinker.lat = my_lat
        home_gps_blinker.lon = my_lon
 
        # Center map on gps
        if not self.has_centered_map:
            # map2 = App.get_running_app().root.ids.home_screen.ids.mapview
            map2 = App.get_running_app().sm.get_screen("displaymap").ids.mapview
            map2.center_on(my_lat, my_lon)
            self.has_centered_map = True
 
        App.get_running_app().current_lat = my_lat
        App.get_running_app().current_lon = my_lon
 
    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            print("Open gps access popup")
            try:
                self.open_gps_access_popup()
            except:
                print("error")
                pass
 
    def open_gps_access_popup(self):
        if not self.dialog:
            self.dialog = "STOP"
            Clock.schedule_once(self.run_dialog, 2)
 
    def run_dialog(self, *args):
        self.dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly", size_hint=(0.5, 0.5))
        self.dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        self.dialog.open()
        self.dialog = None

class GpsBlinker(MapMarker):
    def blink(self):
        # Animation that changes the blink size and opacity
        anim = Animation(outer_opacity=0, blink_size=50)
         
        # When the animation completes, reset the animation, then repeat
        anim.bind(on_complete = self.reset)
        anim.start(self)
 
    def reset(self, *args):
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()

class SearchPopupMenu(MDInputDialog):
     
    title = 'Search by Address'
    text_button_ok = 'Search'
    def __init__(self): 
        super().__init__() # super() inherits all the methods in MDInputDialog, within the __init__() function
        self.size_hint = [.9, .3]
        self.events_callback = self.callback #call the callback function below
 
    def open(self):
        super().open() # super() inherits all the methods in MDInputDialog, within the open() function
        Clock.schedule_once(self.set_field_focus, 0.5)
 
    def callback(self, *args):
        address = self.text_field.text
        self.geocode_get_lat_lon(address)
 
    def success(self, result):
        print("Success")
        # print(result)
        try:
            latitude = result[0]
            longitude = result[1]
            mapview = App.get_running_app().sm.get_screen('displaymap').ids.mapview
            mapview.center_on(latitude, longitude)
        except:
            Snackbar(text="Address not found, please try other addresses.", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            pass
        App.get_running_app().press_dist()


    def geocode_get_lat_lon(self, address):
        geolocator = GoogleV3(api_key=config.google_api_key)
        location = geolocator.geocode(address)
        log_lat = [location.latitude,location.longitude]
        global destination_long
        global destination_lat
        destination_long = location.longitude
        destination_lat = location.latitude
        self.success(log_lat)


class SafeSailing(MDApp): 
    def __init__(self, **kwargs):
        super().__init__()
        self.table = None
        self.route_points = []
        self.list_of_lines = []

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.accent_hue = '400'
        self.title = "Messages"
        self.ind = 0
        self.search_menu = SearchPopupMenu()

        Builder.load_file('ss_main.kv')

        self.sm = ScreenManager()
        screens = [FirstWindow(name="main"), LoginWindow(name="login"), CreateAccWindow(name="createaccount"),
                   DisplayMapWindow(name="displaymap"), RateCommentWindow(name="ratecomment"), 
                   ViewSafetyNotifWindow(name="clickbelowsafetynotif"), SafetyNotifWindow(name="safetynotif"), 
                   ViewWeatherNotifWindow(name="clickbelowweathernotif"), WeatherNotifWindow(name="weathernotif"),
                   MessageScreen(name="msg"), CallWindow(name="callfirstresponders")]

        for screen in screens:
            self.sm.add_widget(screen)
        
        # Initialize GPS
        home_gps_blinker = App.get_running_app().sm.get_screen('displaymap').ids.blinker2 
 
        # Start blinking the GpsBlinker
        home_gps_blinker.blink()

        return self.sm


    def change_screen(self, screen: str, direction='left'):
        self.root.transition.direction =  direction
        self.root.current = screen


    def login(self, email, password):
        # Initialise firebase
        fb = firebase.FirebaseApplication('https://safesailing-f9c4c-default-rtdb.firebaseio.com', None)

        # Get data
        result = fb.get('safesailing-f9c4c-default-rtdb/User', '')

        # Verify email and password
        for i in result.keys():
            if result[i]['Email'] == email:
                if result[i]['Password'] == password:
                    curr_user = "email"
                    self.change_screen('clickbelowweathernotif')
                else:
                    self.sm.get_screen("login").ids.error_message.text = "Incorrect email or password"

    def create_account(self, fname, lname, dob, email, password, homeadd, workadd):
        # Criteria for weak password:
            # The password is too short (less than 8 characters).
            # The password contains only lowercase letters or only uppercase letters.
            # The password contains only digits.
            # The password is a common word or phrase.

        fb = firebase.FirebaseApplication('https://safesailing-f9c4c-default-rtdb.firebaseio.com', None)

        common_passwords = ['password', '123456', 'qwerty', 'letmein', 'picture1']
        if ("@" not in email) or ((".com" not in email) and (".edu" not in email)):
            self.sm.get_screen("createaccount").ids.createaccount_error.text = "Invalid email"    
        elif (len(password) < 8 or (password.islower() or password.isupper()) or password.isdigit() or (password.lower() in common_passwords)):
            self.sm.get_screen("createaccount").ids.createaccount_error.text = "Weak password"
        else:
            # Import data
            data = {
                'Email': email,
                'Password': password,  
                'FirstName': fname, 
                'LastName': lname,
                'DateofBirth': dob,
                'Home': homeadd,    
                'Work': workadd 
            }
            # Post data: DatabaseName/TableName
            fb.post('safesailing-f9c4c-default-rtdb/User', data)
            self.change_screen('login')

    def select1(self):
        self.sm.get_screen("ratecomment").ids.star1.opacity = 1
        self.sm.get_screen("ratecomment").ids.star2.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star3.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star4.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star5.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.text.text = "It was horrible."

    def select2(self):
        self.sm.get_screen("ratecomment").ids.star1.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star2.opacity = 1
        self.sm.get_screen("ratecomment").ids.star3.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star4.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star5.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.text.text = "It was somewhat unsafe ~"

    def select3(self):
        self.sm.get_screen("ratecomment").ids.star1.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star2.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star3.opacity = 1
        self.sm.get_screen("ratecomment").ids.star4.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star5.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.text.text = "It was alright, but it could have been better."

    def select4(self):
        self.sm.get_screen("ratecomment").ids.star1.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star2.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star3.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star4.opacity = 1
        self.sm.get_screen("ratecomment").ids.star5.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.text.text = "It was good!"

    def select5(self):
        self.sm.get_screen("ratecomment").ids.star1.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star2.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star3.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star4.opacity = 0.5
        self.sm.get_screen("ratecomment").ids.star5.opacity = 1
        self.sm.get_screen("ratecomment").ids.text.text = "It was perfect."

    def post_rate_comment(self, trip_id, rating, comment):
        fb = firebase.FirebaseApplication('https://safesailing-f9c4c-default-rtdb.firebaseio.com', None)

        # Import data
        data = {
            'TripID': trip_id, 
            'Rating': rating,
            'Comment': comment 
        }

        # Post data: DatabaseName/TableName
        fb.post('safesailing-f9c4c-default-rtdb/Trip', data)
        self.change_screen('displaymap')

    def add_datatable(self):
        jsonFile = open('/Users/Malakhalifa/Downloads/SS/DisplayMap/raw_response2.json', "r")
        crime = json.load(jsonFile)
        row_data1 = []
        global crime_coord_long, crime_coord_lat
        crime_coord_long = []
        crime_coord_lat = []

        for j in range (20):
            title = crime['results'][j]['title']
            neighbourhood = crime['results'][j]['neighborhood']
            address = crime['results'][j]['address']
            longitude = crime['results'][j]['longitude']
            latitude = crime['results'][j]['latitude']
            timestamp = crime['results'][j]['ts']
            crime_coord_lat.append(float(latitude))
            crime_coord_long.append(float(longitude))
            
            json_timestamp = timestamp / 1000  # convert milliseconds to seconds
            date = datetime.datetime.fromtimestamp(json_timestamp, datetime.timezone.utc)
            time = date.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
            est_date = time.strftime("%m/%d/%Y")
            est_time = time.strftime("%I:%M:%S %p")
            DI = calculate_danger_index(title)
            cdata = CrimeData(title, neighbourhood, address, est_date, est_time, DI, longitude, latitude)
            row = [title, address, neighbourhood, est_date, est_time, DI]
            row_data1.append(row)
        
        self.table = MDDataTable(
            use_pagination = True,
            pos_hint = {'center_x': 0.5, 'center_y':0.3},
            size_hint = (0.97,0.5),
            
            column_data = [
                ("Incident", dp(50)), 
                ("Address", dp(40)),
                ("Neighbourhood", dp(25)),
                ("Date", dp(20)),
                ("Time (EST)", dp(20)),
                ("DI", dp(10))
            ],
            row_data = row_data1
        )

        jsonFile.close()
        self.sm.get_screen("safetynotif").ids.data_layout.add_widget(self.table)
        self.change_screen('safetynotif')
    
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
                    self.root.get_screen('weathernotif').ids.weather_image.source =  "/Users/Malakhalifa/Downloads/SS/asset/clear.png"
                elif id in cloudy: 
                    self.root.get_screen('weathernotif').ids.weather_image.source =  "/Users/Malakhalifa/Downloads/SS/asset/cloudy.png"
                elif id in rainy: 
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/Downloads/SS/asset/raining.png"
                elif id in snowy:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/Downloads/SS/asset/snow.png"
                elif temperature > 24:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/Downloads/SS/asset/sunny.png"
                elif wind_speed > 20:
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/Downloads/SS/asset/windy.png"
                else: 
                    self.root.get_screen('weathernotif').ids.weather_image.source = "/Users/Malakhalifa/Downloads/SS/asset/clouds.png"
            else:
                print("City Not Found")

        except requests.ConnectionError:
            print("No Internet Connection")
       
        except requests.RequestException:
            print("Error")

    def search_weather(self, location):
        self.get_weather(location)

    def create_chat(self, profile):
        # Get all messages and create a chat screen
        chat_name = "chat"+str(self.ind)
        self.chat_screen = ChatScreen(name=chat_name)
        if self.chat_screen not in self.sm.screens:
            self.sm.add_widget(self.chat_screen)
            self.ind+=1
        
        self.msg_builder(profile, self.chat_screen)
        self.chat_screen.text = profile['name']
        self.chat_screen.active = profile['active']
        self.change_screen(chat_name)

    def send_message(self, message):
        now = datetime.datetime.now()
        if message != "":
            if len(message) <= 5:
                message = message + "     "
            self.chatmsg = ChatBubble()
            self.chatmsg.msg = message
            self.chatmsg.time = now.strftime("%I:%M %p")
            self.chatmsg.isRead = 'delivered'
            self.chatmsg.sender = 'you'
            self.chat_screen.ids['msglist'].add_widget(self.chatmsg)
        self.chat_screen.ids.new_message.text = ""
        
    
    def chat_list_builder(self):
        # Create a Chat List Item for each user and add it to the Message List
        for profile in profiles:
            for msg in profile['msg']:
                self.chatitem = ChatListItem()
                self.chatitem.profile = profile
                self.chatitem.username = profile['name']

                lastMessage, time, isRead, sender = msg.split(";")
                self.chatitem.msg = lastMessage
                self.chatitem.timestamp = time
                self.chatitem.isRead = isRead
                self.chatitem.sender = sender

            self.sm.get_screen("msg").ids.chatTimeline.add_widget(self.chatitem)
    
    def msg_builder(self, profile, screen):
        # Create a message bubble for creating chat
        for prof in profile['msg']:
            for messages in prof.split("~"):
                if messages != "":
                    message, time, isRead, sender = messages.split(";")
                    self.chatmsg = ChatBubble()
                    self.chatmsg.msg = message
                    self.chatmsg.time = time
                    self.chatmsg.isRead = isRead
                    self.chatmsg.sender = sender
                    screen.ids['msglist'].add_widget(self.chatmsg)
                else:
                    print("No message")

                print(self.chatmsg.isRead)

    def press_dist(self):  
        self.start_lon = -73.9874499
        self.start_lat = 40.6931479
        self.end_lon = destination_long
        self.end_lat = destination_lat
        self.body = {"coordinates":[[self.start_lon,self.start_lat],[self.end_lon,self.end_lat]]}
        self.headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    		'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
    		'Content-Type': 'application/json; charset=utf-8'}
        self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body, headers=self.headers)
        self.string_res = self.call.text

        self.tag = 'rtept'
        self.reg_str = '</' + self.tag + '>(.*?)' + '>'
        self.res = re.findall(self.reg_str, self.string_res)
        self.string1 = str(self.res)
        self.tag1 = '"'
        self.reg_str1 = '"' + '(.*?)' + '"'
        self.res1 = re.findall(self.reg_str1, self.string1)
        for i in range(0, len(self.res1)-1, 2):
            self.points_lat = self.res1[i]
            print("PRINT:", self.points_lat)
            self.points_lon = self.res1[i+1]
            if (float(self.points_lat) not in crime_coord_lat) and (float(self.points_lon) not in crime_coord_long):
                self.points_pop = MapMarkerPopup(lat=self.points_lat, lon=self.points_lon, source='waypoints.png')
                self.route_points.append(self.points_pop)
                print(self.points_lat, self.points_lon)
                App.get_running_app().sm.get_screen("displaymap").ids.mapview.add_widget(self.points_pop)
            else:
                pass
            
        with App.get_running_app().sm.get_screen("displaymap").ids.mapview.canvas:
            Color(0.5, 0, 0 ,1)
            for j in range(0, len(self.route_points)-1, 1):
                self.lines = Line(points=(self.route_points[j].pos[0],self.route_points[j].pos[1], self.route_points[j+1].pos[0],self.route_points[j+1].pos[1] ), width=4)
                self.list_of_lines.append(self.lines)
        Clock.schedule_interval(self.update_route_lines, 1/50)
    
    def update_route_lines(self, *args):
        for j in range(1, len(self.route_points), 1):
            self.list_of_lines[j-1].points = [self.route_points[j-1].pos[0],self.route_points[j-1].pos[1], self.route_points[j].pos[0], self.route_points[j].pos[1]]
    

def calculate_danger_index(title):
    super_high = ["fatally", "fatal", "armed", "weapon", "knife", "knifepoint", "knife-wielding", "gun", "gunpoint","firearm", "machete", "stabbing", "stabbed", "shot", "shooting", "shots", "assault"]
    high = ["fire", "blaze", "ablaze", "robbery", "robbed", "broke into", "theft", "snatched", "shoplifter", "stolen"]
    med = ["police", "crash", "crashed", "collision", "hit-and-run", "hit", "wreck", "smash", "smashed", "assaulted", "injured", "hurt"]
    low = ["crowd", "march", "detained", "smoke", "EMS", "odor", "gas", "threats", "missing", "fight"]
    dubious = ["unfounded", "investigating"]

    for i in range(len(title)):
        danger_i = 0
        words = title.split()
        for word in words:
            if word.lower() in super_high:
                if word.lower() not in dubious:
                    danger_i += 4
                else: 
                    danger_i -= 1
            if word.lower() in high:
                if word.lower() not in dubious:
                    danger_i += 3
                else:
                    danger_i -= 1
            if word.lower() in med:
                if word.lower() not in dubious:
                    danger_i += 2
                else:
                    danger_i -= 1
            if word.lower() in low:   
                if word.lower() not in dubious:
                    danger_i += 1
                else: 
                    danger_i -= 1      
        if danger_i > 10:
            danger_i = 10
        if danger_i == 0:
                danger_i = 1
    return danger_i 


class CrimeData:
    def __init__(self, title, neighbourhood, address, date, time, DI, longitude, latitude):
        self.title = title
        self.neighbourhood = neighbourhood
        self.address = address
        self.date = date
        self.time = time
        self.DI = DI
        self.long = longitude
        self.lat = latitude
    


if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    SafeSailing().run()