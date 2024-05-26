from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout


class HomeScreen(GridLayout): 
    pass
    

class PlantApp(App):
    def build(self):
        root = HomeScreen()
    
    def say_hello(self):
        print("Hello world")


if __name__ == '__main__':
    PlantApp().run()
    
