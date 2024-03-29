import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from geopy.geocoders import Nominatim, GoogleV3 

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy_garden.mapview import MapMarker, MapMarkerPopup, MapView
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog, MDInputDialog
from kivy.clock import Clock

from urllib import parse
from kivy.network.urlrequest import UrlRequest #can also use requests, see test.py
# from apikey_ import apikey_
import certifi
# For snackbar
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

import config

import requests
import re

import time

Window.size = (310, 580)

from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
 
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from kivy.uix.widget import Widget 
from kivy.clock import Clock

class ImageButton(ButtonBehavior, Image):
    pass
 
class LabelButton(ButtonBehavior, Label):
    pass

class HomeMapView(MapView):
    pass

class HomeScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class fscreen(Widget):
	my_avat = StringProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.list_of_lines = []
		self.route_points = []
		self.placed = False
		self.exists = False
		self.ids.main_map.zoom = 15
		self.ids.main_map.center_on(self.ids.main_map_me.lat, self.ids.main_map_me.lon)
		self.my_avat = 'avatar.png'

	def press_dist(self, instance):
		print(self.dist.lat)
		print(self.dist.lon)

		self.start_lon = -73.986707
		self.start_lat = 40.694011

		self.end_lon = 73.9973 
		self.end_lat = 40.7309
		self.body = {"coordinates":[[self.start_lon,self.start_lat],[self.end_lon,self.end_lat]]}
		self.headers = {
    		'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    		'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
    		'Content-Type': 'application/json; charset=utf-8'}
		self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body, headers=self.headers)
		print(self.call.text)
		self.string_res = self.call.text

		print(self.string_res)

		self.tag = 'rtept'
		self.reg_str = '</' + self.tag + '>(.*?)' + '>'
		self.res = re.findall(self.reg_str, self.string_res)
		print(self.res)
		print('_____________________________________')
		self.string1 = str(self.res)
		self.tag1 = '"'
		self.reg_str1 = '"' + '(.*?)' + '"'
		self.res1 = re.findall(self.reg_str1, self.string1)
		print(self.res1)

		for i in range(0, len(self.res1)-1, 2):
			print('lat= ' + self.res1[i])
			print('lon= ' + self.res1[i+1])

			self.points_lat = self.res1[i]
			self.points_lon = self.res1[i+1]

			self.points_pop = MapMarkerPopup(lat=self.points_lat, lon=self.points_lon, source='waypoints.png')
			self.route_points.append(self.points_pop)

			self.ids.main_map.add_widget(self.points_pop)

		with self.canvas:
			Color(0.5, 0, 0 ,1)
			for j in range(0, len(self.route_points)-1, 1):
				self.lines = Line(points=(self.route_points[j].pos[0],self.route_points[j].pos[1], self.route_points[j+1].pos[0],self.route_points[j+1].pos[1] ), width=4)
				self.list_of_lines.append(self.lines)

		Clock.schedule_interval(self.update_route_lines, 1/50)
	def update_route_lines(self, *args):
		for j in range(1, len(self.route_points), 1):
			self.list_of_lines[j-1].points = [self.route_points[j-1].pos[0],self.route_points[j-1].pos[1], self.route_points[j].pos[0], self.route_points[j].pos[1]]								


class HomeGpsHelper():
    has_centered_map = False
    dialog = None
    def run(self):
        # Get a reference to GpsBlinker, then call blink()
        #while True:
        home_gps_blinker = App.get_running_app().root.ids.home_screen.ids.mapview.ids.blinker 
        #time.sleep(1)
 
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
 
            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

 
    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position
        # home_gps_blinker = App.get_running_app().root.ids.home_screen.ids.mapview.ids.blinker
        home_gps_blinker = App.get_running_app().root.sm.get_screen("home_screen").ids.mapview.ids.blinker
        home_gps_blinker.lat = my_lat
        home_gps_blinker.lon = my_lon
 
        # Center map on gps
        if not self.has_centered_map:
            # map2 = App.get_running_app().root.ids.home_screen.ids.mapview
            map2 = App.get_running_app().root.sm.get_screen("home_screen").ids.mapview
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
 
    # blink --> outer_opacity = 0, blink_size = 50
    # reset --> outer_opacity = 1, blink_size = default = 25

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
            app = App.get_running_app()
            mapview = app.root.ids.home_screen.ids.mapview
            mapview.center_on(latitude, longitude)

        except:
            Snackbar(text="Address not found, please try other addresses.", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            pass

    def geocode_get_lat_lon(self, address):
        #GEOCODER KEY HERE
        # address = parse.quote(address)
        # url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=%s&apiKey=%s"%(address, api_key)
        # UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error, ca_file=certifi.where())
        #certifi directs our apps to ssl certificate
        geolocator = GoogleV3(config.google_api_key)
        location = geolocator.geocode(address)
        # print(location.latitude, location.longitude)
        log_lat = [location.latitude,location.longitude]
        self.success(log_lat)
        # call class fscreen(Widget)
        fscreen().update_map(log_lat)
 
    def error(self, urlrequest, result):
        print("Error")
        print(result)
 
    def failure(self, urlrequest, result):
        print("Failure")
        print(result)

class DisplayMap(MDApp):

    search_menu = None

    current_lat = 40.694011
    current_lon = -73.986707

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        # Instantiate SearchPopupMenu
        self.search_menu = SearchPopupMenu()

        Builder.load_file('DisplayMap.kv')

        self.sm = ScreenManager()
        screens = [HomeScreen(name="home_screen")]
        for screen in screens:
            self.sm.add_widget(screen)
            
        # Initialize GPS
        HomeGpsHelper().run()

    def change_screen(self, screen_name, direction='forward', mode = ""):
        # Get the screen manager from the kv file.
        screen_manager = self.root.ids.screen_manager
 
        if direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return
 
        screen_manager.transition = CardTransition(direction=direction, mode=mode)
        screen_manager.current = screen_name
 
        if screen_name == "home_screen":
            self.root.ids.titlename.title = "Sg Transport"

            
if __name__ == '__main__':
    DisplayMap().run()

