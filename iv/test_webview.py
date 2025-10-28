import webview as wv
from utils1 import *

class API():
    def init(self):
        self.state = 0
        self.name = ''
        self.nat = ''
        self.level = 0
        self.stats = dict()
        self.base = dict()

    def change_state_one(self):
        self.state = 1
        img = get_ss()
        self.nat = get_nature(img)
        self.name = get_name(img)
        self.level = get_level(img)

    def change_state_two(self):
        self.state = 2
        img = get_ss()
        self.stats = get_stats(img)
        self.base = get_base_stats(self.name)
    
    def change_state_zero(self):
        self.state = 0
        self.name = ''
        self.nat = ''
        self.level = 0
        self.stats = dict()
        self.base = dict()

window = wv.create_window('s', 'D:\\Pokemon\\iv\\first_window.html')

