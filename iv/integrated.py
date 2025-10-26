import cv2
import pyautogui as pya
import numpy as np
import keyboard
import pytesseract
from utils1 import *
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_both_ss():
    keyboard.wait('space')
    nat_image = np.array(pya.screenshot().convert('RGB'))
    keyboard.wait('space')
    stat_image = np.array(pya.screenshot().convert('RGB'))
    return nat_image, stat_image

def main():
    nature_page, stat_page = get_both_ss()

    gray_nature_page = cv2.cvtColor(nature_page, cv2.COLOR_RGB2GRAY)
    lvl_img = gray_nature_page[880:960, 420:600]
    lvl_img = cv2.threshold(lvl_img, 200, 255, cv2.THRESH_BINARY)[1]
    lvl_img = 255 - lvl_img


    #gray_nature_page = cv2.threshold(gray_nature_page, 20, 255, cv2.THRESH_BINARY)[1]
    name_img = cv2.threshold(gray_nature_page, 200, 255, cv2.THRESH_BINARY)[1]
    name_img = 255 - name_img
    name_img = name_img[500:750, 180:550]

    name_str = pytesseract.image_to_string(name_img, lang='eng', config=r'--psm 6')
    s = []
    score = []
    with open('data\\names.txt', 'r') as f:
        l = f.read()
        s = l.split(',')
    for x in s:
        best = []
        for y in name_str.split(' '):
            best.append(ratcliff_obershelp_similarity(y.lower(), x.lower()))
        score.append(max(best))

    name = s[score.index(max(score))]

    gray_nature_page = 255 - gray_nature_page
    gray_nature_page = cv2.threshold(gray_nature_page, 20, 255, cv2.THRESH_BINARY)[1]

    nature = gray_nature_page[770:880, 730:1300]
    nature = cv2.threshold(nature, 150, 255, cv2.THRESH_BINARY)[1]
    nature = 255 - nature

    
    comp = dict()
    for i in range(10):
        temp = cv2.imread(f'data\\{i}.png')
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        comp[i] = trim(cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)[1])

    
    digits_lvl = []
    i = 0
    for z in range(3):
        digits_lvl.append(trim(lvl_img[:, i:i+46]))
        i += 48  

    mini = [10000010, 10000010, 10000010, 11000000, 11000010, 10000010, 10000010, 11000000, 10000010, 10000010]
    num_lvl = []
    for x in digits_lvl:
        for key, digit in comp.items():
            if(np.sum(cv2.bitwise_not(x)) == 0):
                mini[0] = 0 
                continue 
            mini[int(key)] = np.sum(cv2.bitwise_xor(x, digit))
        num_lvl.append(mini.index(min(mini)))
    level = int(''.join([str(x) for x in num_lvl]))
    level = (int(level / 100) if level % 100 == 0 else int(level / 10)) if  level > 100 else level

    data = pytesseract.image_to_string(nature, lang='eng', config=r'--psm 6')
    
    list_natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy', 'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']
    poke_nature = ''
    score = []

    for x in list_natures:
        score.append(ratcliff_obershelp_similarity(data.split(' ')[0].lower(), x.lower()))

    poke_nature = list_natures[score.index(max(score))]

    gray_stat_page = cv2.cvtColor(stat_page, cv2.COLOR_RGB2GRAY)
    gray_stat_page = cv2.threshold(gray_stat_page, 0, 255, cv2.THRESH_BINARY)[1]

    left = gray_stat_page[385:685, 1180:1330]
    right = gray_stat_page[385:685, 1600:1750]

    stats = dict({'hp' : left[0:100, 20::],
              'atk' : left[100:200, 20::],
              'def' : left[200:300, 20::],
              'spatk' : right[0:100, 20::],
              'spdef' : right[100:200, 20::],
              'spd' : right[200:300, 20::]
            })
    
    for x, y in stats.items():
        l = []
        i = 0
        for z in range(3):
            l.append(trim(y[:, i:i+39]))
            i += 39
        stats[x] = l
    
    
    read_stats = dict({'hp' : [],
              'atk' : [],
              'def' : [],
              'spatk' : [],
              'spdef' : [],
              'spd' : []
            })

    mini = [10000010, 10000010, 10000010, 11000000, 11000010, 10000010, 10000010, 11000000, 10000010, 10000010]
   
    for stat_name, stat in stats.items():
        for i, num in enumerate(stat):
            for key, digit in comp.items():
                if(np.sum(cv2.bitwise_not(num)) == 0):
                    mini[0] = 0
                    continue 
                mini[int(key)] = np.sum(cv2.bitwise_xor(num, digit))
            read_stats[stat_name].append(mini.index(min(mini)))
            mini = [10000010, 10000010, 10000010, 10000010, 10000110, 10000010, 10000010, 11000010, 10000010, 10000010]
    print(name, poke_nature, level, read_stats)

if __name__ == '__main__':
    main()