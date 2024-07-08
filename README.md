# CircuitPython ESP32-S3 WiFi I2S Music Player

## Overview
This project connects to a WiFi network, downloads an .wav from a URL, and plays the .wav on a speaker with the [ESP32 Xiao S3 from SEEED Studio](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/).

[![This is a demo video of the first prototype.](https://github.com/AugmentHub/esp32-s3-wifi-i2s-musicplayer/blob/b09ceb14060484af4d2f5885600bc56aaff7a363/demo_video.mp3)]

## Steps

0. The contents of the CIRCUITPY folder in this repo can be placed on an ESP32-S3.

1. The WiFi login credentials are set in a /CIRCUITPY/settings.toml file (you need to provide it, not included in this repo). Details ![here](https://learn.adafruit.com/adafruit-esp32-s3-feather/circuitpython-internet-test).

2. We used pins board.IO1, board.IO2, and board.IO3 to connect to a ![MAX98357 I2S amp](https://www.adafruit.com/product/3006) on the pins BLCK, LRC, and DIN respectively. These are set in /CIRCUITPY/code.py

3. The URL is currently set in code.py as https://www.dubov.ski/s/siren.wav for testing purposes. However, we deployed a webserver that takes in a YouTube URL and lets you download it from the chip, write it to the SD card, and play it on the speaker as you wish.

This is how our bare circuit looks like: 
<img src="https://github.com/AugmentHub/esp32-s3-wifi-i2s-musicplayer/blob/45a6a3e149530b5d1a607535d0f565dcdc180c81/IMG_1052.jpg" alt="Electronics">
