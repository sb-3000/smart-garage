# Smart Garage Control Panel

This is GTK based GUI application to control garage doors, optimized for Raspberry Pi 7" Touch Screen Display
My motivation to use GTK over web based dashboard was... ip web camera. Raspberry has enough juce to decode H.264/MPEG-4, but RTSP streaming is not supported by browsers, 
plugins like VLC are banned, so after messing with workarounds for a little while I decided to try write a 'native' application

Before publishing project on github I removed part of functionality for Chamberlain MyQ, camera and etc. because of migration to python 3, but I'll port it and publish there. 

### Deploy Smart Garage on Raspberian:
 
1. Login into your RPi

2. Install GTK and dependencies, I assume python is installed by default
```
  sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

3. Install xset, a lightweight application that control X settings, like power managment
```
  apt-get install x11-xserver-utils
```

3. Install application 
```
sudo mkdir -p /var/garage/control-panel/
sudo chown -R pi:pi /var/garage/
wget -O - https://github.com/sb-3000/smart-garage/tarball/master | tar xz --directory /var/garage/control-panel/ --strip 1
```
4. Add smart-garage to autostart
(I assume there you are running Raspbian on your Raspberry Pi, but if you are using other OS, steps will be not much different)

In your home folder create fine named garage.sh, and make it executable:

```
#!/bin/bash
sleep 2
cd /var/garage/control-panel && python3 garage-control-panel.py >garage.out 2>&1
```

add following line at the end of ~/.config/lxsession/LXDE-pi/autostart
```
@/home/pi/garage.sh
```

Enjoy!

### Dependencies required for development:

1. Install PyGObject, GTK and their dependencies: 
  https://pygobject.readthedocs.io/en/latest/getting_started.html

2. Install fake-rpi:
```
  pip install fake-rpi
```

During development you may run program with -w -m arguments, it will run app in windowed mode instead of full screen and disable motion detector:
```
python garage-control-panel.py -w -m
```

## License

This project is licensed under the MIT License
