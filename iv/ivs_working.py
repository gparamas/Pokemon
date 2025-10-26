import cv2
import pyautogui as pya
import numpy as np
import keyboard

image = []
while(True):
    if(keyboard.is_pressed('space')):
        image = np.array(pya.screenshot().convert('RGB'))
        break
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

def trim(img):
    coords = cv2.findNonZero(255 - img)
    if coords is None:
       return np.full((120, 150), 255, np.uint8)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = img[y:y+h, x:x+w]
    resized = cv2.resize(cropped, (120, 150), interpolation=cv2.INTER_NEAREST)

    return resized

left = thresh[385:685, 1180:1330]
right = thresh[385:685, 1600:1750]

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

comp = dict()
for i in range(10):
    temp = cv2.imread(f'data\\{i}.png')
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    comp[i] = trim(cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)[1])

read_stats = dict({'hp' : [],
              'atk' : [],
              'def' : [],
              'spatk' : [],
              'spdef' : [],
              'spd' : []
            })

mini = [10000010, 10000010, 10000010, 11000000, 11000010, 10000010, 10000010, 11000000, 10000010, 10000010]
listofnames = ['spatk1', 'spatk2', 'spatk3', 'spd10', 'spd20', 'spd30']
print([np.sum(i == 0) for i in comp.values()])
for x in comp.values():
    print(x.shape)
print()
indx = 0
for name, stat in stats.items():
    for i, num in enumerate(stat):
        #num_blacks = np.sum(num == 0)
        if(name == 'spatk' or name == 'spd'):
            cv2.imwrite(f'{listofnames[indx]}.png', num)
            print(listofnames[indx], end='')
            print(num.shape)
            indx +=1 
        for key, digit in comp.items():
            #mini[int(key)] = abs(np.sum(digit == 0)  - num_blacks)
            if(num.shape[1] == digit.shape[1]):
                if(np.sum(cv2.bitwise_not(num)) == 0):
                    mini[0] = 0
                    continue 
                mini[int(key)] = np.sum(cv2.bitwise_xor(num, digit))
        read_stats[name].append(mini.index(min(mini)))
        mini = [10000010, 10000010, 10000010, 10000010, 10000110, 10000010, 10000010, 11000010, 10000010, 10000010]
print(read_stats)


cv2.waitKey(10000) 
cv2.destroyAllWindows()
