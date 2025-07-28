import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Plataforme Reborn")

#Text
font_path = os.path.join("assets", "fonts", "Super Vanilla.ttf")
font = pygame.font.Font(font_path, 60)
small_font = pygame.font.Font(font_path, 32)

#+ y -
volume_imgs = [pygame.image.load(f"assets/volumen/Volumen_{i}.png") for i in range(6)]
volume_level = 3
pygame.mixer.init()
pygame.mixer.music.set_volume(volume_level / 5)

#sistema de vidas
player_health_imgs = [pygame.image.load(f"assets/sysHealth/playerHealth/Health_{i}.png") for i in range(4)]
boss_health_imgs = [pygame.image.load(f"assets/sysHealth/bossHealth/Health_{i}.png") for i in range(9)]
player_health = 3
boss_health = 8

#BG
backgrounds = [pygame.image.load(f"assets/images/BG_{i}.png") for i in range(1, 5)]
current_bg = random.choice(backgrounds)

#:v
player_skins = [pygame.image.load(f"assets/images/players/player_{i}.png") for i in range(1, 6)]
selected_player = None

#no
enemy1 = pygame.image.load("assets/images/enemy's/enemy_1.png")
enemy2 = pygame.image.load("assets/images/enemy's/enemy_2.png")
enemies1 = []
enemies2 = []

#si
player_x, player_y = 100, 600
player_vx = 0
player_vy = 0
grounded = True
player_rect = pygame.Rect(player_x, player_y, 50, 80)

#menu
bg_menu = pygame.image.load("assets/images/menu/BG_menu.png")
menu_items = ["Play", "Options", "Exit"]
menu_rects = []

#Puntuacion
score = 0

clock = pygame.time.Clock()
run = True
state = "menu"

def draw_menu():
    screen.blit(bg_menu, (0, 0))
    menu_rects.clear()
    for i, text in enumerate(menu_items):
        rendered = font.render(text, True, WHITE)
        rect = rendered.get_rect(center=(WIDTH // 2, 200 + i * 100))
        screen.blit(rendered, rect)
        menu_rects.append((rect, text))

def draw_skin_selector():
    screen.fill(BLACK)
    for i, skin in enumerate(player_skins):
        x = 100 + i * 220
        y = 200
        rect = skin.get_rect(topleft=(x, y))
        if rect.collidepoint(pygame.mouse.get_pos()):
            overlay = pygame.Surface(skin.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))  
            screen.blit(skin, (x, y))
            screen.blit(overlay, (x, y))
        else:
            screen.blit(skin, (x, y))

def spawn_enemies():
    enemies1.clear()
    for _ in range(2):
        x = random.randint(100, WIDTH - 100)
        y = 650
        enemies1.append(pygame.Rect(x, y, enemy1.get_width(), enemy1.get_height()))

def draw_game():
    screen.blit(current_bg, (0, 0))
    screen.blit(player_skins[selected_player], (player_rect.x, player_rect.y))
    for enemy in enemies1:
        screen.blit(enemy1, (enemy.x, enemy.y))
    for enemy in enemies2:
        screen.blit(enemy2, (enemy.x, enemy.y))

    #Health
    screen.blit(player_health_imgs[player_health], (10, 10))
    screen.blit(boss_health_imgs[boss_health], (WIDTH - 200, 10))

    #Volumen
    screen.blit(volume_imgs[volume_level], (WIDTH//2 - 50, 10))

    #score
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 60, 60))

def draw_game_over():
    screen.fill(BLACK)
    text = font.render("Game Over", True, WHITE)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

def draw_victory():
    screen.fill(BLACK)
    text = font.render("You Win!", True, WHITE)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

while run:
    clock.tick(FPS)
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, text in menu_rects:
                    if rect.collidepoint(event.pos):
                        if text == "Play":
                            state = "select_skin"
                        elif text == "Exit":
                            run = False

        elif state == "select_skin":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, skin in enumerate(player_skins):
                    rect = skin.get_rect(topleft=(100 + i * 220, 200))
                    if rect.collidepoint(event.pos):
                        selected_player = i
                        spawn_enemies()
                        state = "game"

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS and volume_level > 0:
                    volume_level -= 1
                    pygame.mixer.music.set_volume(volume_level / 5)
                elif event.key == pygame.K_EQUALS and volume_level < 5:
                    volume_level += 1
                    pygame.mixer.music.set_volume(volume_level / 5)

    keys = pygame.key.get_pressed()
    if state == "game":
        if keys[pygame.K_a]:
            player_rect.x -= 5
        if keys[pygame.K_d]:
            player_rect.x += 5
        if keys[pygame.K_SPACE] and grounded:
            player_vy = -15
            grounded = False

        player_vy += 1
        player_rect.y += player_vy
        if player_rect.y >= 600:
            player_rect.y = 600
            player_vy = 0
            grounded = True

        # GAAAAAAAAAAAAAAAA
        if random.randint(0, 30) == 0:
            x = random.randint(0, WIDTH - enemy2.get_width())
            enemies2.append(pygame.Rect(x, 0, enemy2.get_width(), enemy2.get_height()))

        for enemy in enemies2[:]:
            enemy.y += 5
            if enemy.y > HEIGHT:
                enemies2.remove(enemy)
            elif player_rect.colliderect(enemy):
                enemies2.remove(enemy)
                player_health -= 1
                if player_health < 0:
                    player_health = 0

        for enemy in enemies1[:]:
            if player_rect.colliderect(enemy):
                enemies1.remove(enemy)
                score += 10
                boss_health -= 1
                if boss_health < 0:
                    boss_health = 0

        if player_health == 0:
            state = "game_over"
        elif boss_health == 0:
            state = "victory"

    if state == "menu":
        draw_menu()
    elif state == "select_skin":
        draw_skin_selector()
    elif state == "game":
        draw_game()
    elif state == "game_over":
        draw_game_over()
    elif state == "victory":
        draw_victory()

    pygame.display.flip()

pygame.quit()
