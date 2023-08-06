# Bugs

## Issue #3: Missing return packages using Raspberry Pi's GPIO (issue #3)

https://github.com/jeremiedecock/pyax12/issues/3

### Warning message

    RuntimeWarning: This channel is already in use, continuing anyway.

### Raspberry Pi Coockbook (Siomon Monk), recipe 8.7 "Freeing the serial port"

"By default, the serial port acts as a console, through which you can Raspberry Pi with sudo reboot.
To disable this so that you can use the serial port to connect to peripherals such as GPS ( Recipe 11.10 ), comment out a line in /etc/inittab:

    $ sudo nano /etc/inittab

Scroll down to the end of the file to find the line:

    T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

Comment it out by placing a # in front of it:

    #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

Save the file with Ctrl-X followed by Y. For the changes to take effect, you need to reboot your Raspberry Pi with sudo reboot."

### UART issues with Raspberry Pi 3

See http://www.framboise314.fr/le-port-serie-du-raspberry-pi-3-pas-simple/ (in French).


## Issue #4: Cannot put AX-12A into wheel mode

I checked the *wheel mode*, it works.
The `Angle Limit Error` is raised if you set the speed with `pyax12.connection.goto()` because it also set the position (which is forbidden because of the cw and the ccw angle limit).
I added a function to easily set the speed  : `pyax12.connection.set_speed()`.

Here is an example (you can also check [examples/endless_turn.py](https://github.com/jeremiedecock/pyax12/blob/master/examples/endless_turn.py) ):

```
from pyax12.connection import Connection
import pyax12.packet as pk
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyAMA0", baudrate=57600, rpi_gpio=True)

dynamixel_id = 1

# Set the "wheel mode"
serial_connection.set_cw_angle_limit(dynamixel_id, 0, degrees=False)
serial_connection.set_ccw_angle_limit(dynamixel_id, 0, degrees=False)

# Activate the actuator (speed=512)
serial_connection.set_speed(dynamixel_id, 512)

# Leave the actuator turn 5 seconds
time.sleep(5)

# Stop the actuator (speed=0)
serial_connection.set_speed(dynamixel_id, 0)

# Leave the "wheel mode"
serial_connection.set_ccw_angle_limit(dynamixel_id, 1023, degrees=False)

# Go to the initial position (0 degree)
serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)

# Close the serial connection
serial_connection.close()
```
