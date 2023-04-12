import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp

import json
import datetime

Window.size = (310, 580)

class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

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

class SafetyNotifClass(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        self.table = None

    def build(self):
        kv = Builder.load_file('safe_sailing/Features/ViewSafetyNotifications/safetynotif.kv')
        return kv

    def add_datatable(self):

        jsonFile = open('safe_sailing/Features/ViewSafetyNotifications/raw_response.json', "r")
        crime = json.load(jsonFile)

        self.table = MDDataTable(
            use_pagination = True,
            pos_hint = {'center_x': 0.5, 'center_y':0.3},
            size_hint = (0.9,0.5),
            
            column_data = [
                ("Incident", dp(50)), 
                ("Address", dp(40)),
                ("Neighbourhood", dp(25)),
                ("Date", dp(20)),
                ("Time (EST)", dp(20)),
                ("DI", dp(10))
            ],
            row_data = []
        )
        
        for j in range (20):
            title = crime['results'][j]['title']
            neighbourhood = crime['results'][j]['neighborhood']
            address = crime['results'][j]['address']
            longitude = crime['results'][j]['longitude']
            latitude = crime['results'][j]['latitude']
            timestamp = crime['results'][j]['ts']
            
            json_timestamp = timestamp / 1000  # convert milliseconds to seconds
            date = datetime.datetime.fromtimestamp(json_timestamp, datetime.timezone.utc)
            time = date.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
            est_date = time.strftime("%m/%d/%Y")
            est_time = time.strftime("%I:%M:%S %p")
            DI = calculate_danger_index(title)
            cdata = CrimeData(title, neighbourhood, address, est_date, est_time, DI, longitude, latitude)
            row = [title, address, neighbourhood, est_date, est_time, DI]
            self.table.row_data.append(row)


        jsonFile.close()
        self.root.ids.data_scr.ids.data_layout.add_widget(self.table)
    
    def change_screen(self, screen: str):
        self.root.current = screen


if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    SafetyNotifClass().run()
