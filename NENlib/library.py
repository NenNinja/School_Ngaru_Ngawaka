import pygame
from pathlib import Path
import math
import random
import cProfile, pstats, io
import threading
keys = [0] * 512

def asset(string = "FILENAME"):
    a = (Path(__file__).resolve()).parent
    return str(a) + "/assets/" + string

class KeyPress:
    def __init__(self, key):
        self.key = key
        self.pressed = False
        self.down = False

    def update(self, keys):
        if keys[self.key]:
            if self.down:
                self.pressed = False
            else:
                self.pressed = True
            self.down = True
        else:
            self.down = False


class Mouse:
    def __init__(self):
        self.rect = [0,0,0,0]
        self.pressed = [False,False]
        self.down = [False,False]
        self.x = 0
        self.y = 0
        self.prevPos = [0,0]
        self.vel = [0,0]
    
    def update(self):
        self.pressed = [False,False]
        mousePos = pygame.mouse.get_pos()
        self.x = mousePos[0]
        self.y = mousePos[1]
        self.rect = [self.x, self.y, 0,0]
        pressed = pygame.mouse.get_pressed(num_buttons=3)
        if pressed[0]:
            if self.down[0]:
                self.pressed[0] = False
            else:
                self.pressed[0] = True
            self.down[0] = True
        else:
            self.down[0] = False

        if pressed[1]:
            if self.down[1]:
                self.pressed[1] = False

            else:
                self.pressed[1] = True
            self.down[1] = True
        else:
            self.down[1] = False
        
        self.vel[0] = self.x - self.prevPos[0]
        self.vel[1] = self.y - self.prevPos[1]
        self.prevPos = [self.x, self.y]

mouse = Mouse()


def init(windowW, windowH, caption):
    pygame.init()
    window = pygame.display.set_mode((windowW,windowH))#, flags=pygame.SCALED | pygame.HIDDEN)
    pygame.display.set_caption(caption)
    return window

def AABBColision(rect1, rect2):
    x1 = rect1[0] + rect1[2] > rect2[0]
    x2 = rect1[0] < rect2[0] + rect2[2]
    y1 = rect1[1] + rect1[3]> rect2[1]
    y2 = rect1[1] < rect2[1] + rect2[3]
    
    return x1 and x2 and y1 and y2

def AABBColisionDir(rect1, rect2):
    # Resolve collision by choosing the axis with the smallest overlap.
    if not AABBColision(rect1, rect2):
        return [0, 0]

    l1, t1, w1, h1 = rect1
    l2, t2, w2, h2 = rect2
    r1 = l1 + w1
    b1 = t1 + h1
    r2 = l2 + w2
    b2 = t2 + h2

    overlap_x = min(r1, r2) - max(l1, l2)
    overlap_y = min(b1, b2) - max(t1, t2)

    # If horizontal overlap is smaller, resolve horizontally; otherwise vertically.
    if overlap_x < overlap_y:
        cx1 = l1 + w1 / 2
        cx2 = l2 + w2 / 2
        if cx1 < cx2:
            return [-1, 0]
        else:
            return [1, 0]
    else:
        cy1 = t1 + h1 / 2
        cy2 = t2 + h2 / 2
        if cy1 < cy2:
            return [0, -1]
        else:
            return [0, 1]

class Image:
    def __init__(self, src, spriteSize):
        self.src = src
        self.spriteW = spriteSize[0]
        self.spriteH = spriteSize[1]
        self.spriteLine = 0
        self.img = pygame.image.load(src)
        self.img.set_colorkey((0,255,0))

    def spriteLineSet(self, num):
        self.spriteLine = num

    def draw(self, window, pos, rot=0, line = None, scale = 2):
        if line != None:
            self.spriteLine = line
        s = pygame.Surface((self.spriteW, self.spriteH))
        s.blit(self.img.convert() , (0, 0 - self.spriteH * self.spriteLine))
        window.blit(pygame.transform.scale(pygame.transform.rotate(s, rot), [self.spriteW * scale, self.spriteH * scale]), [pos[0], pos[1], self.spriteW, self.spriteH])
        

def normalize(num):
    return math.sqrt(num**2)

def lerp(cur, tar, t, dt = 1):
    return cur + (tar - cur) * t * dt * 40

def listLerp(cur, tar, t, dt = 1):
    for i in range(len(cur)):
        cur[i] = cur[i] + (tar[i] - cur[i]) * t * dt  * 40
    return cur


def drawRect(window, rect, color, rot=0):
    theta = rot/180 * math.pi
    
    r = [
        [-rect[2]/2, -rect[3]/2],
        [rect[2]/2, -rect[3]/2],
        [rect[2]/2, rect[3]/2], 
        [-rect[2]/2, rect[3]/2]
        ]
    for point in r:
        a = math.cos(theta)
        b = math.sin(theta)
        c = math.sin(theta)
        d = math.cos(theta)
        
        x = point[0] * math.cos(theta) - point[1] * math.sin(theta)
        y = point[0] * math.sin(theta) + point[1] * math.cos(theta)
        point[0] = x + rect[0]
        point[1] = y + rect[1]
    pygame.draw.polygon(window, color, r)



def drawTriangle(window, rect, color, rot=0):
    theta = rot
    
    r = [
        [-rect[2]/2, -rect[3]/2],
        [rect[2]/2, -rect[3]/2],
        [0, rect[3]/2]
        ]
    for point in r:
        x = point[0] * math.cos(theta) - point[1] * math.sin(theta)
        y = point[0] * math.sin(theta) + point[1] * math.cos(theta)
        point[0] = x + rect[0]
        point[1] = y + rect[1]
    pygame.draw.polygon(window, color, r)

def drawText(window, string, col, pos, size, drawAtCenter=False, theta = 0):
    font = pygame.font.SysFont("Aerial",size)
    img = font.render(string, True, col)

    img = pygame.transform.rotate(img, -theta)

    if drawAtCenter:
        textRect = img.get_rect()
        textRect.center = pos
        window.blit(img, textRect)
    else:
        window.blit(img, pos)

def drawText2(window, text, color, rect, size, drawAtCenter=False, theta=0, aa=True):
    font = pygame.font.SysFont("Arial", size)
    rect = pygame.Rect(rect)
    
    # Prepare text wrapping
    words = text.split(" ")
    lines = []
    line = ""

    for w in words:
        test = line + w + " "
        if font.size(test)[0] < rect.width:
            line = test
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)  # last line

    # Determine the height of the whole text block
    fontHeight = font.size("Tg")[1]
    text_height = len(lines) * fontHeight

    # Create a surface for the text block
    text_surface = pygame.Surface((rect.width, text_height), pygame.SRCALPHA)

    # Blit each line onto the text surface
    y = 0
    for ln in lines:
        img = font.render(ln.strip(), aa, color)
        text_surface.blit(img, (0, y))
        y += fontHeight

    # Rotate the whole block
    rotated = pygame.transform.rotate(text_surface, -theta)
    rotated_rect = rotated.get_rect()

    # Position the rotated block
    if drawAtCenter:
        rotated_rect.center = rect.center
    else:
        rotated_rect.topleft = rect.topleft

    window.blit(rotated, rotated_rect.topleft)




def profile(fnc):
    """A decorator that uses cProfile to profile a function"""
    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

def threadstart(target, args=()):
    threading.Thread(
            target=target,
            args=args,
            daemon=True
        ).start()