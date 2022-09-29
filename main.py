import pygame, sys
import os

from yaml import YAMLObjectMetaclass

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Game!")

BLUE=(32, 30, 117)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect((WIDTH//2)-5,0,10,HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

DUCK_WIDTH, DUCK_HEIGHT = 55,40

GREEN_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

DUCK_IMAGE_GREEN = pygame.image.load(os.path.join('assets', 'kaczuha_green.png'))
DUCK_GREEN = pygame.transform.flip(pygame.transform.scale(DUCK_IMAGE_GREEN,(DUCK_WIDTH,DUCK_HEIGHT)), True, False)

DUCK_IMAGE_YELLOW = pygame.image.load(os.path.join('assets', 'kaczuha_yellow.png'))
DUCK_YELLOW = pygame.transform.scale(DUCK_IMAGE_YELLOW,(DUCK_WIDTH,DUCK_HEIGHT))

QUACK_ATTACK_GREEN = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'quackAttack_green.png')), (45,30))

POND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ocean.png')), (WIDTH,HEIGHT))

def draw_window(yellow, green, green_bullets, yellow_bullets):
    WIN.blit(POND, (0, 0))    
    pygame.draw.rect(WIN, BLUE, BORDER)
    WIN.blit(DUCK_GREEN, (green.x, green.y))
    WIN.blit(DUCK_YELLOW, (yellow.x,yellow.y))

    for bullet in green_bullets:
        WIN.blit(QUACK_ATTACK, (bullet.x, bullet.y))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

def green_handle_movement(keys_pressed, green):
        if(keys_pressed[pygame.K_a] and green.x - VEL > 0): #Left
            green.x -= VEL
        if(keys_pressed[pygame.K_d] and green.x + VEL + green.width < BORDER.x): #Right
            green.x += VEL
        if(keys_pressed[pygame.K_w] and green.y - VEL > 0): #UP
            green.y -= VEL
        if(keys_pressed[pygame.K_s] and green.y + VEL + green.height < HEIGHT): #down
            green.y += VEL

def yellow_handle_movement(keys_pressed, yellow):
        if(keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width): #Left
            yellow.x -= VEL
        if(keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH): #Right
            yellow.x += VEL
        if(keys_pressed[pygame.K_UP] and yellow.y - VEL > 0): #Up
            yellow.y -= VEL
        if(keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT): #Down
            yellow.y += VEL
def handle_bullets(green_bullets, yellow_bullets, green, yellow):
    for bullet in green_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            green_bullets.remove(bullet)
        elif( bullet.x > WIDTH):
            green_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            yellow_bullets.remove(bullet)
        elif( bullet.x < 0):
            yellow_bullets.remove(bullet)
def main():
    green = pygame.Rect(100, 300, DUCK_WIDTH, DUCK_HEIGHT)
    yellow = pygame.Rect(700, 300, DUCK_WIDTH, DUCK_HEIGHT)
    green_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y+yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(green_bullets, yellow_bullets, green, yellow)
        draw_window(yellow, green, green_bullets, yellow_bullets)
    pygame.quit()

if __name__ == "__main__":
    main()