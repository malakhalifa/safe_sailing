import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
# from Features.Login.login import LoginClass
# from Features.CreateAccount.createaccount import CreateAccountClass
# from Features.RateComment.ratecomment import RateCommentClass

Window.size = (310, 580)
class MyApp(MDApp):
    def build(self):
        screen_manager = ScreenManager() 
        screen_manager.add_widget(Builder.load_file('Features/MainPage/main.kv'))
        screen_manager.add_widget(Builder.load_file('Features/Login/login.kv'))
        screen_manager.add_widget(Builder.load_file('Features/CreateAccount/CreateAccount.kv'))
        # screen_manager.add_widget(Builder.load_file('Features/RateComment/ratecomment.kv'))

        return screen_manager

# Can't figure out how to integrate multiple .py files into one (main)
# Can't figure out how to implement functionality in main     
    
if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='Features/FontPoppins/Poppins-SemiBold.ttf')

    MyApp().run()