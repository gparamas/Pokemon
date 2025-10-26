import cv2
import pyautogui as pya
import numpy as np
import keyboard
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = []
while(True):
    if(keyboard.is_pressed('space')):
        image = np.array(pya.screenshot().convert('RGB'))
        break
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
gray = 255 - gray
thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)[1]

nature = gray[770:980, 730:1300]
nature = cv2.threshold(nature, 20, 255, cv2.THRESH_BINARY)[1]
nature = 255 - nature
cv2.imwrite('test2.png', nature)
data= pytesseract.image_to_string(nature, lang='eng', config=r'--psm 6')
list_natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy', 'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']
poke_nature = ''
for x in list_natures:
    if x.lower() in data.lower():
        poke_nature = x.capitalize()
        break
print(data)
level = re.search(r'[0-9]+', re.escape(data)).group()
print(poke_nature, level)

