from kivy.lang import Builder
from kivymd.app import MDApp

class LoginClass(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('Features/Login/login.kv')


