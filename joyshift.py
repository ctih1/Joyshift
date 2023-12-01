import pygame
import keyboard
import os
import sys
import json
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
if not os.path.exists("config.json"):
    with open("config.json","w") as f:
        f.write("{\n    \n}")
with open("config.json","r") as f:
    config = json.load(f)
ctheme = config.get("theme","gray")
x_axis = config.get("x",0)
y_axis = config.get("y",1)
ups = config.get("ups",60)
id = config.get("id",0)
if ctheme == "colorful":
    theme = ["#FF0000","#A020F0","#008000","#FFA500","#FFFF00","#808080","#70A3CC"]
elif ctheme == "gray":
    theme = ["#808080","#808080","#808080","#808080","#808080","#808080","#808080"]
pygame_icon = pygame.image.load("joystick.ico")
pygame.display.set_caption("Initializing...")
pygame.display.set_icon(pygame_icon)
pygame.display.init()
pygame.joystick.init()
pygame.font.init()
a = 0
b = 0
clock = pygame.time.Clock()
mode = "manual5"
screen = pygame.display.set_mode((685, 400))
font = pygame.font.SysFont("Helvetica", 30)
try:
    _joystick = pygame.joystick.Joystick(id)
except:
    raise Exception("No Joysticks found.")
_joystick.init()

class Ball:
    def __init__(self):
        self.x = 250
        self.y = 250
        self.loaded = _joystick.get_init()
        self.prev_x = self.x
        self.prev_y = self.y
        self.reset = True
        self.rect = pygame.draw.circle(screen,"#0000ff",(self.x,self.y),10)
    def update(self):
        x = ((_joystick.get_axis(x_axis)+1)*350)-a*350
        y = ((_joystick.get_axis(y_axis)+1)*250)-b*250
        self.x = round(x)
        self.y = round(y)
        if abs(y-200) <= 50:
            self.reset = True
        self.rect = pygame.draw.circle(screen,"#0000ff",(self.x,self.y),10)
            


class Shift:
    class manual:
        def __init__(self):
            self.one = font.render(config.get("k1","1").upper(),False, (0, 0, 0))
            self.two = font.render(config.get("k2","2").upper(),False, (0, 0, 0))
            self.three = font.render(config.get("k3","3").upper(),False, (0, 0, 0))
            self.four = font.render(config.get("k4","4").upper(),False, (0, 0, 0))
            self.five = font.render(config.get("k5","5").upper(),False, (0, 0, 0))
            self.six = font.render(config.get("k6","6").upper(), False, (0, 0, 0))
            self.seven = font.render(config.get("k7","7").upper(),False, (0,0,0))
            self.click = False
        def update(self):
            _1 = pygame.draw.rect(screen,theme[0],(0,0,125,125),5)
            _2 = pygame.draw.rect(screen,theme[1],(0,275,125,125),5)
            _3 = pygame.draw.rect(screen,theme[2],(190,0,125,125),5)
            _4 = pygame.draw.rect(screen,theme[3],(190,275,125,125),5)
            _5 = pygame.draw.rect(screen,theme[4],(375,0,125,125),5)
            _6 = pygame.draw.rect(screen,theme[5],(375,275,125,125),5)
            _7 = pygame.draw.rect(screen,theme[6],(560,275,125,125),5)
            if _1.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k1","1"))
                ball.reset = False
                _joystick.rumble(0,1000,10)
            if _2.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k2","2")) 
                ball.reset = False
            if _3.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k3","3"))
                ball.reset = False
            if _4.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k4","4"))
                ball.reset = False
            if _5.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k5","5"))
                ball.reset = False
            if _6.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k6","6"))
                ball.reset = False
            if _7.colliderect(ball.rect) and ball.reset == True:
                keyboard.press_and_release(config.get("k7","7"))
                ball.reset = False
            else:   
                self.click = False
            screen.blit(self.one, (48,44))
            screen.blit(self.two, (48,319))
            screen.blit(self.three, (238,44))
            screen.blit(self.four,(238,319))
            screen.blit(self.five,(423,44))
            screen.blit(self.six,(423,319))
            screen.blit(self.seven,(608,319))
def reset():
    global a,b
    a = _joystick.get_axis(x_axis)
    b = _joystick.get_axis(y_axis)
    return a,b
def restore():
    global a,b
    a = 0
    b = 0
    return a,b
#axis: 0 = x
#axis: 1 = y
#axis: 2 = throttle
ball = Ball()
manual5 = Shift.manual()
running = True
#reset()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit(0)
    if keyboard.is_pressed("ctrl+p"):
        reset()
    if keyboard.is_pressed("ctrl+o"):   
        restore()
    pygame.display.set_caption(f"Joyshifter < Joystick Info: {_joystick.get_name()} ({_joystick.get_id()}) {_joystick.get_numaxes()}-Axes >")
    screen.fill((255,255,255))
    manual5.update()
    ball.update()
    clock.tick(ups)
    pygame.display.flip()
    