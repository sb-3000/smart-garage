# Smart Garage Control Panel

This is GTK based GUI application to control garage doors, optimized for Raspberry Pi 7" Touch Screen Display

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
chown -R pi:pi /var/garage/
cd /var/garage/
```
### Dependencies required for development:

1. Install PyGObject, GTK and their dependencies: 
  (https://pygobject.readthedocs.io/en/latest/getting_started.html)

2. Install fake-rpi:
```
  pip install fake-rpi
```

You may run program with -w -m arguments, it will run app in windowed mode instead of full screen and disable motion detector:
```
python garage-control-panel.py -w -m
```

## License

This project is licensed under the MIT License
