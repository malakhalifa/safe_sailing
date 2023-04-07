import kivy
kivy.require('2.1.0') # replace with your current kivy version !
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

Window.size = (310, 580)

class RateCommentClass(MDApp):
    def build(self):
        kv = Builder.load_file('Features/RateComment/ratecomment.kv')
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
        self.root.ids.text.text = "It was somewhat unsafe"

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
    LabelBase.register(name = 'MPoppins', fn_regular='Feature/RateComment/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='Features/RateComment/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='Features/RateComment/FontPoppins/Poppins-SemiBold.ttf')

    RateCommentClass().run()
