from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from prune_and_extract_text import extract_text, match

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    input_image = ObjectProperty(None)
    input_file_path = ""
    input_file_name = ""

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.ids.input_image.source = os.path.join(path, filename[0])
        self.dismiss_popup()
        self.input_file_path = path
        self.input_file_name = filename[0]

    def save(self):
        input_image_path = os.path.join(self.input_file_path, self.input_file_name)
        os.system("python detect.py --source " + input_image_path + " --weights weights/last.pt --save-txt")
        output_image_path = "./inference/output/" + self.input_file_name.replace(self.input_file_path,"")
        cropped_image_path = output_image_path.replace(".jpg", "_cropped.jpg")
        print(cropped_image_path)
        self.ids.output_image.source = output_image_path
        extract_num = extract_text(cropped_image_path, 'out')
        suspected_plates = ""
        if len(extract_num) > 2:
            suspected_plates = match(extract_num)
        if suspected_plates == "":
            suspected_plates = "NO MATCH FOUND, NOT STOLEN"
        self.ids.plate_number.text = "\nPLATE NUMBER: " + extract_num + "\n" + "SUSPECTED PLATES: " + suspected_plates

class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Editor().run()

