import cv2
import pyautogui as pya
import numpy as np
import keyboard
from integrated import get_ss
import pytesseract
import pokebase
from utils1 import ratcliff_obershelp_similarity, get_ss
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = get_ss()
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
thresh = 255 - thresh
thresh = thresh[500:750, 180:550]
cv2.imwrite('testname1.png', thresh)

data = pytesseract.image_to_string(thresh, lang='eng', config=r'--psm 6')
s = []
score = []
with open('data\\names.txt', 'r') as f:
    l = f.read()
    s = l.split(',')
for x in s:
    best = []
    for y in data.split(' '):
        best.append(ratcliff_obershelp_similarity(y.lower(), x.lower()))
    score.append(max(best))

name = s[score.index(max(score))]
print(name)

