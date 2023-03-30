import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

from kivy.lang import Builder
from kivymd.app import MDApp

#import features

from Features.Login.login import LoginClass


class MyApp(App):

    def build(self):    
        #return Label(text='Welcome to Safe Sailing!')
        return LoginClass().build()
    
if __name__ == '__main__':
    MyApp().run()