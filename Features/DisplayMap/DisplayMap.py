from kivymd.app import MDApp
from kivy_garden.mapview import MapView

class DisplayMap(MDApp):
    def build(self):
        mapView = MapView(zoom=12, lat=37.4419, lon=-122.1419)
        return mapView
    
DisplayMap().run()

