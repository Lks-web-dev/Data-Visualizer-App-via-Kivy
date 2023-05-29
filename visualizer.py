from kivy.app import App
from kivy.clock import Clock
from kivy.core.window.window_x11 import Config

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import pandas as pd
from plyer import filechooser
from matplotlib import pyplot as plt
import awkward as ak  # maybe he woks with flatten() ?
import math

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '600')
Config.write()


class Image_btn(ButtonBehavior, Image):
    pass


class Interface(BoxLayout):
    obj_dict = {}
    colomn_dict = {}
    files = ""
    file_address = {}
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def binder(self, checkbox, value):
        if value:
            print(self.obj_dict[checkbox], "Ajouté")  # added
        else:
            print(self.obj_dict[checkbox], "retiré")  # removed

    def upload(self, dt):
        # files retourne le répertoire
        self.files = filechooser.open_file(title="Choose excel files", filter=[["*.xlsx"]], multiple=True)
        for file in self.files:
            file_name = file.split('/')[-1]
            self.file_address[file_name] = file
            print(file_name)
            box = BoxLayout(size_hint_y=None, height=20, padding=[30, 0, 0, 0])
            checkbox = CheckBox(size_hint_x=.25, background_checkbox_normal="checkbox_nor.png", background_checkbox_down="checkbox_tic.png")
            checkbox.bind(active=self.binder)
            label = Label(text=f'[color=#3f51b5]{file_name}[/color]', markup=True)
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.file_placeholder.add_widget(box)
            self.obj_dict[checkbox] = file_name
        columns = pd.read_excel(self.files[0]).columns.values.tolist()
        for column in columns:
            box = BoxLayout(size_hint_y=None, height=20, padding=[30, 0, 0, 0])
            checkbox = CheckBox(size_hint_x=.25, background_checkbox_normal="checkbox_nor.png",
                                background_checkbox_down="checkbox_tic.png")
            label = Label(text=f'[color=#3f51b5]{column}[/color]', markup=True, text_size=(170, None))
            box.add_widget(checkbox)
            box.add_widget(label)
            self.colomn_dict[checkbox] = column
            self.ids.property_placeholder.add_widget(box)
        
        self.ids.upload_btn.source = "Drag.png"

    def update(self):
        # Afin de mettre à jour le graph, on vérifie s'il y a un children (un graph déjà déssiné)
        # Puis on remove ce widget
        children = self.ids.graph_placeholder.children
        if children:  # ça peut être plusieurs
            self.ids.graph_placeholder.remove_widget(children[0])

        # x_axis = []
        # Ici on va définir le nombre de graphique
        files_leg = len(self.files)
        row_col = math.ceil(files_leg / 2)
        print(row_col)
        fig, axis = plt.subplots()
        # flatten_axis = axis.flatten().tolist()
        # print(flatten_axis)
        # Récupération des fichiers en fonction de la key
        properties_checkbox = self.colomn_dict.keys()
        files_checkbox = self.obj_dict.keys()  # on veut juste récupérer une liste de clef
        plt.gcf().autofmt_xdate()
        for index, file_checkbox in enumerate(files_checkbox):
            y_axis = []
            if file_checkbox.active:
                file_name = self.obj_dict[file_checkbox]
                file_address = self.file_address[file_name]
                content = pd.read_excel(file_address)
                print(content)
                for property_checkbox in properties_checkbox:
                    if property_checkbox.active:
                        if self.colomn_dict[property_checkbox] == "annee_numero_de_tirage":
                            x_axis = content[self.colomn_dict[property_checkbox]]
                        else:
                            y_axis.append(content[self.colomn_dict[property_checkbox]])
                for y in y_axis:
                    plt.bar(x_axis.to_numpy(), y.to_numpy())
        self.ids.graph_placeholder.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def upload_menu(self):
        self.ids.upload_btn.source = "Drop.png"
        Clock.schedule_once(self.upload)

    def switching(self):
        self.ids.sm.current = "visualizer_window"


class VisualizerApp(App):
    pass


if __name__ == "__main__":
    VisualizerApp().run()
