import os
import sys
import random

import pygame
import win32api

from scripts.constants import (
    DISPLAY_SIZE, TICKRATE, PRESSED_SCALE,
    STEERING_SPEED, USEREVENT1_SEC, CAR_SCALE
)
from scripts.surfaces_buffer import SurfBuffer
from scripts.button import Button
from scripts.road import RoadSystem
from scripts.cars import Car, BotCars
from scripts.t2_token import Token


def exit(*args) -> None:
    pygame.quit()
    sys.exit(0)


def game(sc: pygame.Surface, clock: pygame.time.Clock) -> object:
    speed = 5
    score = 0
    t2_coins = 0
    
    
    road = RoadSystem(
        asphalt=surfaces('asphalt'),
        roadside=surfaces('roadside'),
        width=sc.get_width() * 0.9,
        center_x=sc.get_width() / 2

    )
    x_cords = road.calculate_x(sc.get_width())
    x_edges = road.get_x_edges()
    
    model = surfaces(
        'cybertruck'
    )
    scale = road.scale

    player_car = Car(
        model=pygame.transform.scale(
            surface=model,
            size=(model.get_width() * (scale * CAR_SCALE), model.get_height() * (scale * CAR_SCALE))
        ),
        pos=(sc.get_width() / 2, sc.get_height() * .8)
    ) # 3 часа ночи, хочу спать...
    
    bots = BotCars(
        [
            Car(
                model=pygame.transform.scale(
                    surface=model,
                    size=(model.get_width() * (scale * CAR_SCALE), model.get_height() * (scale * CAR_SCALE)) # Делаю модельки ботов чуть меньше игрока
                ),
                pos=(x, random.randint(-3000, -500))) for x in x_cords
        ]
    )
    
    token_model = surfaces(
        'token'
    )
    
    token = Token(
        model=pygame.transform.scale(
            surface=token_model,
            size=(token_model.get_width() * scale, token_model.get_height() * scale)
        ),
        x_cords=x_cords
    )

    while True:
        sc.fill((255, 255, 255))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        btns = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'Score: {score // 100}, Tokens: {t2_coins}  -- Начислим юзеру столько мегабайт, собранные токены')
                return main_menu
            if event.type == pygame.USEREVENT:
                speed += 1

        if player_car.model_rect.x > x_edges[0]:
            if keys[pygame.K_a]:
                player_car.model_rect.x -= STEERING_SPEED
        
        if player_car.model_rect.x < x_edges[1]:
            if keys[pygame.K_d]:
                player_car.model_rect.x += STEERING_SPEED
        print(player_car.model_rect.right, x_edges[1])
        if btns[0]:
            if mouse_x < sc.get_width() / 2:
                if player_car.model_rect.x > x_edges[0]:
                    player_car.model_rect.x -= STEERING_SPEED
            else:
                if player_car.model_rect.x < x_edges[1]:
                    player_car.model_rect.x += STEERING_SPEED

        road(
            sc=sc,
            speed=speed
        )
        score += speed
        bots(
            sc=sc,
            speed=speed
        )
        player_car(
            sc=sc,
            speed=0
        )
        '''
        for i in x_cords:
            pygame.draw.circle(sc, (255, 0, 0), (i, sc.get_height() / 2), 5)
        '''
        if bots.check_cols(player_car=player_car):
            print(f'Score: {score // 100}, Tokens: {t2_coins}  -- Начислим юзеру столько мегабайт, собранные токены')
            return main_menu
        
        t2_coins += token(sc, player_car, speed)
        
        pygame.display.update()
        clock.tick(TICKRATE)

    
def main_menu(sc: pygame.Surface, clock: pygame.time.Clock) -> object:
    background = surfaces(
        'main'
    )
    background = pygame.transform.scale(
        surface=background,
        size=(sc.get_width(), sc.get_height())
    )

    start_unpressed = surfaces(
        key='start_unpressed'
    )
    start_pressed = surfaces(
        key='start_pressed'
    )
    scale = (sc.get_width() / start_unpressed.get_width()) * 0.9

    start_unpressed = surfaces(
        key='start_unpressed',
        scale=scale
    )
    start_pressed = surfaces(
        key='start_pressed',
        scale=scale
    )

    start_button = Button(
        surface=sc,
        surf_unpressed=start_unpressed,
        surf_pressed=start_pressed,
        pressed_scale=PRESSED_SCALE,
        offset=(0, 0),
        position=(sc.get_width() / 2, sc.get_height() - start_unpressed.get_height()),
        on_click=game
    )

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        btns = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return exit

        sc.blit(
            source=background,
            dest=(0, 0)
        )

        func = start_button(
            pos=(mouse_x, mouse_y),
            lkm_pressed=btns[0]
        )
        if func:
            return func


        pygame.display.update()
        clock.tick(TICKRATE)

        
def main():
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, USEREVENT1_SEC * 1000)
    
    scale = (win32api.GetSystemMetrics(1) / DISPLAY_SIZE[1]) - 0.05 # Pseudo-emulation phone
    display_size = tuple(map(lambda e: e * scale, DISPLAY_SIZE))
    print(display_size)

    sc = pygame.display.set_mode(display_size)
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('T2 Racing')
    pygame.display.set_icon(surfaces('t2_racing'))
    
    function_buffer = main_menu
    while True:
        function_buffer = function_buffer(sc, clock)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    surfaces = SurfBuffer()
    main()