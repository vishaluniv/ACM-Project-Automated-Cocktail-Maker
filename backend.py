### when the order is complete: well, we make it, duh. what else did you expect?

import RPi.GPIO as GPIO
import time
import smbus
from gpiozero import PWMLED, DistanceSensor

GPIO.setmode(GPIO.BCM)

TRIGG_1=19
ECHO_1=23

TRIGG_2=8
ECHO_2=7

TRIGG_3=9
ECHO_3=14

TRIGG_4=23
ECHO_4=15

CUP_PRESENT=0.09
SLAVE_ADDRESS=0x8

BASEDRINK_TIME = 7
MIXER_TIME = 12

UNIT_DELAY  = 3

UNIT_MOVEMENT = 0



MOTOR_1_FORWARD = 24

MOTOR_1_BACKWARD = 12


GPIO.setup(MOTOR_1_BACKWARD,GPIO.OUT)
GPIO.setup(MOTOR_1_FORWARD,GPIO.OUT)


GPIO.setup(TRIGG_1,GPIO.OUT)
GPIO.setup(TRIGG_2,GPIO.OUT)
GPIO.setup(TRIGG_3,GPIO.OUT)
GPIO.setup(TRIGG_4,GPIO.OUT)

GPIO.setup(ECHO_1,GPIO.IN)
GPIO.setup(ECHO_2,GPIO.IN)
GPIO.setup(ECHO_3,GPIO.IN)
GPIO.setup(ECHO_4,GPIO.IN)



def ConvertForI2C(d):
    converted=[]
    for b in d:
        converted.append(ord(b))
    return converted

bus = smbus.SMBus(1)

def order(order):
    time.sleep(1)
    move_to(find_cup(), 1)
    make_drink(order)


def move_ahead():
    rotate=0
    while(rotate<31):
        rotate = rotate+1
        GPIO.output(MOTOR_1_FORWARD, True)
        time.sleep(0.01)
        GPIO.output(MOTOR_1_FORWARD, False)
        time.sleep(0.01)

def move_back():
    rotate=0
    while(rotate<31):
        rotate = rotate+1
        GPIO.output(MOTOR_1_BACKWARD, True)
        time.sleep(0.01)
        GPIO.output(MOTOR_1_BACKWARD, False)
        time.sleep(0.01)


def find_cup():
    if(cup_is_present(1) == True):
        return 1
    elif(cup_is_present(2) == True):
        return 2
    elif(cup_is_present(3) == True):
        return 3
    elif(cup_is_present(4) == True):
        return 4
    else:
        return 0

def cup_is_present(i):
    if(i==1):
        if(ultrasonic(TRIGG_1,ECHO_1) < CUP_PRESENT):
            return True
        else:
            return False
    elif(i==2):
        if(ultrasonic(TRIGG_2,ECHO_2) < CUP_PRESENT):
            return True
        else:
            return False
    elif(i==3):
        if(ultrasonic(TRIGG_3,ECHO_3) < CUP_PRESENT):
            return True
        else:
            return False
    elif(i==4):
        if(ultrasonic(TRIGG_4,ECHO_4) < CUP_PRESENT):
            return True
        else:
            return False

def initial():
    if(cup_is_present(1) == True):
        return True
    else:
        return False

def move_to(i,f):
    time.sleep(0.2)
    move=0
    while(move<abs(f-i)):
        move=move+1
        if(f>i):
            move_ahead()
        else:
            move_back()
    

    
def send_to_Arduino(send):
    if(send==1):
        bus.write_byte(SLAVE_ADDRESS,0x0)
    elif(send==2):
        bus.write_byte(SLAVE_ADDRESS,0x1)
    elif(send==4):
        bus.write_byte(SLAVE_ADDRESS,0X2)
    elif(send==5):
        bus.write_byte(SLAVE_ADDRESS,0x3)
  

def ultrasonic(trig,echo):
    ultrasonic = DistanceSensor(
    echo=13, trigger=19, max_distance=0.35, threshold_distance=0.05)

    distance = ultrasonic.value * 0.35
    print(f"Distance => {distance: 1.2f} m")


def make_drink(ord):
    initial = 1
    time.sleep(1)

    move_to(initial, ord[0])

    time.sleep(UNIT_DELAY*abs(initial-ord[0]))

    send_to_Arduino(ord[0])
    time.sleep(BASEDRINK_TIME)
    send_to_Arduino(ord[0])
    initial=ord[0]
    time.sleep(2)

    move_to(initial, ord[1])

    time.sleep(UNIT_DELAY*abs(initial-ord[1]))

    send_to_Arduino(ord[1])
    time.sleep(MIXER_TIME)
    send_to_Arduino(ord[1])
    
    time.sleep(2)

    move_to(ord[1], 5)

    
       



