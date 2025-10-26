
import cv2
import numpy as np
import keyboard
import pyautogui as pya

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
    return image