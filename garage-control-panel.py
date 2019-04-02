#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

import sys, os, time, json, argparse

import gclock, time

try:
    from RPi import GPIO
except ImportError:
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi
    from RPi import GPIO
    from fake_rpi import toggle_print
    toggle_print(False)

GARAGE_1_DOOR_PIN  = 19
GARAGE_1_LIGHT_PIN = 26
GARAGE_2_DOOR_PIN  = 20
GARAGE_2_LIGHT_PIN = 21
MOTION_DETECTOR_PIN = 17

class BigButton(Gtk.Button):

     def __init__(self, label = None, image = None):
        Gtk.Button.__init__(self)

        vbox = Gtk.VBox();
        vbox.set_spacing(5);
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        self.add(vbox)

        if label is not None:
            la_title = Gtk.Label(label, xalign=0.5)
            la_title.get_style_context().add_class("la_header")
            vbox.pack_start(la_title, True, True, 0)

        if image is not None:
            img = Gtk.Image()
            img.set_from_file(image)
            vbox.pack_start(img, False, False, 0)

        if label is not None:
            la_status = Gtk.Label("Closed", xalign=0.5)
            vbox.pack_start(la_status, True, True, 0)

        self.set_can_focus(False)

class MainWindow(Gtk.Window):

    def __init__(self, full_screen, motion_enabled, camera_enabled):
        self.__is_fullscreen = False
 
        Gtk.Window.__init__(self, title="Smart Garage", type=Gtk.WindowType.TOPLEVEL)
        self.set_default_size(800, 480)
        self.set_border_width(0)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        context = Gtk.StyleContext()
        context.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        # window background
        background = Gtk.Image.new_from_file('background.jpg')
        self.fixed.put(background, 0, 0)

        event_box = Gtk.EventBox()
        event_box.set_size_request(50, 50)
        self.fixed.put(event_box, 0, 0)
        event_box.connect("button_press_event", lambda w, e: Gtk.main_quit())

        button = BigButton("Door S", "garage.png")
        button.connect("clicked", self.set_pin_high, GARAGE_1_DOOR_PIN)
        button.set_size_request(150, 150)
        self.fixed.put(button, 50, 180)

        button = BigButton(image="bulb.png")
        button.connect("clicked", self.set_pin_high, GARAGE_1_LIGHT_PIN)
        button.set_size_request(150, 80)
        self.fixed.put(button, 50, 350)

        button = BigButton("Door T", "garage.png")
        button.set_size_request(150, 150)
        self.fixed.put(button, 250, 180)
        button.connect("clicked", self.set_pin_high, GARAGE_2_DOOR_PIN)

        button = BigButton(image="bulb.png")
        button.set_size_request(150,80)
        self.fixed.put(button, 250, 350)
        button.connect("clicked", self.set_pin_high, GARAGE_2_LIGHT_PIN)

        self.clock = gclock.DigitalClock()
        self.fixed.put(self.clock, 600, 40)
        self.clock.start()
 
        box = Gtk.Box()
        box.set_size_request(260,250)
        box.get_style_context().add_class("tile_webcam")
        self.fixed.put(box, 450, 180)
        
        self.connect("realize", self.realize_cb)
        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event", self.on_win_key_press_event)
        self.connect("window-state-event", self.on_window_state_event)

        self.la_motion = Gtk.Label("Motion: Not detected")
        self.fixed.put(self.la_motion, 330, 450)

        if full_screen:
            self.fullscreen_mode()

        self.show_all()

    def realize_cb(self, widget):
        cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR)
        #window = Gtk.Widget.get_window(widget)
        window = widget.get_window()
        window.set_cursor(cursor)
    
    def fullscreen_mode(self):
        if self.__is_fullscreen:
            self.unfullscreen()
        else:
            self.fullscreen()

    def on_win_key_press_event(self, widget, ev):
        key = Gdk.keyval_name(ev.keyval)
        if key == "f":
            self.fullscreen_mode()
        elif key == "q":
            Gtk.main_quit()

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)

    def set_pin_high(self, widget, data=None):
        print('Set pin {} high'.format(data))
        GPIO.output(data, GPIO.LOW)
        time.sleep(0.1)
        print('Set pin {} low'.format(data))
        GPIO.output(data, GPIO.HIGH)

class GarageControlPanel(object):

    def __init__(self, full_screen, motion_enabled, camera_enabled):
        self.motion_enabled = motion_enabled
        self.motion_detected = 0

        self.init_gpio()
        self.mwin = MainWindow(full_screen, motion_enabled, camera_enabled)
        
        GObject.timeout_add(100, self.update_motion)
        
    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(GARAGE_1_DOOR_PIN, GPIO.OUT)
        GPIO.output(GARAGE_1_DOOR_PIN, GPIO.HIGH)
        GPIO.setup(GARAGE_1_LIGHT_PIN, GPIO.OUT)
        GPIO.output(GARAGE_1_LIGHT_PIN, GPIO.HIGH)
        GPIO.setup(GARAGE_2_DOOR_PIN, GPIO.OUT)
        GPIO.output(GARAGE_2_DOOR_PIN, GPIO.HIGH)
        GPIO.setup(GARAGE_2_LIGHT_PIN, GPIO.OUT)
        GPIO.output(GARAGE_2_LIGHT_PIN, GPIO.HIGH)

        GPIO.setup(MOTION_DETECTOR_PIN, GPIO.IN)

    def update_motion(self):
        if not self.motion_enabled:
            return

        state = GPIO.input(MOTION_DETECTOR_PIN)
        self.mwin.la_motion.set_label('Motion: {} at {}'.format(state, time.strftime(' %M:%S')))
        if self.motion_detected == 0 and state == 1:
            os.system("xset dpms force on")
        
        self.motion_detected = state
        return True

parser = argparse.ArgumentParser(description='Smart Garage Control Panel')
parser.add_argument('-w', dest='full_screen', action='store_false', help='window mode')
parser.add_argument('-m', dest='motion', action='store_false', help='don''t init motion detector')
parser.add_argument('-c', dest='camera', action='store_false', help='don''t init camera')
args = parser.parse_args()

GObject.threads_init()

Gtk.init(sys.argv)

controlPanel = GarageControlPanel(args.full_screen, args.motion, args.camera)

Gtk.main()
