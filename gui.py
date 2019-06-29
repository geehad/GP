import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 3

        self.inside.add_widget(Label(text="what do you think ... ? "))

        self.inside.inside = GridLayout()
        self.inside.inside.rows = 2
        self.description = TextInput(multiline=True)
        self.inside.inside.add_widget(self.description)

        self.inside.inside.inside = GridLayout()
        self.inside.inside.inside.cols = 2
        # size_hint_max_y= 0.5
        self.visualize = Button(text="Animate", font_size=15)
        self.visualize.bind(on_press=self.play)
        self.inside.inside.inside.add_widget(self.visualize)

        self.clear = Button(text="clear", font_size=15)
        self.clear.bind(on_press=self.pressed)
        self.inside.inside.inside.add_widget(self.clear)

        self.inside.inside.add_widget(self.inside.inside.inside)
        self.inside.add_widget(self.inside.inside)
        self.add_widget(self.inside)

        self.player = VideoPlayer(source='hjk.MP4', state='stop',
                                  options={'allow_stretch': True})
        self.add_widget(self.player)

    def pressed(self, instance):
        name = self.description.text
        print("scene:", name)
        self.description.text = ""

    def play(self, instance):
        self.player.state = 'play'
        input_text=self.description.text
        print( input_text ) ###########-----> to do send to NLP_module

class MyApp(App):
    def build(self):
        self.title = 'Animare'
        self.icon = 'Animare_logo.png'
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()