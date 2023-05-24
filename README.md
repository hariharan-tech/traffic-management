# traffic-management
A smart traffic management system which will be deployed on a Raspberry Pi 4. Image processing is done at the server side and sends alerts on Telegram.

# Dependencies

- ## pi74HC595 Module
  - Used to interface 74HC595 serial-in parallel-out shift register with the raspberry pi 4.
    #### References
    - [https://pypi.org/project/pi74HC595/](https://pypi.org/project/pi74HC595/)
    - [https://www.ti.com/lit/ds/symlink/sn74hc595.pdf](https://www.ti.com/lit/ds/symlink/sn74hc595.pdf)
- ## Accessing Camera
  - Use ```raspistill``` for accessing and using Raspberry Pi camera.
  - Using the ```raspistill``` (for images) and ```raspivid``` (for videos) **[OUTDATED]**.
    #### References
      - [https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started](https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started)
