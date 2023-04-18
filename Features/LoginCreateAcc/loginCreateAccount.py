from kivy.lang import Builder
from kivymd.app import MDApp
# from kivy.config import Config
# Config.set('kivy','keyboard_mode','systemanddock')
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from firebase import firebase

Window.size = (310, 580)

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp): 
    def build(self):
        kv = Builder.load_file('/Users/Malakhalifa/senior_proj/safe_sailing/Features/LoginCreateAcc/loginCreateAccount.kv')
        return kv

    def change_screen(self, screen: str):
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
                    self.change_screen('displaymap')

    def create_account(self, fname, lname, dob, email, password, homeadd, workadd):
        fb = firebase.FirebaseApplication('https://safesailing-f9c4c-default-rtdb.firebaseio.com', None)

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
                    
if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    MyApp().run()



