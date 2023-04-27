from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, DictProperty, OptionProperty, ObjectProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from demo import profiles
# from firebase import firebase

Window.size = (310, 580)

class WindowManager(ScreenManager):
    pass

class MessageScreen(Screen):
    # A screen that display the story fleets and all message histories.
    pass

class ChatScreen(Screen):
    # A screen that display messages with a user
    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(defaultvalue=False)

class ChatListItem(MDCard):
    # Clickable chat item for the chat screen
    isRead = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    username = StringProperty()
    msg = StringProperty()
    timestamp = StringProperty()
    profile = DictProperty()

class ChatBubble(MDBoxLayout):
    # A chat bubble for the chat screen messages.

    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    isRead = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])

class Message(MDLabel):
    # A adaptive text for the chat bubble.'''
    pass 

class MyChat(MDApp): 
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.accent_hue = '400'
        self.title = "Messages"
        
        # back button does not work in main_chat.kv
        Builder.load_file("/Users/Malakhalifa/senior_proj/safe_sailing/Features/CommunicateUsers/main_chat.kv")
        
        sm = ScreenManager()
        self.sm = sm
        screens = [MessageScreen(name="allmessages"), ChatScreen(name='chat')]
        for screen in screens:
            sm.add_widget(screen)

        self.chat_list_builder()
        return self.sm
    
    def change_screen(self, screen: str):
        self.sm.current = screen

    def create_chat(self, profile):
        # Get all messages and create a chat screen
        self.chat_screen = ChatScreen()
        self.msg_builder(profile, self.chat_screen)
        self.chat_screen.text = profile['name']
        self.chat_screen.active = profile['active']
        self.sm.switch_to(self.chat_screen)
    
    def chat_list_builder(self):
        # Create a Chat List Item for each user and add it to the Message List
        for profile in profiles:
            for msg in profile['msg']:
                self.chatitem = ChatListItem()
                self.chatitem.profile = profile
                self.chatitem.username = profile['name']

                lastMessage, time, isRead, sender = msg.split(";")
                self.chatitem.msg = lastMessage
                self.chatitem.timestamp = time
                self.chatitem.isRead = isRead
                self.chatitem.sender = sender

            self.sm.screens[0].ids['chatTimeline'].add_widget(self.chatitem)

    # Given user's final destination, go through database andfind all users with the same final destination 
    # display all the users in the messages page 
    
    def msg_builder(self, profile, screen):
        # Create a message bubble for creating chat
        for prof in profile['msg']:
            for messages in prof.split("~"):
                if messages != "":
                    message, time, isRead, sender = messages.split(";")
                    self.chatmsg = ChatBubble()
                    self.chatmsg.msg = message
                    self.chatmsg.time = time
                    self.chatmsg.isRead = isRead
                    self.chatmsg.sender = sender
                    screen.ids['msglist'].add_widget(self.chatmsg)
                else:
                    print("No message")

                print(self.chatmsg.isRead)

if __name__ == '__main__':
    LabelBase.register(name = 'MPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-Medium.ttf')
    LabelBase.register(name = 'MPoppinsBold', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')
    LabelBase.register(name = 'BPoppins', fn_regular='/Users/Malakhalifa/senior_proj/safe_sailing/Features/FontPoppins/Poppins-SemiBold.ttf')

    MyChat().run()