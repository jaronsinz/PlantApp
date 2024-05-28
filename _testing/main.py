import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MainGrid(Widget):
    output = ObjectProperty(None)

    def say_hello(self):
        self.output.text = "Hello World"
    


class PlantApp(App):
    def build(self):
        return MainGrid()
    
    
if __name__ == "__main__":
    PlantApp().run()

