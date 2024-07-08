# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import busio
import sdcardio
import storage
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull 

import audiocore
import board
import audiobusio
import audiomixer
import time

#STARTUP TONE
# audio = audiobusio.I2SOut(board.IO1, board.IO2, board.IO3)
# music = audiocore.WaveFile(open("/startup.wav", "rb"))
# mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1,
#                          bits_per_sample=16, samples_signed=True)
# mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1, bits_per_sample=16, samples_signed=True)  
# mixer.voice[0].level = 1

# print("playing")
# # Have AudioOut play our Mixer source
# audio.play(mixer)
# # Play the first sample voice
# mixer.voice[0].play(music)
# while mixer.playing:
#   time.sleep(1)

# Defining button & Pot pin
BUTTON_PIN = board.IO4
SWITCH_PIN = board.IO5

# Setting up the switch for switching between songs.
switch= AnalogIn(SWITCH_PIN) 

# Setting up the button to start and stop a song.
button = DigitalInOut(BUTTON_PIN)
button.direction = Direction.INPUT
button.pullup = Pull.UP

# Use the board's primary SPI bus
# spi = board.IO
# Or, use an SPI bus on specific pins:
spi = busio.SPI(board.IO7, MOSI=board.IO9, MISO=board.IO8)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.IO21
# Boards with built in SPI SD card slots will generally have a
# pin called SD_CS:
#cs = board.SD_CS

sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# URLs to fetch from
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"
JSON_STARS_URL = "https://api.github.com/repos/adafruit/circuitpython"

print("ESP32-S2 WebClient Test")

print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                             network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

ping_ip = ipaddress.IPv4Address("8.8.8.8")
ping = wifi.radio.ping(ip=ping_ip)

# retry once if timed out
if ping is None:
    ping = wifi.radio.ping(ip=ping_ip)

if ping is None:
    print("Couldn't ping 'google.com' successfully")
else:
    # convert s to ms
    print(f"Pinging 'google.com' took: {ping * 1000} ms")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

response = requests.get("https://youtube-converter.replit.app/Ym8JURyCNXk", stream=True)

with open("/sd/cashmoneybuckets.wav", "wb") as f:
    # print(f"Fetching data from https://www.dubov.ski/s/siren.wav")
    # response = requests.get("https://www.dubov.ski/s/siren.wav")
    print("-" * 40)
    if response.status_code == 200:
        # print(response.iter_content)
        i = 0
        for chunk in response.iter_content(chunk_size=64):
            if chunk:
                if(i%100 == 0):
                    print(f"Writing chunk {i}")
                i+=1 
                f.write(bytes(chunk))
                del chunk 
            
        print(response.headers)
        print("written successfully")
    else:
        print("Failed.")
    # print(response.text)
    # f.write(bytes(response.content))
    print("-" * 40)

# print(f"Fetching json from {JSON_QUOTES_URL}")
# response = requests.get(JSON_QUOTES_URL)
# print("-" * 40)
# print(response.json())
# print("-" * 40)

# print()

# print(f"Fetching and parsing json from {JSON_STARS_URL}")
# response = requests.get(JSON_STARS_URL)
# print("-" * 40)
# print(f"CircuitPython GitHub Stars: {response.json()['stargazers_count']}")
# print("-" * 40)


audio = audiobusio.I2SOut(board.IO1, board.IO2, board.IO3)

song = 0 # defaulting to the first song.

playing = True
# Creating the loop

while True:
    # Assuming that the ESP32 reads analog numbers from 0 to 4096
    if switch.value % 4:
        song = switch.value / 1024 # Continuously reading in the values
    else: 
        song = switch.value % 4 if os.path.exists(f"/sd/{song}.wav") else 0 # Checking that the path exists, otherwise defaulting to 0
    
    path = f"/sd/{song}.wav"
    
    music = audiocore.WaveFile(open(path, "rb"))
    mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1,
                            bits_per_sample=16, samples_signed=True)
    mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1, bits_per_sample=16, samples_signed=True)  
    mixer.voice[0].level = 1 # setting the volume, can be adjusted manually through the potentiometer.
    # audio.play(mixer)
    if button.value: 
        playing != playing
    # Have AudioOut play our Mixer source
    if playing: 
        audio.play(mixer)
            # Play the first sample voice
        mixer.voice[0].play(music)
        while mixer.playing:
            time.sleep(1)
            print("stopped")
    else:
        print("playing")
        audio.stop()
        mixer.voice[0].stop(music)

    print("Done")