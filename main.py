import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.core.text import LabelBase
from Features.Login.login import LoginClass

class MyApp(App):

    def build(self):    
        #return Label(text='Welcome to Safe Sailing!')
        return LoginClass().build()
    
if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='Features/Login/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='Features/Login/FontPoppins/Poppins-SemiBold.ttf')

    MyApp().run()