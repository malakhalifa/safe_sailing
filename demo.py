from firebase import firebase
import requests


chats = {

    "anita": ["hi! We're going to the same place ;2:20 PM;read;you", "hi whats up;2:20 PM;read;friend", "how are you doing?;2:20 PM;read;you","doing great you?;2:20 PM;waiting;friend", 
        "staying alive;2:20 PM;delivered;you"],
    "zendaya": ["hi! We're going to the same place ;2:20 PM;read;you","hi whats up;2:20 PM;read;friend", "how are you doing?;2:20 PM;read;you","doing great you?;2:20 PM;waiting;friend", 
        "Did you see that guy get stabbed? ;2:20 PM;delivered;you"],
    "rihanna": ["hi! We're going to the same place ;2:20 PM;read;you","hi whats up;2:20 PM;read;friend", "how are you doing?;2:20 PM;read;you","doing great you?;2:20 PM;waiting;friend", 
        "I'm excited to take the I-78 home!;2:20 PM;delivered;you"],
} 


anita = {
    "name": "Anita",
    "active": True,
    "msg": chats["anita"],
    }

zendaya = {
    "name": "Zendaya",
    "active": False,
    "msg": chats["zendaya"],
    }

rihanna = {
    "name": "Rihanna",
    "active": True,
    "msg": chats["rihanna"],
    }

profiles = [anita, zendaya, rihanna]

    
   