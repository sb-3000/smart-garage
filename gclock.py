import time, threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class DigitalClock(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        self.laDate = Gtk.Label("Date", xalign=0)
        self.pack_start(self.laDate, True, True, 0)
        
        self.laTime = Gtk.Label("Time", xalign=0)
        self.pack_start(self.laTime, True, True, 0)

    def start(self):
        thread = threading.Thread(target=self.update_time_info)
        thread.daemon = True
        thread.start()

    def update_time_info(self):
        while True:
            GLib.idle_add(self.update_ui)
            time.sleep(10)

    def update_ui(self):
        self.laDate.set_text(time.strftime('  %A, %b %d'))
        self.laTime.set_text(time.strftime('  %I:%M %p'))
        return False
