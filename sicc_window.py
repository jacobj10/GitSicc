import os
import gi
import math
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject, Gdk
from sicc import GitAssistant

gtk_builder_file = os.path.splitext(__file__)[0] + '.ui'

COLOR_CYCLE = [
                ('#ffffff'), ('#d6e685'),
                ('#8cc665'), ('#44a340'),
                ('#1e6823')
            ]

class SiccWindow(object):
    def __init__(self, *args, **kwargs):
        self.color_to_counter = {}

        for color in COLOR_CYCLE:
            self.color_to_counter[color] = 0

        self.assistant = GitAssistant()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gtk_builder_file)

        self.window = self.builder.get_object('main_window')
        self.window.connect('destroy', self.signal_window_destroy)

        self.grid = self.builder.get_object('calendar_grid')

        self.entry = self.builder.get_object('date_entry')
        self.entry.connect('changed', self.signal_entry_changed)
        self.entry.set_text('2016')

        self.export = self.builder.get_object('export')
        self.export.connect('clicked', self.signal_export)

        self.window.show_all()

    def signal_window_destroy(self, _):
        self.window.destroy()
        Gtk.main_quit()

    def populate_calendar(self, cols, last, beginning):
        for child in self.grid.get_children():
            self.grid.remove(child)
        for i in range(cols + 1):
            for j in range(7):
                if i == cols and j >= last:
                    continue
                button = Gtk.Button()
                button.connect('clicked', self.signal_button_press)
                rgb = Gdk.RGBA()
                rgb.parse(COLOR_CYCLE[0])
                button.override_background_color(Gtk.StateFlags.NORMAL, rgb)
                self.grid.attach(button, i, j, 1, 1)

        self.grid.show_all()

    def signal_button_press(self, button):
        curr = button.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        counter = 0
        color = COLOR_CYCLE[counter]
        rgb = Gdk.RGBA()
        rgb.parse(color)
        while not rgb.equal(curr):
            counter = (counter + 1) % len(COLOR_CYCLE)
            color = COLOR_CYCLE[counter]
            rgb.parse(color)
        rgb.parse(COLOR_CYCLE[(counter + 1) % len(COLOR_CYCLE)])
        button.override_background_color(Gtk.StateFlags.NORMAL, rgb)
        if counter % len(COLOR_CYCLE) != 0:
            self.color_to_counter[COLOR_CYCLE[counter % len(COLOR_CYCLE)]] -= 1
        if (counter + 1) % len(COLOR_CYCLE) != 0:       
            self.color_to_counter[COLOR_CYCLE[(counter + 1) % len(COLOR_CYCLE)]] += 1

    def signal_entry_changed(self, text):
        text = text.get_text()
        if text.isnumeric() and int(text) > 1900 and int(text) < 3000:
            self.year = int(text)
            self.params = self.assistant.calculate_start_date(self.year)
            self.populate_calendar(self.params[0], self.params[1], self.params[2])

    def signal_export(self, _):
        color_max = 0
        counter = len(COLOR_CYCLE) - 1
        while counter > 0:
            if self.color_to_counter[COLOR_CYCLE[counter]] != 0:
                color_max = counter
                counter = -1
            counter -= 1
        mask = self.get_mask()
        for color in mask:
            if color != 0 :
                if color != math.ceil(int(color * 1.0 / color_max * 100) / 25):
                    
        startday = self.params[2].toordinal()
        self.assistant.generate_repo(startday, mask)

    def get_mask(self):
        mask = []
        for i in range(self.params[0] + 1):
            for j in range(7):
                if i == self.params[0] and j >= self.params[1]:
                    break
                button = self.grid.get_child_at(i, j)

                curr = button.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
                counter = 0
                color = COLOR_CYCLE[counter]
                rgb = Gdk.RGBA()
                rgb.parse(color)
                while not rgb.equal(curr):
                    counter = (counter + 1) % len(COLOR_CYCLE)
                    color = COLOR_CYCLE[counter]
                    rgb.parse(color)
                mask.append(counter)
        return mask
if __name__ == '__main__':
    x = SiccWindow()
    Gtk.main()
