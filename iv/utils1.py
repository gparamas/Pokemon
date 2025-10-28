import cv2
import numpy as np
from fractions import Fraction
import math
import keyboard
import time
import pytesseract
import json
import pyautogui as pya


def get_both_ss():
    keyboard.wait('space')
    nat_image = np.array(pya.screenshot().convert('RGB'))
    print('penis')
    cv2.imwrite('nat_img.png', nat_image)
    time.sleep(2)
    keyboard.wait('space')
    stat_image = np.array(pya.screenshot().convert('RGB'))
    cv2.imwrite('stat_img.png', stat_image)
    return nat_image, stat_image


def get_both_ss_test():
    return cv2.cvtColor(cv2.imread('iv\\nat_img.png'), cv2.COLOR_BGR2RGB), cv2.cvtColor(cv2.imread('iv\\stat_img.png'), cv2.COLOR_BGR2RGB)

def longest_common_subsequence(s1, s2):
    m = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0 or j == 0:
                m[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                m[i][j] = m[i - 1][j - 1] + 1
            else:
                m[i][j] = max(m[i - 1][j], m[i][j - 1])
    return m[len(s1)][len(s2)]

def ratcliff_obershelp_similarity(s1, s2):
    if not s1 or not s2:
        return 0.0

    lcs_len = longest_common_subsequence(s1, s2)
    
    # This simplified version only considers the LCS length directly.
    # A full implementation would recursively find matches in the remaining parts.
    
    total_chars = len(s1) + len(s2)
    
    if total_chars == 0:
        return 0.0
    
    return (2 * lcs_len) / total_chars

def trim(img):
    coords = cv2.findNonZero(255 - img)
    if coords is None:
       return np.full((120, 150), 255, np.uint8)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = img[y:y+h, x:x+w]
    resized = cv2.resize(cropped, (120, 150), interpolation=cv2.INTER_NEAREST)
    return resized

def get_ss():
    while(True):
        if(keyboard.is_pressed('space')):
            image = np.array(pya.screenshot().convert('RGB'))
            break
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image

def calc_iv_hp(base, curr, lev, ev=0):
    A = curr - lev - 10 
    print(A)
    T_min = math.ceil(Fraction(100*A,lev))
    T_max = math.ceil(Fraction(100*(A+1),lev))
    return T_min - 2 * base - ev//4, T_max - 2 * base - ev//4-1
    
def calc_iv_stat(base, curr, nat, lev, ev=0):
    nat = Fraction.from_float(float(nat)).limit_denominator(1000)
    print(base, curr, nat, lev)
    A_min = math.ceil(Fraction(curr, 1) / nat - 5)
    A_max = math.ceil(Fraction(curr + 1, 1)/nat - 5) - 1
    poss_ivs = []
    print(A_min, A_max)
    for a in range(A_min, A_max + 1):
        T_min = math.ceil(Fraction(100 * a, lev))
        T_max = math.ceil(Fraction(100 * (a + 1), lev)) - 1
        
        IV_max = T_max - 2 * base - ev // 4
        IV_min = T_min - 2 * base - ev // 4
        print(max(0, IV_min), min(31, IV_max) + 1)
        poss_ivs.extend([x for x in range(max(0, IV_min), min(31, IV_max) + 1)])
    if len(poss_ivs) == 0:
        return 0
    return min(poss_ivs), max(poss_ivs)

def get_name(gray_nature_page):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
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

    return name

def get_nature(gray_nature_page):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    gray_nature_page = 255 - gray_nature_page
    gray_nature_page = cv2.threshold(gray_nature_page, 20, 255, cv2.THRESH_BINARY)[1]

    nature = gray_nature_page[770:880, 730:1300]
    nature = cv2.threshold(nature, 150, 255, cv2.THRESH_BINARY)[1]
    nature = 255 - nature

    data = pytesseract.image_to_string(nature, lang='eng', config=r'--psm 6')

    list_natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy', 'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']
    score = []

    for x in list_natures:
        score.append(ratcliff_obershelp_similarity(data.split(' ')[0].lower(), x.lower()))
    poke_nature = list_natures[score.index(max(score))]
    return poke_nature

def get_level(gray_nature_page):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    lvl_img = gray_nature_page[880:960, 420:600]
    lvl_img = cv2.threshold(lvl_img, 200, 255, cv2.THRESH_BINARY)[1]
    lvl_img = 255 - lvl_img

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

    return level

def get_stats(gray_stat_page):
    gray_stat_page = cv2.threshold(gray_stat_page, 0, 255, cv2.THRESH_BINARY)[1]

    left = gray_stat_page[385:685, 1180:1330]
    right = gray_stat_page[385:685, 1600:1750]

    comp = dict()
    for i in range(10):
        temp = cv2.imread(f'data\\{i}.png')
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        comp[i] = trim(cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)[1])

    stats = dict({'hp' : left[0:100, 20::],
              'attack' : left[100:200, 20::],
              'defense' : left[200:300, 20::],
              'special-attack' : right[0:100, 20::],
              'special-defense' : right[100:200, 20::],
              'speed' : right[200:300, 20::]
            })
    
    for x, y in stats.items():
        l = []
        i = 0
        for z in range(3):
            l.append(trim(y[:, i:i+39]))
            i += 39
        stats[x] = l
    
    read_stats = dict({'hp' : [],
              'attack' : [],
              'defense' : [],
              'special-attack' : [],
              'special-defense' : [],
              'speed' : []
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
   
    for n, v in read_stats.items():
        read_stats[n] = 100 * v[0] + 10 * v[1] + v[2]
    
    return read_stats

def get_base_stats(name):
    spec_stats = dict()
    with open('data\\stats.txt', 'r') as f:
        stat_data = json.load(f)
        spec_stats = stat_data[name]
    return spec_stats