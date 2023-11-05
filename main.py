import pygame
import sys
import random

pygame.init()
pygame.display.set_caption('Pong')
display_w, display_h = 800, 400
display = pygame.display.set_mode((display_w, display_h))
clock = pygame.time.Clock()

class Player:
    def __init__(self) -> None:
        pass


def draw_bg():
    offwhite = (230,230,230)
    border = pygame.draw.rect(display, offwhite, (0, 0, display_w, display_h), 10)
    divider = pygame.draw.rect(display, offwhite, (display_w/2, 0, 10, display_h))

def render_menu():
    title_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 48)
    instr_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 24)

    bg = pygame.Surface.fill(display, "BLACK")
    menu_title = title_font.render("PONG", False, "White")
    menu_title_rect = menu_title.get_rect(center = (display_w/2, 150))
    instr_text = instr_font.render("PRESS SPACE TO START", False, ("White"))
    instr_rect = instr_text.get_rect(center = (display_w/2, display_h - 150))

    display.blit(menu_title, menu_title_rect)
    display.blit(instr_text, instr_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return True
    




game_active = False
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_active = False
    if game_active == True:
        display.fill((0,0,0))
        draw_bg()
    else:
        game_active = render_menu()
    pygame.display.update()
    clock.tick(60)