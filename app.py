import math
from operator import xor #lijkt niet nodig
import random
from re import X
from tkinter import font #lijkt niet nodig
import pygame
import time #zeker niet nodig voor final game, alleen voor debugging
import sys
from pygame.display import flip
import looping
import cooldown
import Sound

pygame.init()
pygame.font.get_fonts()

#mag waarscijnlijk in aparte/juist class gezet worden (dit is een beetje dom hier)
cool_down = cooldown.Cooldown(1)
mine_cooldown = cooldown.Cooldownmine(2)


def main(size = (1101, 601)):
        
        pygame.mixer.music.set_volume(0.35) 
        status = state(60)
        surface = pygame.display.set_mode(size, pygame.RESIZABLE)
        intro_screen = Intro()
        intro_screen.intro_screening(surface)
        

        

        

        #Infinite loop here
        while True:
            
           


            status.render(surface)
            status.update(status, surface)
            UserInput.process_key_inputs(status)
                            
            UserInput.is_quit()
            pass


class Music:

    def change_music_to(self, music_file, looping = -1, starting = 0.0, fadeing_ms = 1000):
        self.stop_music()
        pygame.mixer.music.load("assets/music/{}".format(music_file))
        pygame.mixer.music.play(looping, starting, fadeing_ms)
    
    def stop_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


class Spaceship:    

    def __init__(self):
        self.schip_image = pygame.image.load('assets/images/sprites/spaceship.png')
        self.ship_x = 500
        self.ship_y = 500
        self.ship_speed = 0.5
        self.wobble_ammount = 50
        
    def render_spaceship(self, surface, time_difference):
        self.ship_wobble(time_difference)

        if self.ship_x > surface.get_width() + 20:
            self.ship_x = 0
        elif self.ship_x < -20:
            self.ship_x = surface.get_width() + 20
        elif self.ship_y > surface.get_height():
            self.ship_y = surface.get_height() - 20
        elif self.ship_y < -20:
            self.ship_y = -20
        
        self.render(surface)
   
    def update_y(self, new_y):
        self.ship_y += new_y

    def update_x(self, new_x):
        self.ship_x += new_x 
    
    def ship_wobble(self, time_difference):
        self.update_x(random.randint(-self.wobble_ammount, self.wobble_ammount)*time_difference)
        self.update_y(random.randint(-self.wobble_ammount, self.wobble_ammount)*time_difference)

    @property
    def bounding_box(self):
        return pygame.Rect((self.ship_x - pygame.Surface.get_width(self.schip_image)/2), (self.ship_y + pygame.Surface.get_height(self.schip_image)/2), pygame.Surface.get_width(self.schip_image), pygame.Surface.get_height(self.schip_image))
    
    def render(self, surface):
        surface.blit(self.schip_image, (self.ship_x,self.ship_y))


class Mine():

    def __init__(self,mine_x,mine_y):
        self.mines_image = pygame.image.load('assets/images/sprites/mine.png')
        self.mine_x = mine_x
        self.mine_y = mine_y
        self.speed=2
    
    def render(self, surface,):
        surface.blit(self.mines_image, (self.mine_x,self.mine_y) )

    def update(self,elapsed_seconds):
        self.mine_y += self.speed*elapsed_seconds

    @property
    def bounding_box(self):
        return pygame.Rect((self.mine_x - pygame.Surface.get_width(self.mines_image)/2), self.mine_y + pygame.Surface.get_height(self.mines_image)/2, pygame.Surface.get_width(self.mines_image), pygame.Surface.get_height(self.mines_image))


class Bullet:

    def __init__(self, bullet_x_value, bullet_y_value):
        self.bullet = pygame.image.load('assets/images/sprites/bullets/small.png')
        self.bullet_x = bullet_x_value
        self.bullet_y = bullet_y_value
        self.speed = 10
        self.time_left = 150
        self.bullet_drift = 1 #memes als je dit hoog zet

    def render(self, surface):
        surface.blit(self.bullet, (self.bullet_x + 16 ,self.bullet_y) )

    def update(self, elapsed_seconds):
        self.bullet_y -= self.speed * elapsed_seconds
        self.faux_bullet_drift(elapsed_seconds)
        self.time_left -= 1

    def faux_bullet_drift(self, elapsed_seconds): #momenteel bibberen ze maar wat (nie echt random inaccuracy)
        self.bullet_x += random.randint(-self.bullet_drift, self.bullet_drift)*elapsed_seconds

    @property
    def disposed(self):
        return self.time_left <= 0
    
    @property
    def bounding_box(self):
        return pygame.Rect((self.bullet_x - pygame.Surface.get_width(self.bullet)/2), self.bullet_y + pygame.Surface.get_height(self.bullet)/2, pygame.Surface.get_width(self.bullet), pygame.Surface.get_height(self.bullet))


class state:
    
    def __init__(self, fps_value = 60, volume_value = 0.35):
        self.falcon = Spaceship()
        self.achtergrond = Background()
        self.tijd = 0
        self.new_tijd = 0
        self.target_fps = fps_value
        self.bullets = []
        self.mines = []
        self.sound_library = Sound.SoundLibrary(volume_value) #volume van de sound effects (be warned! de explosions zijn tering luid)
        self.pijn = False #als je pijn wilt lijden makker, zet op True
        #self.score = 0 
    def update(self,status, surface):
        self.tijd = pygame.time.Clock().tick(self.target_fps)
        self.new_tijd = self.tijd/1000
        Background.update(self.achtergrond, 5)
        for i in self.bullets:
            i.update(1)
        cool_down.update(0.1)
        for i in self.mines:
            i.update(1)
        mine_cooldown.update(0.25)
        if mine_cooldown.ready == False:
            pass
        else:
            status.mines.append(Mine(random.randint(0,surface.get_width()),-150))
            mine_cooldown.reset()
        for i in self.bullets:
            if i.disposed:
                self.bullets.remove(i)

        #waarschijnlijk beter om hier 1 functie van te maken die flexiebel gebruikt kan worden
        self.process_ship_collision(self.mines, self.falcon, surface) 
        self.process_bullet_collisions(self.mines, self.bullets)

        #verandert de fps elke frame (doe dit als je pijnt wilt lijden) (echt wel een aanraader toch)
        if self.pijn == True:
            self.falcon.ship_x += (100*self.new_tijd) #verplaats het schip naar rechts lmao
            self.target_fps = random.randint(10, 144) #verandert de fps constant
  
    def process_ship_collision(self, mines, pizza, cuck):
        mine_bounding_boxes = [mine.bounding_box for mine in mines]
   
        if not pizza.bounding_box.collidelist(mine_bounding_boxes) == -1:
            self.sound_library.play_random_explosion()
            main(pygame.Surface.get_size(cuck))
   

    def process_bullet_collisions(self, mines, bullets ):
        
        mine_bounding_boxes = [mine.bounding_box for mine in mines]
        bullet_bounding_boxes = [bullet.bounding_box for bullet in bullets]
        
        for shot_bullet in bullet_bounding_boxes:
            collusion = shot_bullet.collidelist(mine_bounding_boxes)
            if not collusion == -1:
                self.sound_library.play_random_explosion()
                try:
                    mines.pop(collusion)
                except:
                    mines.pop()
                    
        for hit_mine in mine_bounding_boxes:
            colly = hit_mine.collidelist(bullet_bounding_boxes)
            if not colly == -1:
                try:
                    bullets.pop(colly)
                except:
                    bullets.pop()
            
              
        return
    # def score_text(surface):
    #  img=font.render(f'Score:{score}',True,'white')
    #  surface.blit(img,(10,10))

    
    def render(self, surface):
        self.achtergrond.render(surface)
        self.falcon.render_spaceship(surface, self.new_tijd)
        for i in self.mines:
            i.render(surface)
        for i in self.bullets:
            i.render(surface)
        pygame.display.update()
        flip()
        

class Intro:

    def intro_screening(self, surface):
        __muzak = Music()

        __muzak.change_music_to("intro.ogg")

        #infite loop for intro screen
        while True:
            self.render(surface)
            __keys_pressed = UserInput.Keyboard.key_events()

            if self.start_game(__keys_pressed) == True:
                __muzak.change_music_to("nemesis.ogg", starting=11.4, fadeing_ms=1)
                return

            UserInput.is_quit()
            pass

    def render(self, surface):
        pygame.Surface.fill(surface, (100, 20, 20))

        #text !!!dit (of de functie) moet nog herschreven worden als je veranderbare window sizes wilt hebben!!!
        self.render_text(surface, text= "STAR WARS", position=(100,100) ,font_size=50)
        self.render_text(surface, text= "Dit is toch echt wel onroerend goed!", position=(100,200) ,font_size=20)
        self.render_text(surface, text= 'Druk op de knop "ENTER" om te beginnen', position=(600,100) ,font_size=20)
        surface.blit(pygame.image.load('assets/images/sprites/onroerend_goed.jpg'), (100, 230)) #de og's mogen weg
        #surface.blit(pygame.image.load('assets/images/sprites/pers.jpg'), (600, 130))

        pygame.display.update()
        flip()

    def start_game(self, keys_pressed):
        for pressed_key in keys_pressed:
            if pressed_key == pygame.K_RETURN:
                return True
        return False
    
    #gebruik dit om snel en makkelijker tekst te maken op het (intro) scherm (mag waarschijnlijk in een aparte klasse als je ooit de death screen maakt)
    def render_text(self, surface, text="Placeholder", position= (50, 50), font='freesansbold.ttf', font_size = 12, text_collor=(255,255,255), antialias=True):
        rendered_text = pygame.font.Font(font, font_size).render(text, antialias, text_collor)
        surface.blit(rendered_text, position)


class Background:
    

    
    def __init__(self):
        self.background = pygame.image.load('assets/images/backgrounds/space.jpg')
        self.height = pygame.Surface.get_height(self.background)
        self.loopobject = looping.LoopingVariable(self.height)
        self.y = 100

    def render(self, surface):
        surface.blit(self.background, (0, self.y) )
        surface.blit(self.background, (0, self.y - self.height) )

    def update(self, elapsed_seconds):
        self.loopobject.increase(elapsed_seconds)
        self.y = self.loopobject.value


class UserInput:

    def is_quit(exclude_event_type = None): #clears the event queue
        for event in pygame.event.get(exclude= exclude_event_type):
                if event.type == pygame.QUIT:
                    sys.exit()

    def process_key_inputs(status): #ge kunt nie naar links boven gaan lol. tis een feature
        going_speed = status.falcon.ship_speed*status.tijd
        keys_pressed = UserInput.Keyboard.key_events()
        ship_coordinates = UserInput.Keyboard.check_direction(keys_pressed)
        status.falcon.update_x(ship_coordinates[0]*going_speed)
        status.falcon.update_y(ship_coordinates[1]*going_speed)

        if pygame.K_SPACE in keys_pressed:
            if cool_down.ready == False:
                pass
            else:
                status.bullets.append(Bullet(status.falcon.ship_x,status.falcon.ship_y))
                status.sound_library.play('shots\pew')
                cool_down.reset()

        #pause
        if pygame.K_p in keys_pressed:
            while pygame.K_p in keys_pressed:
                keys_pressed = UserInput.Keyboard.key_events()
                UserInput.is_quit((pygame.KEYDOWN, pygame.KEYUP))
            print("game paused")
            while not pygame.K_p in keys_pressed:
                keys_pressed = UserInput.Keyboard.key_events()
                UserInput.is_quit((pygame.KEYDOWN, pygame.KEYUP))
            print("game unpaused")
            while pygame.K_p in keys_pressed:
                keys_pressed = UserInput.Keyboard.key_events()
                UserInput.is_quit((pygame.KEYDOWN, pygame.KEYUP))            


    class Keyboard:

        def key_events(keys = set()): # <-- dit werkt voor een of andere reden (kan waarschijnlijk beter)
            for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                if event.type == pygame.KEYDOWN:
                    keys.add(event.__dict__.get("key"))
                elif event.type == pygame.KEYUP:
                    keys.discard(event.__dict__.get("key"))
            return keys

        # wordt niet gebruikt
        def is_key_down(key):
            for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                if event.__dict__.get("key") == key:
                    return True
            return False
        
        # wordt niet gebruik
        def any_key_down():
            for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN:
                    return True
            return False
        
        def check_direction(keys_pressed):
            coordinates = [0, 0] # [x, y]
            if pygame.K_DOWN in keys_pressed:
                coordinates[1] += 1
            if pygame.K_UP in keys_pressed:
                coordinates[1] -= 1
            if pygame.K_RIGHT in keys_pressed:
                coordinates[0] += 1
            if pygame.K_LEFT in keys_pressed:
                coordinates[0] -= 1

            cuck = math.sqrt(2)/2
            if coordinates == [0, 0]:
                return [0, 0]
            elif coordinates == [1, 1]:
                return [cuck, cuck]
            elif coordinates == [-1, 1]:
                return [-cuck, cuck]
            elif coordinates == [-1, -1]:
                return [-cuck, -cuck]
            elif coordinates == [1, -1]:
                return [cuck, -cuck]
            else:
                return coordinates
            
            #fuck it het werkt goed genoeg (niet alsof iemand ooit met joystick wilt spelen ofzo lmao)


#main die hier wa staat te doen
main()