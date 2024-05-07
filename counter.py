import threading
import pygame
import os

pygame.init()
class SharedCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
        self.my_sound = pygame.mixer.Sound(os.path.abspath("military-alarm-129017.mp3"))
    

    def increment(self):
        with self.lock:
            self.value += 1

    def incrementByValue(self, value):
        with self.lock:
            self.value += value

    def decrement(self):
        with self.lock:
            self.value -= 1

    def get_value(self):
        with self.lock:
            return self.value
    
    def reset(self):
        self.value = 0
    
    def check_value(self):
        if self.value >= 25:
            self.my_sound.play()
            self.value = 0
