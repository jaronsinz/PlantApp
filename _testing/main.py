import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.rows = 2
        self.add_widget(Label(text="Oberer Bereich"))
        menu = Menu()
        self.add_widget(menu)

class Menu(GridLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.cols = 4
        self.add_widget(Label(text="Pflanzen"))
        self.add_widget(Label(text="Aufgaben"))
        self.add_widget(Label(text="Pflanze Hinzufügen"))


class PlantApp(App):
    def build(self):
        return MyGrid()
    
if __name__ == "__main__":
    PlantApp().run()

