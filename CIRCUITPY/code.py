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
button.pull = Pull.DOWN

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
# TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
# JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"
# JSON_STARS_URL = "https://api.github.com/repos/adafruit/circuitpython"

# print("ESP32-S2 WebClient Test")

# print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

# print("Available WiFi networks:")
# for network in wifi.radio.start_scanning_networks():
#     print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#                                              network.rssi, network.channel))
# wifi.radio.stop_scanning_networks()

# print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
# wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
# print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
# print(f"My IP address: {wifi.radio.ipv4_address}")

# ping_ip = ipaddress.IPv4Address("8.8.8.8")
# ping = wifi.radio.ping(ip=ping_ip)

# # retry once if timed out
# if ping is None:
#     ping = wifi.radio.ping(ip=ping_ip)

# if ping is None:
#     print("Couldn't ping 'google.com' successfully")
# else:
#     # convert s to ms
#     print(f"Pinging 'google.com' took: {ping * 1000} ms")

# pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl.create_default_context())

# response = requests.get("https://youtube-converter.replit.app/Ym8JURyCNXk", stream=True)

# with open("/sd/cashmoneybuckets.wav", "wb") as f:
#     # print(f"Fetching data from https://www.dubov.ski/s/siren.wav")
#     # response = requests.get("https://www.dubov.ski/s/siren.wav")
#     print("-" * 40)
#     if response.status_code == 200:
#         # print(response.iter_content)
#         i = 0
#         for chunk in response.iter_content(chunk_size=512):
#             if chunk:
#                 if(i%100 == 0):
#                     print(f"Writing chunk {i}")
#                 i+=1 
#                 f.write(bytes(chunk))
#                 del chunk 
            
#         print(response.headers)
#         print("written successfully")
#     else:
#         print("Failed.")
#     # print(response.text)
#     # f.write(bytes(response.content))
#     print("-" * 40)

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

old_switch = switch.value
old_button = button.value

old_channel = 0

def get_channel(switch):
    global old_channel
    if (switch.value >= 0 and switch.value <= 9000):
        old_channel = 0
    if (switch.value >= 11000 and switch.value <= 19000):
        old_channel = 1
    if (switch.value >= 21000 and switch.value <= 29000):
        old_channel = 2
    if (switch.value >= 31000 and switch.value <= 41000):
        old_channel = 3
    if (switch.value >= 41000 and switch.value <= 49000):
        old_channel = 4
    return old_channel

        
    

# while True:
#     print(button.value)
#     time.sleep(0.1)

pause = True
breakbreak = False
while True:
    # Assuming that the ESP32 reads analog numbers from 0 to 4096
   
    print(button.value)
    print(switch.value)
    old_switch = get_channel(switch)
    old_button = button.value

    path = f"/sd/{old_switch}.wav"

    print(path)
    
    music = audiocore.WaveFile(open(path, "rb"))
    mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1,
                            bits_per_sample=16, samples_signed=True)
    mixer = audiomixer.Mixer(voice_count=1, sample_rate=16000, channel_count=1, bits_per_sample=16, samples_signed=True)  
    mixer.voice[0].level = 0.5 # setting the volume, can be adjusted manually through the potentiometer.
    # audio.play(mixer)
    # if button.value: 
    #     playing != playing
    # Have AudioOut play our Mixer source
    audio.play(mixer)
        # Play the first sample voice
    mixer.voice[0].play(music)
    playing = True
    paused = False
    while mixer.playing: 
        if ((old_button != button.value) and button.value): # if the button value changes and the button is pressed 
            print("Pausing")
            paused = True
            print(paused)
            old_button = button.value
            while paused:
                
                print("Paused, old_button is: ", old_button)
                audio.stop()
                print(button.value)
                if ((old_button != button.value) and button.value): # if the button value changes and the button is pressed
                    print("unpausing")
                    paused = False
                    audio.play(mixer)
                    # break
                old_button = button.value
                time.sleep(0.1)



            # paused = not paused
            break
    
    #    
        old_button = button.value
        if(old_switch != get_channel(switch)):
            print(get_channel(switch))
            
            old_switch = get_channel(switch)
            time.sleep(0.25)
            
            audio.stop()
            break
        time.sleep(0.1)
        print("playing")

    # print("Done")

