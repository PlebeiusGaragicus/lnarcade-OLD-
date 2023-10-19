# INSTALL


1. copy over the `systemd` service

```sh
sudo cp lnarcade.service /etc/systemd/system/lnarcade.service

sudo systemctl daemon-reload
sudo systemctl enable lnarcade.service
sudo systemctl start lnarcade.service

# sanity check on status
sudo systemctl status lnarcade.service

# look at the logs?
sudo journalctl -u lnarcade.service
```

2. install `LightDM`

```sh
sudo apt install -y lightdm # --> Choose LightDM as Default!!

sudo nano /usr/share/xsessions/arcade.desktop
```

```txt
[Desktop Entry]
Name=Arcade Kiosk Mode
Comment=Start Arcade in Kiosk Mode
Exec=/home/satoshi/arcade-game-menu/run
Type=Application
```

```sh
sudo chmod +x /home/satoshi/arcade-game-menu/run

sudo nano /etc/lightdm/lightdm.conf
```

```txt
[Seat:*]
autologin-user=satoshi
autologin-session=arcade
user-session=arcade
```

```sh
sudo reboot
```



---

### FOR FT232H

> from: https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux

```sh
sudo apt-get install libusb-1.0

sudo nano /etc/udev/rules.d/11-ftdi.rules
```

```txt
# /etc/udev/rules.d/11-ftdi.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6011", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6015", GROUP="plugdev", MODE="0666"
```

```sh
pip3 install pyftdi

pip3 install adafruit-blinka

export BLINKA_FT232H=1
```

---

### FOR MCP2221

> from: https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/linux

```sh
sudo apt-get install -y libusb-1.0 libudev-dev
pip3 install hidapi adafruit-blinka --break-system-packages
```


```sh
sudo nano /etc/udev/rules.d/99-mcp2221.rules
```

```txt
SUBSYSTEM=="usb", ATTRS{idVendor}=="04d8", ATTR{idProduct}=="00dd", MODE="0666"
```

```sh
sudo rmmod hid_mcp2221
sudo update-initramfs -u
```

```sh
export BLINKA_MCP2221=1
```
