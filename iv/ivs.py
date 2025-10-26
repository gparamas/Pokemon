import cv2
import pyautogui as pya
import numpy as np
import keyboard
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def fill_hollow_digits(img):
    """
    Takes a cropped image of hollow (outlined) digits and returns
    a preprocessed version suitable for Tesseract OCR.
    Output: black digits on white background
    """
    gray = img.copy()
    filled = gray.copy()
    h, w = gray.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(filled, mask, (0,0), 255)
    gray_filled = gray & filled

    gray_filled = cv2.resize(gray_filled, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST)

    return gray_filled

#once you find a corner, keep track of how far the walls are - if they're below a threshold fill the corner completely.
#otherwise fill it to some threshold amount and move on
def smooth_edges(img):
    done = False
    img2 = img.copy()
    while not done:
        size = 0
        changed = 0
        for i in range(img.shape[0]-2, 1, -1):
            for j in range(img.shape[1]-1):
                if(img[i][j] == 255):
                    if(img[i+1][j] == 0 and img[i][j+1] == 0 and img[i-1][j+1] == 0):
                        img2[i][j] = 0
                        changed += 1
                        size += 1
                    else:
                        img2[i][j] = 255
        if changed == 0 or size >= 20:
            done = True
        img = img2.copy()
    return img2

# Load image, grayscale, Otsu's threshold, then invert
#image = pya.screenshot().convert('RGB')
#image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
thresh = cv2.imread('s.png')
thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# Perfrom OCR with Pytesseract
left = thresh[385:700, 1180:1330]
right = thresh[385:700, 1600:1750]

stats = dict({'hp' : left[0:100, 20::],
              'atk' : left[100:200, :],
              'def' : left[200:315, :],
              'spatk' : right[0:100, :],
              'spdef' : right[100:200, :],
              'spd' : right[200:315, :]
            })

stats = dict({'hp' : left[0:100, 20::]})

for idx, (x, y) in enumerate(stats.items()):
    l = []
    i = 0
    for z in range(3):
        l.append(y[:, i:i+42])
        i += 42
    stats[x] = l

for x, y in stats.items():
    l = []
    for temp in y:
        #temp2 = temp.copy()
        #temp = smooth_edges(temp)
        #print(np.array_equal(temp, temp2))
        temp = fill_hollow_digits(temp)
        l.append(temp)
    stats[x] = l

for i, (x, y) in enumerate(stats.items()):
    print(len(y))
    for i2, d in enumerate(y):
        data= pytesseract.image_to_string(d, lang='eng', config=r'--psm 10 digits')
        print(':' + data, end='')
        cv2.imshow(str(10+i+i2), d)
        print(d.shape)
    print('penis')

for i, x in enumerate([left, right]):
    data = pytesseract.image_to_string(x, lang='eng', config=r'--psm 6 outputbase digits')
    cv2.imshow(str(i),x)
    print(f'\'{data}\'')

#for x, y in stats.items():
 #   cv2.imshow(x, y)

cv2.waitKey() 

