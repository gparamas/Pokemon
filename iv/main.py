import webview as wv
from utils1 import *

class API():
    def __init__(self):
        self.name = ''
        self.nat = ''
        self.level = 0
        self.stats = dict()
        self.base = dict()
        self.ivs = dict()
        self.evs = list()

    def change_state_one(self):
        img, s = get_both_ss_test()
        #img = get_ss()
        self.nat = get_nature(img)
        self.name = get_name(img)
        self.level = get_level(img)

    def change_state_two(self, evs):
        self.evs = evs
        s, img = get_both_ss_test()
        #img = get_ss()
        self.stats = get_stats(img)
        self.base = get_base_stats(self.name)
        self.ivs['hp'] = calc_iv_hp(self.base['hp'], self.stats['hp'], self.level, evs[0])
        self.ivs.update(calc_iv_stat(self.base, self.stats, self.nat, self.level, evs[1::]))

    def calc(self):
        self.ivs['hp'] = calc_iv_hp(self.base['hp'], self.stats['hp'], self.level, self.evs[0])
        self.ivs.update(calc_iv_stat(self.base, self.stats, self.nat, self.level, self.evs[1::]))


    def change_state_zero(self):
        self.name = ''
        self.nat = ''
        self.level = 0
        self.stats = dict()
        self.base = dict()

    def get_ivs(self):
        print(self.ivs)
        return self.ivs

    def get_stats(self):
        print(self.stats)
        return self.stats
    
    def get_evs(self):
        print(self.evs)
        return self.evs

    def set_evs(self, evs):
        self.evs = evs
    
    def get_name(self):
        return self.name
    
    def get_level(self):
        return self.level
    
    def get_nature(self):
        return self.nat
    
a = API()
print(a.name, a.nat, a.level, a.stats)
window = wv.create_window('s', url='D:\\Pokemon\\iv\\first_window.html', js_api=a)
wv.start(debug=True)

