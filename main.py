from typing import Any
import pygame
import sys
import random

pygame.init()
pygame.display.set_caption('Pong')
display_w, display_h = 800, 400
display = pygame.display.set_mode((display_w, display_h))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, is_player) -> None:
        super().__init__()
        self.y = 10
        if is_player:
            self.x = 10
            self.paddle = pygame.Rect(self.x, self.y, 10, 70)
            self.player = True
        else:
            self.x = display_w - 20
            self.paddle = pygame.Rect(self.x, self.y, 10, 70)
            self.player = False
    def draw_paddle(self):
        pygame.draw.rect(display, 'WHITE', self.paddle)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.player:
            if keys[pygame.K_w]:
                self.paddle.y -= 5
            if keys[pygame.K_s]:
                self.paddle.y += 5
        else:
            if keys[pygame.K_UP]:
                self.paddle.y -= 5
            if keys[pygame.K_DOWN]:
                self.paddle.y += 5
    def check_collision(self):
        if self.paddle.top <= 10:
            self.paddle.top = 10
        elif self.paddle.bottom >= display_h - 10:
            self.paddle.bottom = display_h - 10
    def update(self) -> None:
        self.draw_paddle()
        self.player_input()
        self.check_collision()

class Ball(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.x = display_w/2
        self.y = display_h/2
        self.x_movement = 5
        self.y_movement = 5
        self.radius = 10
        self.object = pygame.draw.circle(display, (66, 214, 255), (self.x, self.y), self.radius)
    def draw_ball(self):
        self.object = pygame.draw.circle(display, (66, 214, 255), (self.x, self.y), self.radius)
    def movement(self):
        self.x += self.x_movement
    def check_collision(self):
        if self.object.colliderect(player.paddle):
            self.x_movement = -self.x_movement
        elif self.object.colliderect(opp.paddle):
            self.x_movement = -self.x_movement
    def update(self) -> None:
        self.draw_ball()
        self.check_collision()
        self.movement()


def draw_bg():
    offwhite = (207, 59, 29)
    border_top = pygame.draw.line(display, offwhite, (0,0), (display_w,0), 15)
    border_bottom = pygame.draw.line(display, offwhite, (0, display_h), (display_w, display_h), 15)
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
    


player = Player(True)
opp = Player(False)
ball = Ball()

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
        player.update()
        opp.update()
        ball.update()
    else:
        game_active = render_menu()
    pygame.display.update()
    clock.tick(60)