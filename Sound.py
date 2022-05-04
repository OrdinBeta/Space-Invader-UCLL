class SoundLibrary:
    #import time #niet nodig, alleen voor debugging
    import os
    import pygame
    import glob
    import random

    pygame.mixer.init()

    def __init__(self, value_volume):
        self.geluidlijst = []
        self.table = {}
        self.find_audio_files()
        self.create_sound_table()
        self.change_volume(value_volume)

    def play(self, geluid):
        self.pygame.mixer.Sound.play(self.table[geluid])

    def find_audio_files(self):
        #targetPattern = r"assets\sounds\**\*.ogg"
        self.geluidlijst = self.glob.glob(r"assets\sounds\**\*.ogg")

    def derive_id(self, path):
        #path = path[:-4]
        full_path = path[:-4]
        #relative_path = 'assets/sounds'
        return self.os.path.relpath(full_path, 'assets/sounds') # 'assets/sounds' was hier vroeger relative_path

    def create_sound_table(self):
        for i in self.geluidlijst:
            #variabele = self.derive_id(i)
            self.table[self.derive_id(i)] = self.pygame.mixer.Sound(i) # self.derive_id(i) was hier vroeger variabele
        #print (self.table)
        
    def play_random_explosion(self):
        self.play("explosions\\" + str((self.random.randint(1,6))))
        #self.pygame.mixer.Sound.set_volume(self, self.volume) #werkt nog niet (TypeError: descriptor 'set_volume' for 'Sound' objects doesn't apply to a 'SoundLibrary' object)

    def change_volume(self, volume_value):
        sounds = self.table.values()
        for sound_effect in sounds:
            sound_object = sound_effect
            sound_object.set_volume(volume_value)
        return