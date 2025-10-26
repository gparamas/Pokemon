from enum import Enum
import pyautogui as pya
import numpy as np
import cv2
import time
import re
import keyboard
import win32gui


old_man = 'Screenshot 2025-10-14 003659.png'
poke_center = ''
hatch = ''

class State(Enum):
    ACCEPTING = 0
    RUNNING = 1
    HATCHING = 2
    STORING = 3

def find_subimg(img):
#Find template image in large image
    threshold = 0.8
    img = cv2.imread(img)
    screen = pya.screenshot().convert('RGB')
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    img = img.astype(np.uint8)
    screen = screen.astype(np.uint8)
    res = cv2.matchTemplate(screen, img, cv2.TM_CCOEFF_NORMED)
    print(img.shape)
    loc = np.where(res >= threshold)
    if len(loc[1]) > 0:
        avg = 0
        for x in loc[1]:
            avg += x
        avg /= len(loc[1])
        dir = ''
        if (screen.shape[1]/2 - avg > 75):
            dir = 'right'
        elif (screen.shape[1]/2 - avg - 50 < -75):
            dir = 'left'
        else:
            dir = 'center'
        print(avg, screen.shape[1]/2)
        print(dir)
        dist = abs(screen.shape[1]/2 - avg) / 122
        return True, dir, dist
    return False, '', 0

def accept_left():
# accept an egg if inventory is not full
        yes = False
        while(not yes):
            yes, dir = find_subimg(old_man)
        if(yes): 
            time.sleep(5)
            print('penis')
            i = 0
            dire = ['left', 'right']
            if(dir != 'center'):
                pya.keyDown(key='right')
            while(dir != 'center'):
                yes, dir = find_subimg(old_man)
            a = time.time()
            pya.keyUp(key='right')
            pya.keyDown(key='up')
            print(time.time() - a)
            time.sleep(2)
            pya.keyUp(key='up')
            for y in range(2):
                pya.keyDown('x')
                time.sleep(.2)
                pya.keyUp('x')
                time.sleep(.5)
            pya.press(keys='down')
def accept_right():
    pass
def run():
# start running
    pass

def hatch(): 
    pass 

def store_left():
    pass

def store_right():
    pass
#accept_left()
def test():
    while(True):
        if(keyboard.is_pressed('space')):
            a = time.time()
            pya.keyDown('left')
            time.sleep(.2)
            pya.keyUp('left')
            print(time.time() - a)
            break
test()