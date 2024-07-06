# CircuitPython ESP32-S3 WiFi I2S Music Player

This project connects to a WiFi network, downloads an .wav from a URL, and plays the .wav on a speaker.

0. The contents of the CIRCUITPY folder in this repo can be placed on an ESP32-S3.

1. The WiFi login credentials are set in a /CIRCUITPY/settings.toml file (you need to provide it, not included in this repo). Details ![here](https://learn.adafruit.com/adafruit-esp32-s3-feather/circuitpython-internet-test).

2. We used pins board.IO1, board.IO2, and board.IO3 to connect to a ![MAX98357 I2S amp](https://www.adafruit.com/product/3006) on the pins BLCK, LRC, and DIN respectively. These are set in /CIRCUITPY/code.py

3. The URL is currently set in code.py as https://www.dubov.ski/s/siren.wav.
