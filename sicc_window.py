import os

from gi.repository import Gtk, GObject, Gdk

gtk_builder_file = os.path.splitext(__file__)[0] + '.ui'

class SiccWindow(object):
    def __init__(self, *args, **kwargs):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gtk_builder_file)

        self.window = self.builder.get_object('main_window')
        self.window.connect('destroy', self.signal_window_destroy)
        self.window.show()

    def signal_window_destroy(self, _):
        self.window.destroy()
        Gtk.main_quit()
