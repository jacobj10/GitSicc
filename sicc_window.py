import os

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject, Gdk

gtk_builder_file = os.path.splitext(__file__)[0] + '.ui'

COLOR_CYCLE = [
                ('#ffffff'), ('#d6e685'),
                ('#44a340'), ('#28752d'),
                ('#1e6823'), ('#365e2f'),
                ('#144e12')
            ]

class SiccWindow(object):
    def __init__(self, *args, **kwargs):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gtk_builder_file)

        self.window = self.builder.get_object('main_window')
        self.window.connect('destroy', self.signal_window_destroy)

        self.grid = self.builder.get_object('calendar_grid')

        self.populate_calendar(52, 3, 1)
        self.window.show_all()

    def signal_window_destroy(self, _):
        self.window.destroy()
        Gtk.main_quit()

    def populate_calendar(self, cols, last, beginning):
        for i in range(cols):
            for j in range(7):
                if i == cols - 1 and j > last:
                    continue
                button = Gtk.Button()
                button.connect('clicked', self.signal_button_press)
                rgb = Gdk.RGBA()
                rgb.parse(COLOR_CYCLE[0])
                button.override_background_color(Gtk.StateFlags.NORMAL, rgb)
                self.grid.attach(button, i, j, 1, 1)

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
        print((counter + 1) % len(COLOR_CYCLE))
