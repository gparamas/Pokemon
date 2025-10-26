from utils1 import *

def main():
    num_eggs = 0
    num_poke = 0
    state = State.RUNNING
    old_man = r'Screenshot 2025-10-14 003659.png'
    hatching = ''
    poke_center = ''

    while True:
        if(state == State.RUNNING):
            if(num_poke == 4):
                storing = find_subimg(poke_center)
                if(storing[0]):
                    state = State.STORING
            hatching = find_subimg(hatching)
            if(hatching[0]):
                state = state.HATCHING
            if(num_eggs < 4):
                accepting = find_subimg(old_man)
                if(accepting[0]):
                    state = State.ACCEPTING
        elif(state == State.ACCEPTING):
            accepting = find_subimg(old_man)
            if(accepting[1] == 'left'):
                accept_left()
            elif(accepting[1] == 'right'):
                accept_right()
            num_eggs += 1
            state = State.RUNNING
        elif(state == State.HATCHING):
            hatch()
            num_poke += 1
            num_eggs -= 1
            state == State.RUNNING
        elif(state == State.STORING):
            storing = find_subimg(poke_center)
            if(storing[1] == 'left'):
                store_left()
            elif(storing[1] == 'right'):
                store_right()
            num_poke = 0
            state = State.RUNNING()
            

