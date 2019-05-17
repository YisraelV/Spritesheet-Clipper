#!/usr/bin/python3

import pygame
pygame.init()
SCREENRECT = pygame.rect.Rect(0, 0, 2000, 1500)
winstyle = 0  # |FULLSCREEN
bestdepth = pygame.display.mode_ok(SCREENRECT.size)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

def start_clipper(image):
    INITIAL_RECT = pygame.Rect(0, 0, 100, 100)
    current = INITIAL_RECT.copy()
    rects = []
    while True:
        new_event = False
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.constants.QUIT:
                return
            if e.type == pygame.constants.KEYDOWN:
                new_event = True
        key = pygame.key.get_pressed()

        if new_event and key[pygame.constants.K_LCTRL] and key[ord('s')]:
            for r in rects:
                print("{},{},{},{}".format(r.x, r.y, r.width, r.height))
                rects = []

        increase = 1 if not key[pygame.constants.K_LSHIFT] or new_event else 0
        if new_event and key[pygame.constants.K_RETURN]:
            rects.append(current)
            current = INITIAL_RECT.copy()
        elif key[pygame.constants.K_LEFT]:
            current.x -= increase
        elif key[pygame.constants.K_RIGHT]:
            current.x += increase
        elif key[pygame.constants.K_DOWN]:
            current.y += increase
        elif key[pygame.constants.K_UP]:
            current.y -= increase

        if key[ord('a')]:
            current.width -= increase
        elif key[ord('d')]:
            current.width += increase
        elif key[ord('s')]:
            current.height += increase
        elif key[ord('w')]:
            current.height -= increase

        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        for r in rects:
            pygame.draw.rect(screen, (255, 255, 255), r, 2)
        pygame.draw.rect(screen, (255, 255, 255), current, 2)
        pygame.display.flip()


image = pygame.image.load('../assets/jungle-tileset.png')
start_clipper(image)

