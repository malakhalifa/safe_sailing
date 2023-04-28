import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase

Window.size = (310, 580)

class CallWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class SafetyNotifClass(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        self.table = None

    def build(self):
        kv = Builder.load_file('/Users/Malakhalifa/senior_proj/safe_sailing/Features/CallFirstResponder/callresponder.kv')
        return kv
    
    def change_screen(self, screen: str):
        self.root.current = screen


if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    SafetyNotifClass().run()