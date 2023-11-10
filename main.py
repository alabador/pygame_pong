from typing import Any
import pygame
import sys
import random

pygame.init()
pygame.display.set_caption('Pong')
display_w, display_h = 800, 400
display = pygame.display.set_mode((display_w, display_h))
clock = pygame.time.Clock()

#Sounds
pygame.mixer.init()
bounce_sound = pygame.mixer.Sound('sounds/bounce-8bit.wav')
bounce_sound.set_volume(0.1)
win_sound = pygame.mixer.Sound('sounds/win.ogg')
win_sound.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self, is_player) -> None:
        super().__init__()
        self.y = 10
        self.score = 0
        if is_player:
            self.x = 5
            self.paddle = pygame.Rect(self.x, self.y, 10, 70)
            self.player = True
        else:
            self.x = display_w - 15
            self.paddle = pygame.Rect(self.x, self.y, 10, 70)
            self.player = False
    def draw_paddle(self):
        pygame.draw.rect(display, 'WHITE', self.paddle)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.player:
            if keys[pygame.K_w]:
                self.paddle.y -= 10
            if keys[pygame.K_s]:
                self.paddle.y += 10
        else:
            if keys[pygame.K_UP]:
                self.paddle.y -= 10
            if keys[pygame.K_DOWN]:
                self.paddle.y += 10
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
        self.x_movement = 8
        self.y_movement = random.randint(-10, 10)
        self.radius = 10
        self.round_active = True
        self.object = pygame.draw.circle(display, (66, 214, 255), (self.x, self.y), self.radius)
    def draw_ball(self):
        self.object = pygame.draw.circle(display, (66, 214, 255), (self.x, self.y), self.radius)
    def movement(self):
        self.x += self.x_movement
        self.y += self.y_movement
    def check_collision(self):
        if self.object.colliderect(player.paddle):
            pygame.mixer.Channel(1).play(bounce_sound)
            self.x_movement = -self.x_movement
        if self.object.colliderect(opp.paddle):
            pygame.mixer.Channel(1).play(bounce_sound)
            self.x_movement = -self.x_movement
        if self.object.y <= 10:
            pygame.mixer.Channel(1).play(bounce_sound)
            self.y_movement = -self.y_movement
        if self.object.y >= display_h - 20:
            pygame.mixer.Channel(1).play(bounce_sound)
            self.y_movement = -self.y_movement
    def reset(self):
        self.x = display_w/2
        self.y = display_h/2
        self.x_movement = 0
        self.y_movement = 0
        self.round_active = False
    def restart_movement(self):
        self.y_movement = random.randint(-10, 10)
        self.x_movement = 8
        self.round_active = True
    def check_win(self):
        if self.object.x > display_w + self.radius:
            player.score += 1
            pygame.mixer.Channel(2).play(win_sound)
            self.reset()
        if self.object.x < 0 - self.radius:
            opp.score += 1
            pygame.mixer.Channel(2).play(win_sound)
            self.reset()       
    def update(self) -> None:
        self.draw_ball()
        self.check_collision()
        self.check_win()
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
    
def score_board():
    score_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 24)
    player_score_text = score_font.render(f"Player: {player.score}", False, "WHITE")
    player_score_rect = player_score_text.get_rect(center = (display_w/4, 350)) 
    cpu_score_text = score_font.render(f"CPU: {opp.score}", False, "WHITE")
    cpu_score_rect = cpu_score_text.get_rect(center = (display_w * 3/4, 350)) 

    display.blit(player_score_text, player_score_rect)
    display.blit(cpu_score_text, cpu_score_rect)
    
def reset_prompt():
    prompt_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 20)
    
    prompt_text = prompt_font.render(f"Press SPACE to start round", False, "WHITE")
    prompt_rect = prompt_text.get_rect(center = (display_w/2, display_h/2))
    pygame.draw.rect(display, "BLACK", prompt_rect)
    
    prompt_text2 = prompt_font.render(f"First to 10 wins!", False, "WHITE")
    prompt_rect2 = prompt_text2.get_rect(center = (display_w/2 , display_h/2 + 50))

    display.blit(prompt_text, prompt_rect)
    if player.score < 1 and opp.score < 1:
        pygame.draw.rect(display, "BLACK", prompt_rect2)
        display.blit(prompt_text2, prompt_rect2)

def win_screen(winning_player:Player):
    pygame.Surface.fill(display, 'BLACK')
    prompt_font = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 24)
    winner = winning_player
    if winning_player.player:
        player_type = "Player"
    else:
        player_type = "Computer"
    prompt_text = prompt_font.render(f"{player_type} wins!", False, "WHITE")
    prompt_rect = prompt_text.get_rect(center = (display_w/2, display_h/2))
    pygame.draw.rect(display, "BLACK", prompt_rect)
    
    prompt_text2 = prompt_font.render(f"Press ESC to start a new game!", False, "WHITE")
    prompt_rect2 = prompt_text2.get_rect(center = (display_w/2, display_h/2 + 50))
    pygame.draw.rect(display, "BLACK", prompt_rect2)

    display.blit(prompt_text, prompt_rect)
    display.blit(prompt_text2, prompt_rect2)


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
                player.score = 0
                opp.score = 0
            if event.key == pygame.K_SPACE and not ball.round_active:
                ball.restart_movement()
    if game_active == True:
        display.fill((0,0,0))
        draw_bg()
        player.update()
        opp.update()
        ball.update()
        score_board()
        if not ball.round_active:
            reset_prompt()
        if player.score == 10:
            win_screen(player)
        if opp.score == 10:
            win_screen(opp)
    else:
        game_active = render_menu()
        ball.reset()
    pygame.display.update()
    clock.tick(60)