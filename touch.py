#!/usr/bin/python3
'''
    Based on Tim Richardson's PiHueRoom
    File name: PiHueRoom.py
    Author: Tim Richardson
    Modified: Jimmy White
    Date created: 04/07/2017
    Date last modified: 12/03/2021
    Python Version: 3.4
	Description:
	Control Philips Hue lights using a APDS9960 gesture sensor - Room version
    Requirements:
    * Raspberry Pi (http://raspberrypi.org/)
    * Philips Hue (http://www2.meethue.com)
    The Raspberry Pi must be on the same network as the Hue bridge
    You must set the bridgeip to be the IP address of your bridge
    and edit the room constant 'roomname'
    
'''
from phue import Bridge
import time
from board import SCL, SDA
import board
import busio
from adafruit_apds9960.apds9960 import APDS9960
import digitalio
i2c = busio.I2C(SCL,SDA)
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True
apds.proximity_interrupt_threshold = (0, 175)
apds.enable_proximity_interrupt = True
int_pin = digitalio.DigitalInOut(board.D5)
# ==============================================================================================
#Setup
# ==============================================================================================
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Stuff you need to change!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#The IP address of the Hue bridge and a list of lights you want to use
bridgeip = '192.168.0.85' # <<<<<<<<<<<
# The 'group' of lights you want to change - i.e. the Room Name in the Hue app
roomname = 'Office'
# <<<<<<<<<<<
# -----------------------------------------------------------------------------------------------
#Do some internal setup
# -----------------------------------------------------------------------------------------------
#Connect to the bridge
b = Bridge(bridgeip)
# IMPORTANT: If running for the first time:
# Uncomment the b.connect() line Press button on bridge Run the code This will save your connection details
# in /home/pi/.python_hue Delete that file if you change bridges
#b.connect()
# <<<<<<<<<< Find the room number from the room name
allrooms = b.get_group()
roomnumber = 0
for room in allrooms.keys():
    if allrooms[room]['name'] == roomname:
        roomnumber = int(room)
        break
if roomnumber == 0:
    print('The room name you have supplied in roomname is not recognised. Please try again. Exiting.')
    exit()
# Hue 'xy' colours - expand at will
redxy = (0.675, 0.322)
greenxy = (0.4091, 0.518)
bluexy = (0.167, 0.04)
yellowxy = (0.4325035269415173,0.5007488105282536)
bluevioletxy = (0.2451169740627056, 0.09787810393609737)
orangexy = (0.6007303214398861,0.3767456073628519)
whitexy = (0.32272672086556803, 0.3290229095590793)
bright=255
# For turning the lights all on to bright white
allwhite = {'on': True, 'bri': 255, 'xy': whitexy}
# Wait time between sending messages to the bridge - to stop congestion
defaultwaittime = 0.41
# = End of Setup ============================================================================
# -------------------------------------------------------------------------------------------
#Functions
# -------------------------------------------------------------------------------------------
#Get the status of the room
def getroomstatus():
    roomstatus = b.get_group(roomnumber)
    return roomstatus
    print(roomstatus)
# Return the status of the room to what it was before the alert Input: Dictionary of the status of the room
# (obtained from getroomstatus()
def putroomstatus(roomstatus):
    global roomnumber
    b.set_group(roomnumber, {'xy': roomstatus['action']['xy'],
                             'bri': roomstatus['action']['bri'],
                             'on': roomstatus['action']['on']}, transitiontime=0)
    time.sleep(defaultwaittime)
def islampon():
    global inalert, roomnumber
    result = False
    roomon = b.get_group(roomnumber)
    result = roomon['state']['any_on']
    return result
# ================================================================
#Main loop - keep going forever
# ================================================================
while True:
    gesture = apds.gesture()
    if gesture == 0x01:
        b.set_group(roomnumber, 'on', True)
        print("on")
    if gesture == 0x02:
        b.set_group(roomnumber, 'on', False)
        print("off")
    if gesture == 0x03:
        if bright >= 10:
               bright -= 20
               b.set_group(roomnumber, 'bri', bright)
               print(bright)
               print("Dimming")
    if gesture == 0x04:
        if bright <= 255:
               bright += 20
               b.set_group(roomnumber, 'bri', bright)
               print (bright)
