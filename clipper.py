
import pygame
import math
import re
pygame.init()
SCREENRECT = pygame.rect.Rect(0, 0, 2000, 1500)
winstyle = 0  # |FULLSCREEN
bestdepth = pygame.display.mode_ok(SCREENRECT.size)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

class Commands:
    def __init__(self, events):
        self.new_key_pressed = False
        for e in events:
            if e.type == pygame.constants.KEYDOWN:
                self.new_key_pressed = True

    def get_move_command(self):
        key = pygame.key.get_pressed()

        increase = 8
        #slow mode
        if key[pygame.constants.K_LSHIFT]:
            if self.new_key_pressed:
                increase = 1
            else:
                return None

        if key[pygame.constants.K_LEFT]:
            return (-increase, 0)
        elif key[pygame.constants.K_RIGHT]:
            return (increase, 0)
        elif key[pygame.constants.K_DOWN]:
            return (0, increase)
        elif key[pygame.constants.K_UP]:
            return (0, -increase)

    def get_resize_command(self):
        key = pygame.key.get_pressed()

        increase = 4
        # slow mode
        if key[pygame.constants.K_LSHIFT]:
            if self.new_key_pressed:
                increase = 1
            else:
                return None

        if key[ord('a')]:
            return (-increase, 0)
        elif key[ord('d')]:
            return (increase, 0)
        elif key[ord('s')]:
            return (0, increase)
        elif key[ord('w')]:
            return (0, -increase)

    def get_zoom_commad(self):
        key = pygame.key.get_pressed()
        if not self.new_key_pressed:
            return None

        if key[pygame.constants.K_MINUS]:
            return -0.1
        elif key[pygame.constants.K_EQUALS]:
            return 0.1

    def is_add_rect_commad(self):
        key = pygame.key.get_pressed()
        if self.new_key_pressed and key[pygame.constants.K_RETURN]:
            return True
        return False


def load_saved():
    import os
    if not os.path.isfile('locations.txt'):
        print("no locations.txt file found. Starting fresh")
        return []
    
    try:
        file = open("locations.txt")
    except Exception as e:
        print("could not open file locations.txt")
        raise e
    
    lines = file.readlines()
    file.close()
    
    rects = []
    for index, line in enumerate(lines):
        parts = None
        try:
            pass
        except Exception as e:
            print("could not parse input line " + str(index))
            raise e
        
        parts = re.match("^(?P<left>\d*),\s*(?P<top>\d*),\s*(?P<width>\d*),\s*(?P<height>\d*)\s*$", line)  
        parts = parts.groupdict()
        if len(parts) < 4:
            print("")
        
        rect = None
        try: 
            rect = pygame.Rect(
                int(parts['left']), 
                int(parts['top']), 
                int(parts['width']), 
                int(parts['height']))
        except Exception as e:
            print("could not create rect from parts of line " + index + "line should be in format 'top, left, width, height'")
            raise e
        rects.append(rect)
    return rects

def save_to_file(rects):
    file = open("locations.txt", "w")
    for rect in rects:
        file.write("{}, {}, {}, {}\n".format(rect.left, rect.top, rect.width, rect.height))
    
            
            
        

def start_clipper(image):
    INITIAL_RECT = pygame.Rect(0, 0, 100, 100)
    current = INITIAL_RECT.copy()
    rects = load_saved()
    zoom = 1
    surface = pygame.Surface((SCREENRECT.width, SCREENRECT.height))
    while True:
        new_event = False
        events = pygame.event.get()
        commands = Commands(events)
        for e in events:
            if e.type == pygame.constants.QUIT:
                return
            if e.type == pygame.constants.KEYDOWN:
                new_event = True
        key = pygame.key.get_pressed()

        if new_event and key[pygame.constants.K_LSHIFT] and key[ord('s')]:
            save_to_file(rects)

        move_delta = commands.get_move_command()
        if move_delta != None:
            current.x += move_delta[0]
            current.y += move_delta[1]

        resize_delta = commands.get_resize_command()
        if resize_delta != None:
            current.width += resize_delta[0]
            current.height += resize_delta[1]

        zoom_command = commands.get_zoom_commad()
        if zoom_command != None:
            zoom += zoom_command

        if commands.is_add_rect_commad():
            rects.append(current)
            current = INITIAL_RECT.copy()

        surface.fill((0, 0, 0))
        surface.blit(image, (0, 0))
        for r in rects:
            pygame.draw.rect(surface, (255, 255, 255), r, 2)
        pygame.draw.rect(surface, (255, 255, 255), current, 2)

        zoomed = pygame.transform.scale(surface, ( math.floor(SCREENRECT.width * zoom), math.floor(SCREENRECT.height * zoom)))
        screen.blit(zoomed, (0, 0))
        pygame.display.flip()


image = pygame.image.load('../assets/jungle-tileset.png')
start_clipper(image)

