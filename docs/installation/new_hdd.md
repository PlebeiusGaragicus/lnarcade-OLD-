# installation for development

```sh
sudo apt-get install -y rsync git
```

---

# install FT232H

https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/setup

```sh
sudo apt-get install -y libusb-1.0

sudo nano /etc/udev/rules.d/11-ftdi.rules
```

```txt
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6011", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", GROUP="plugdev", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6015", GROUP="plugdev", MODE="0666"
```

# unplug, replug device

```sh
pip3 install pyftdi adafruit-blinka
```

# NOTE: ensure you run:

...after every reboot!

```sh
export BLINKA_FT232H=1
```

# post-install checks

```sh
python3
```

```python
from pyftdi.ftdi import Ftdi
Ftdi().open_from_url('ftdi:///?')

# and...

import board
# no errors? :)
```

```python
import board
import digitalio
led = digitalio.DigitalInOut(board.C0)
led.direction = digitalio.Direction.OUTPUT
led.value = True
# then...
led.value = False
```
