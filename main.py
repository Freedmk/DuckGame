import pygame, sys
import os

pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Game!")

WHITE=(255,255,255)
BLUE=(32, 30, 117)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH//2)-5,0,10,HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

DUCK_WIDTH, DUCK_HEIGHT = 55,40

GREEN_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

DUCK_IMAGE_GREEN = pygame.image.load(os.path.join('assets', 'kaczuha_green.png'))
DUCK_GREEN = pygame.transform.flip(pygame.transform.scale(DUCK_IMAGE_GREEN,(DUCK_WIDTH,DUCK_HEIGHT)), True, False)

DUCK_IMAGE_YELLOW = pygame.image.load(os.path.join('assets', 'kaczuha_yellow.png'))
DUCK_YELLOW = pygame.transform.scale(DUCK_IMAGE_YELLOW,(DUCK_WIDTH,DUCK_HEIGHT))

QUACK_ATTACK_GREEN = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'quackAttack_green.png')), (45,30))
QUACK_ATTACK_YELLOW = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'quackAttack_yellow.png')), (45,30)), True, False)
POND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ocean.png')), (WIDTH,HEIGHT))

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'quack.wav'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'bamboo-hit.wav'))

def draw_window(yellow, green, green_bullets, yellow_bullets, green_health, yellow_health):
    WIN.blit(POND, (0, 0))    
    pygame.draw.rect(WIN, BLUE, BORDER)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, BLUE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, BLUE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width()-10,10))
    WIN.blit(green_health_text, (10,10))
    WIN.blit(DUCK_GREEN, (green.x, green.y))
    WIN.blit(DUCK_YELLOW, (yellow.x,yellow.y))

    for bullet in green_bullets:
        WIN.blit(QUACK_ATTACK_GREEN, (bullet.x, bullet.y))
    
    for bullet in yellow_bullets:
        WIN.blit(QUACK_ATTACK_YELLOW, (bullet.x, bullet.y))
    
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

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)

def main():
    green = pygame.Rect(100, 300, DUCK_WIDTH, DUCK_HEIGHT)
    yellow = pygame.Rect(700, 300, DUCK_WIDTH, DUCK_HEIGHT)
    green_bullets = []
    yellow_bullets = []
    green_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height//2 - 2, 45,30)
                    green_bullets.append(bullet)
                    
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(yellow.x, yellow.y+yellow.height//2 - 2, 45,30)
                    yellow_bullets.append(bullet)
                    
            if event.type == GREEN_HIT:
                BULLET_HIT_SOUND.play()
                green_health -= 1
                
            
            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                yellow_health -= 1
                

        winner_text = ""
        if green_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "GREEN WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(green_bullets, yellow_bullets, green, yellow)
        draw_window(yellow, green, green_bullets, yellow_bullets, green_health, yellow_health)
main()    

if __name__ == "__main__":
    main()