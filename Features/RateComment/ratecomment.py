import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp

Window.size = (310, 580)

class RateCommentClass(MDApp):
    def build(self):
        kv = Builder.load_file('Features/RateComment/ratecomment.kv')
        dropdown = DropDown()
        for i in range(5):
            btn = Button(text='Route %d' % i, font_size=25, background_color=(169/255, 0, 230/255, 1), size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Choose Route', font_size=25, background_color=(52/255, 0, 231/255, 1), size_hint=(None, None), height=70, width=200, pos=(200, 650))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        kv.add_widget(mainbutton)
        return kv

    
    def select1(self):
        self.root.ids.star1.opacity = 1
        self.root.ids.star2.opacity = 0.5
        self.root.ids.star3.opacity = 0.5
        self.root.ids.star4.opacity = 0.5
        self.root.ids.star5.opacity = 0.5
        self.root.ids.text.text = "It was horrible."

    def select2(self):
        self.root.ids.star1.opacity = 0.5
        self.root.ids.star2.opacity = 1
        self.root.ids.star3.opacity = 0.5
        self.root.ids.star4.opacity = 0.5
        self.root.ids.star5.opacity = 0.5
        self.root.ids.text.text = "It was somewhat unsafe ~"

    def select3(self):
        self.root.ids.star1.opacity = 0.5
        self.root.ids.star2.opacity = 0.5
        self.root.ids.star3.opacity = 1
        self.root.ids.star4.opacity = 0.5
        self.root.ids.star5.opacity = 0.5
        self.root.ids.text.text = "It was alright, but it could have been better."

    def select4(self):
        self.root.ids.star1.opacity = 0.5
        self.root.ids.star2.opacity = 0.5
        self.root.ids.star3.opacity = 0.5
        self.root.ids.star4.opacity = 1
        self.root.ids.star5.opacity = 0.5
        self.root.ids.text.text = "It was good!"

    def select5(self):
        self.root.ids.star1.opacity = 0.5
        self.root.ids.star2.opacity = 0.5
        self.root.ids.star3.opacity = 0.5
        self.root.ids.star4.opacity = 0.5
        self.root.ids.star5.opacity = 1
        self.root.ids.text.text = "It was perfect."

if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='Features/FontPoppins/Poppins-SemiBold.ttf')

    RateCommentClass().run()
