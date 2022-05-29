import pygame, sys
import pygame.freetype
import data.engine as e
clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((600, 400))

font = pygame.font.SysFont(None, 70)

background_img = pygame.image.load('data/images/background.png')
menu_bar_img = pygame.image.load('data/images/main_menu_bar.png')
menu_bar_collide_img = pygame.image.load('data/images/main_menu_bar_collide.png')
logo_img = pygame.image.load('data/images/logo.png')
best_score_img = pygame.image.load('data/images/best_score_bar.png')

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False


def main_menu():
    while True:

        background_rect = pygame.Rect(0,0, 1200, 800)
        screen.blit(background_img, background_rect)
        logo_rect = pygame.Rect(300,100, 600, 186)
        screen.blit(logo_img, logo_rect)

        mx, my = pygame.mouse.get_pos()

        best_score_rect = pygame.Rect(400, 325, 400, 200)
        screen.blit(best_score_img, best_score_rect)
        f = open('best_score.txt', 'r')
        best_score = f.read()
        f.close()
        millis = int(best_score) % 1000
        seconds = int(int(best_score) / 1000 % 60)
        minutes = int(int(best_score) / 60000 % 24)
        best_score = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        draw_text('Best time:', font, (255, 255, 255), screen, 485, 360)
        draw_text(best_score, font, (255, 255, 255), screen, 490, 430)
        button_1 = pygame.Rect(150, 600, 400, 100)
        button_2 = pygame.Rect(650, 600, 400, 100)
        screen.blit(menu_bar_img, button_1)
        draw_text('Play', font, (255, 255, 255), screen, 300, 630)
        screen.blit(menu_bar_img, button_2)
        draw_text('Quit', font, (255, 255, 255), screen, 800, 630)
        if button_1.collidepoint((mx, my)):
            screen.blit(menu_bar_collide_img, button_1)
            draw_text('Play', font, (255, 255, 255), screen, 300, 630)
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            screen.blit(menu_bar_collide_img, button_2)
            draw_text('Quit', font, (255, 255, 255), screen, 800, 630)
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

def game():
    font = pygame.font.SysFont(None, 20)
    font_timer = pygame.freetype.SysFont(None, 24)
    font_timer.origin = True
    pause = False
    damage_moving_right = False
    damage_moving_left = False
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    attack = False
    ghost_fruit_wake_up = False
    air_timer_corn = 0
    frame_count = 0
    heart = 3


    true_scroll = [0, 0]

    def load_map(path):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    e.load_animations('data/images/entities/')

    game_map = load_map('maptest')

    grass_img = pygame.image.load('data/images/grass.png')
    dirt_img = pygame.image.load('data/images/dirt.png')
    grass_L_img = pygame.image.load('data/images/grass_L.png')
    grass_R_img = pygame.image.load('data/images/grass_R.png')
    heart1_img = pygame.image.load('data/images/heart.png')
    heart2_img = pygame.image.load('data/images/heart2.png')
    heart3_img = pygame.image.load('data/images/heart3.png')
    finish_menu_img = pygame.image.load('data/images/finish_menu.png')
    finish_menu_bar_img = pygame.image.load('data/images/finish_menu_bar.png')
    finish_menu_bar_collide_img = pygame.image.load('data/images/finish_menu_bar_collide.png')

    house = e.entity(3648, 405, 91, 95, 'house')

    player = e.entity(304, 1856, 37, 42, 'player')
    #player = e.entity(3600, 400, 37, 42, 'player')

    moabs = []

    moabs.append([0,e.entity(272,1552,33,39,'moab')])
    moabs.append([0, e.entity(688, 1104, 33, 39, 'moab')])
    moabs.append([0, e.entity(1104, 1152, 33, 39, 'moab')])
    moabs.append([0, e.entity(2080, 1504, 33, 39, 'moab')])
    moabs.append([0, e.entity(1840, 848, 33, 39, 'moab')])
    moabs.append([0, e.entity(1584, 848, 33, 39, 'moab')])
    moabs.append([0, e.entity(1840, 416, 33, 39, 'moab')])
    moabs.append([0, e.entity(1840, 288, 33, 39, 'moab')])
    moabs.append([0, e.entity(2160, 416, 33, 39, 'moab')])
    moabs.append([0, e.entity(2160, 288, 33, 39, 'moab')])
    moabs.append([0, e.entity(2400, 352, 33, 39, 'moab')])
    moabs.append([0, e.entity(3216, 480, 33, 39, 'moab')])

    ghost_fruits = []

    ghost_fruits.append([0,e.entity(512,1360,29,46,'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1040, 1504, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1616, 1312, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(2064, 1376, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(2336, 1184, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1968, 864, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1712, 864, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1216, 928, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(1312, 672, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(2016, 416, 29, 46, 'ghost_fruit')])
    ghost_fruits.append([0, e.entity(3392, 480, 29, 46, 'ghost_fruit')])

    jump_corns = []

    jump_corns.append([0,e.entity(848,1104,35,54,'jump_corn')])
    jump_corns.append([0, e.entity(2528, 480, 35, 54, 'jump_corn')])
    jump_corns.append([0, e.entity(2912, 672, 35, 54, 'jump_corn')])



    running = True
    while running:  # game loop
        display.fill((146, 244, 255))
        mx, my = pygame.mouse.get_pos()
        mx = mx/2
        my = my/2



        # map_rendering ---------------------------------------------------- #
        true_scroll[0] += (player.x - true_scroll[0] - 250) / 20
        true_scroll[1] += (player.y - true_scroll[1] - 200) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == '2':
                    display.blit(grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == '3':
                    display.blit(grass_L_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == '4':
                    display.blit(grass_R_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                x += 1
            y += 1


        # player ---------------------------------------------------- #
        player_movement = [0, 0]
        if damage_moving_right == True:
            player_movement[0] += 4
        if moving_right == True:
            player_movement[0] += 2
        if damage_moving_left == True:
            player_movement[0] -= 4
        if moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        if player_movement[0] == 0 and attack == False:
            player.set_action('idle')
        if player_movement[0] > 0 and player_movement[1] > 0 and player_movement[
            1] <= 1 and attack == False and damage_moving_right == True:
            player.set_flip(True)
            player.set_action('walk')
        if player_movement[0] < 0 and player_movement[1] > 0 and player_movement[
            1] <= 1 and attack == False and damage_moving_left == True:
            player.set_flip(False)
            player.set_action('walk')
        if player_movement[0] > 0 and player_movement[1] > 0 and player_movement[
            1] <= 1 and attack == False and damage_moving_right == False:
            player.set_flip(False)
            player.set_action('walk')
        if player_movement[0] < 0 and player_movement[1] > 0 and player_movement[
            1] <= 1 and attack == False and damage_moving_left == False:
            player.set_flip(True)
            player.set_action('walk')
        if player_movement[0] == 0 and player_movement[1] < 0 and attack == False:
            player.set_action('jump')
        if player_movement[0] == 0 and player_movement[1] > 1 and attack == False:
            player.set_action('drop')
        if player_movement[0] > 0 and player_movement[1] < 0 and attack == False and damage_moving_right == True:
            player.set_flip(True)
            player.set_action('jump_movement')
        if player_movement[0] < 0 and player_movement[1] < 0 and attack == False and damage_moving_left == True:
            player.set_flip(False)
            player.set_action('jump_movement')
        if player_movement[0] > 0 and player_movement[1] > 1 and attack == False and damage_moving_right == True:
            player.set_flip(True)
            player.set_action('drop_movement')
        if player_movement[0] < 0 and player_movement[1] > 1 and attack == False and damage_moving_left == True:
            player.set_flip(False)
            player.set_action('drop_movement')
        if player_movement[0] > 0 and player_movement[1] < 0 and attack == False and damage_moving_right == False:
            player.set_flip(False)
            player.set_action('jump_movement')
        if player_movement[0] < 0 and player_movement[1] < 0 and attack == False and damage_moving_left == False:
            player.set_flip(True)
            player.set_action('jump_movement')
        if player_movement[0] > 0 and player_movement[1] > 1 and attack == False and damage_moving_right == False:
            player.set_flip(False)
            player.set_action('drop_movement')
        if player_movement[0] < 0 and player_movement[1] > 1 and attack == False and damage_moving_left == False:
            player.set_flip(True)
            player.set_action('drop_movement')
        if player_movement[0] > 0 and attack == True:
            player.set_flip(False)
            player.set_action('attack')
        if player_movement[0] < 0 and attack == True:
            player.set_flip(True)
            player.set_action('attack')
        if player_movement[0] == 0 and attack == True:
            player.set_action('attack')

        collision_types = player.move(player_movement, tile_rects)

        if collision_types['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
            damage_moving_left = False
            damage_moving_right = False
        else:
            air_timer += 1



        house.display(display, scroll)
        player.change_frame(1)
        player.display(display, scroll)

        # final_menu ---------------------------------------------------- #
        if player.obj.rect.colliderect(house.obj.rect):
            pause = True
            f = open('best_score.txt', 'r')
            best_score = f.read()
            f.close()
            if int(best_score) > frame_count:
                f = open('best_score.txt', 'w')
                f.write(str(frame_count))
                f.close()
            finish_menu = pygame.Rect(200, 100, 200, 200)
            display.blit(finish_menu_img, finish_menu)
            button_1 = pygame.Rect(250, 250, 100, 40)
            display.blit(finish_menu_bar_img, button_1)
            draw_text('To main menu', font, (255, 255, 255), display, 256, 264)
            draw_text('Your time:' + out, font, (255, 255, 255), display, 250, 125)
            millis = int(best_score) % 1000
            seconds = int(int(best_score) / 1000 % 60)
            minutes = int(int(best_score) / 60000 % 24)
            best_score = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
            draw_text('Best time:' + best_score, font, (255, 255, 255), display, 250, 150)
            if button_1.collidepoint((mx, my)):
                display.blit(finish_menu_bar_collide_img, button_1)
                draw_text('To main menu', font, (255, 255, 255), display, 256, 264)
                if click:
                    running = False
        else:
            pause = False


        # entities ---------------------------------------------------- #
        display_r = pygame.Rect(scroll[0], scroll[1], 600, 400)

        # moab ---------------------------------------------------- #
        for moab in moabs:
            if display_r.colliderect(moab[1].obj.rect):
                moab[0] += 0.2
                if moab[0] > 3:
                    moab[0] = 3
                moab_movement = [0, moab[0]]
                if player.x > moab[1].x + 32 and pause == False:
                    moab_movement[0] = 1
                if player.x < moab[1].x - 33 and pause == False:
                    moab_movement[0] = -1

                if moab_movement[0] == 0:
                    moab[1].set_action('idle')

                if moab_movement[0] > 0:
                    moab[1].set_flip(False)
                    fork_flip = False
                    moab[1].set_action('walk')

                if moab_movement[0] < 0:
                    moab[1].set_flip(True)
                    fork_flip = True
                    moab[1].set_action('walk')

                collision_types = moab[1].move(moab_movement, tile_rects)
                if collision_types['bottom'] == True:
                    moab[0] = 0

                moab[1].change_frame(1)
                moab[1].display(display, scroll)

                if player.obj.rect.colliderect(moab[1].obj.rect) and player.y < (moab[1].y - 35) and pause == False:
                    vertical_momentum = -6
                if player.obj.rect.colliderect(moab[1].obj.rect) and player.y > (moab[1].y - 35) and player.x < moab[
                    1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_left = True
                if player.obj.rect.colliderect(moab[1].obj.rect) and player.y > (moab[1].y - 35) and player.x > moab[
                    1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_right = True

        # ghost_fruit ---------------------------------------------------- #
        for ghost_fruit in ghost_fruits:
            if display_r.colliderect(ghost_fruit[1].obj.rect):
                ghost_fruit[0] += 0.2
                if ghost_fruit[0] > 3:
                    ghost_fruit[0] = 3
                ghost_fruit_movement = [0, ghost_fruit[0]]

                if -150 < player.x - (ghost_fruit[1].x) < 150 and pause == False:
                    ghost_fruit_wake_up = True

                if player.x - (ghost_fruit[1].x) > 300 and pause == False:
                    ghost_fruit_wake_up = False
                if player.x - (ghost_fruit[1].x) < -300 and pause == False:
                    ghost_fruit_wake_up = False

                if player.x > ghost_fruit[1].x + 28 and ghost_fruit_wake_up == True and pause == False:
                    ghost_fruit_movement[0] = 0.5
                if player.x < ghost_fruit[1].x - 30 and ghost_fruit_wake_up == True and pause == False:
                    ghost_fruit_movement[0] = -0.5

                if ghost_fruit_movement[0] == 0 and ghost_fruit_wake_up == False:
                    ghost_fruit[1].set_action('sleep')

                if ghost_fruit_movement[0] == 0 and ghost_fruit_wake_up == True:
                    ghost_fruit[1].set_action('idle')

                if ghost_fruit_movement[0] > 0:
                    ghost_fruit[1].set_flip(False)
                    ghost_fruit[1].set_action('walk')

                if ghost_fruit_movement[0] < 0:
                    ghost_fruit[1].set_flip(True)
                    ghost_fruit[1].set_action('walk')

                collision_types = ghost_fruit[1].move(ghost_fruit_movement, tile_rects)
                if collision_types['bottom'] == True:
                    ghost_fruit[0] = 0

                ghost_fruit[1].change_frame(1)
                ghost_fruit[1].display(display, scroll)

                if player.obj.rect.colliderect(ghost_fruit[1].obj.rect) and player.y < (ghost_fruit[1].y - 35) and pause == False:
                    vertical_momentum = -6
                if player.obj.rect.colliderect(ghost_fruit[1].obj.rect) and player.y > (
                        ghost_fruit[1].y - 35) and player.x < ghost_fruit[1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_left = True
                if player.obj.rect.colliderect(ghost_fruit[1].obj.rect) and player.y > (
                        ghost_fruit[1].y - 35) and player.x > ghost_fruit[1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_right = True

        # jump_corn ---------------------------------------------------- #
        for jump_corn in jump_corns:
            if display_r.colliderect(jump_corn[1].obj.rect):
                jump_corn[0] += 0.2
                if jump_corn[0] > 3:
                    jump_corn[0] = 3
                jump_corn_movement = [0, jump_corn[0]]

                if jump_corn[0] < 0:
                    jump_corn[1].set_action('jump')
                if jump_corn[0] > 1:
                    jump_corn[1].set_action('drop')

                collision_types = jump_corn[1].move(jump_corn_movement, tile_rects)

                if collision_types['bottom'] == True:
                    air_timer_corn = 0
                    jump_corn[0] = 0
                else:
                    air_timer_corn += 1

                if air_timer_corn < 6:
                    jump_corn[0] = -7

                jump_corn[1].change_frame(1)
                jump_corn[1].display(display, scroll)

                if player.obj.rect.colliderect(jump_corn[1].obj.rect) and player.y < (jump_corn[1].y - 35) and pause == False:
                    vertical_momentum = -6
                if player.obj.rect.colliderect(jump_corn[1].obj.rect) and player.y > (
                        jump_corn[1].y - 35) and player.x < jump_corn[1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_left = True
                if player.obj.rect.colliderect(jump_corn[1].obj.rect) and player.y > (
                        jump_corn[1].y - 35) and player.x > jump_corn[1].x and pause == False and damage_moving_left == False and damage_moving_right == False and heart > 0:
                    heart -= 1
                    vertical_momentum = -4
                    damage_moving_right = True

        # death_menu ---------------------------------------------------- #
        death_menu = pygame.Rect(200, 100, 200, 200)
        heart_rect = pygame.Rect(10, 10, 87, 26)
        if heart == 3:
            display.blit(heart3_img, heart_rect)
        if heart == 2:
            display.blit(heart2_img, heart_rect)
        if heart == 1:
            display.blit(heart1_img, heart_rect)
        if heart == 0:
            pause = True
            display.blit(finish_menu_img, death_menu)
            button_1 = pygame.Rect(250, 250, 100, 40)
            display.blit(finish_menu_bar_img, button_1)
            draw_text('Game Over', font, (255, 255, 255), display, 265, 150)
            draw_text('To main menu', font, (255, 255, 255), display, 256, 264)
            if button_1.collidepoint((mx, my)):
                display.blit(finish_menu_bar_collide_img, button_1)
                draw_text('To main menu', font, (255, 255, 255), display, 256, 264)
                if click:
                    running = False

        if heart < 0:
            heart = 0

        # stopwatch ---------------------------------------------------- #
        if pause == False:
            millis = frame_count % 1000
            seconds = int(frame_count / 1000 % 60)
            minutes = int(frame_count / 60000 % 24)
            out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
            font_timer.render_to(display, (460, 30), out, (255, 255, 255))
            frame_count += int(1 / 60 * 1000)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if heart > 0 and pause == False:
                if event.type == KEYDOWN:
                    if event.key == K_d:
                        moving_right = True
                    if event.key == K_a:
                        moving_left = True
                    if event.key == K_SPACE:
                        if air_timer < 6:
                            vertical_momentum = -5
                    if event.key == K_LEFT:
                        attack = True
                    if event.key == K_ESCAPE:
                        running = False
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_LEFT:
                    attack = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)

main_menu()