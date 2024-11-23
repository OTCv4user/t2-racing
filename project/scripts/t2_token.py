import random

import pygame

from scripts.cars import Car


class Token:
    def __init__(self, model: pygame.Surface, x_cords: list):
        self.model = model
        self.model_rect = model.get_rect(
            center=(
                0, 0
            )
        )
        self.x_cords = x_cords
        self.__spawn_token()
        
    
    def __spawn_token(self) -> None:
        self.model_rect.center = (
            random.choice(self.x_cords), random.randint(-2000, -1000)
        )
    
    
    def __correction_cords(self, height: float) -> None:
        if self.model_rect.y > height:
            self.__spawn_token()
    
    
    def __call__(self, sc: pygame.Surface, player_car: Car, speed: float) -> bool: # Подобрал или нет, респавн токена
        self.__correction_cords(sc.get_height())
        self.model_rect.y += speed
        sc.blit(
            source=self.model,
            dest=self.model_rect
        )
        is_taken = self.model_rect.colliderect(player_car.model_rect)
        if is_taken:
            self.__spawn_token()
        return is_taken