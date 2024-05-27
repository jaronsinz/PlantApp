import kivy
from kivy.app import App
from kivy.uix.label import Label

class PlantApp(App):
    def build(self):
        return Label(text="PlantApp")
    
if __name__ == "__main__":
    PlantApp().run()

