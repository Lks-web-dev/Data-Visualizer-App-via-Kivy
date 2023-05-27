
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window.window_x11 import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from plyer import filechooser

Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')
Config.write()


class Image_btn(ButtonBehavior, Image):
    pass


class Interface(BoxLayout):
    def upload(self, dt):
        # files retourne le répertoire
        files = filechooser.open_file(title="Choose excel files", filter=[["*.xlsx"]], multiple=True)
        print(files)
        self.ids.upload_btn.source = "Drag.png"

    def upload_menu(self):
        self.ids.upload_btn.source = "Drop.png"
        Clock.schedule_once(self.upload)

    def switching(self):
        self.ids.sm.current = "visualizer_window"




class VisualizerApp(App):
    pass


if __name__ == "__main__":
    VisualizerApp().run()
