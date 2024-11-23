import random

import pygame


class Car:
    def __init__(self, model: pygame.Surface, pos: tuple[float, float]) -> None:
        self.model = model
        self.model_rect = model.get_rect(center=pos)


    def check_collision(self, car: pygame.Surface) -> bool: # Is_crashed типа
        return self.model_rect.colliderect(car)


    def __call__(self, sc: pygame.Surface, speed: float):
        self.model_rect.y += speed
        sc.blit(
            source=self.model,
            dest=self.model_rect
        )


class BotCars:
    def __init__(self, cars: list[Car]) -> None:
        self.cars = cars
        
    
    def check_cols(self, player_car: Car) -> bool: # True, если врезались
        for car in self.cars:
            if player_car.check_collision(car.model_rect):
                return True

        return False
    
    
    def __correction_cords(self, car: Car, height: float) -> None:
        if car.model_rect.y > height:
            car.model_rect.y = random.randint(-1000, -500)
    
    
    def __call__(self, sc: pygame.Surface, speed: float) -> None:
        for car in self.cars:
            car.model_rect.y += speed
            self.__correction_cords(
                car=car,
                height=sc.get_height()
            )
            sc.blit(
                source=car.model,
                dest=car.model_rect
            )