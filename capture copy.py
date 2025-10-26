import cv2
import pyautogui as pya
import numpy as np
import keyboard
from integrated import get_ss
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def trim(img):
    coords = cv2.findNonZero(255 - img)
    if coords is None:
       return np.full((150, 120), 255, np.uint8)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = img[y:y+h, x:x+w]
    resized = cv2.resize(cropped, (120, 150), interpolation=cv2.INTER_NEAREST)

    return resized
image = get_ss()

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cropped = gray[880:960, 420:600]
thresh = cv2.threshold(cropped, 200, 255, cv2.THRESH_BINARY)[1]
thresh = 255 - thresh

digits = []
i = 0
inc = 0
for z in range(3):
    digits.append(trim(thresh[:, i:i+46]))
    cv2.imwrite(f'{z}.png', trim(thresh[:, i:i+46]))
    i += 48  


mini = [10000010, 10000010, 10000010, 11000000, 11000010, 10000010, 10000010, 11000000, 10000010, 10000010]
comp = dict()

for i in range(10):
    temp = cv2.imread(f'images\\{i}.png')
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    comp[i] = trim(cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)[1])

num = []
for x in digits:
    for key, digit in comp.items():
        if(np.sum(cv2.bitwise_not(x)) == 0):
            mini[0] = 0 
            continue 
        mini[int(key)] = np.sum(cv2.bitwise_xor(x, digit))
    print(x.shape, digit.shape)
    num.append(mini.index(min(mini)))
level = int(''.join([str(x) for x in num]))
level = (int(num / 100) if num % 100 == 0 else int(num / 10)) if  num > 100 else num
print(num)
cv2.imwrite('test1.png', thresh)

cv2.waitKey()

