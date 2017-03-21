from sicc_window import SiccWindow
from sicc import GitAssistant
from gi.repository import Gtk, GObject, Gdk


y = GitAssistant()
y.generate_repo(13000, [1,1,3,1])
x = SiccWindow()
Gtk.main()

