import pygame

"""
Умные мысли преследуют меня, но я быстрее...
"""


class RoadSystem:
    def __init__(self, asphalt: pygame.Surface, roadside: pygame.Surface, width: float, center_x: float) -> None:
        self.asphalt = None
        self.roadside = None

        self.scale = self.__calculate_scale(asphalt, roadside, width)
        self.road = self.__generate_road(asphalt, roadside, width)
        self.road_rect1 = self.road.get_rect(center=(center_x, 0))
        self.road_rect2 = self.road.get_rect(center=(center_x, -self.road.get_height()))  # Вторая дорога ниже первой


    def __calculate_scale(self, asphalt: pygame.Surface, roadside: pygame.Surface, width: float) -> float:
        road_width = (
            roadside.get_width() * 2 +
            (asphalt.get_width() * 2) * 2 # Почему не * 4? - Так логически правильнее, я половину пути движения
        )
        return width / road_width


    def __blit_surfaces(self,
                        surf: pygame.Surface,
                        asphalt: pygame.Surface,
                        roadside: pygame.Surface,
                        asphalt_inverted: pygame.Surface,
                        roadside_inverted: pygame.Surface,
                        y: float) -> pygame.Surface:

        offset = 0

        surf.blit(
            source=roadside_inverted,
            dest=(offset, y)
        )
        offset += roadside.get_width()

        surf.blit(
            source=asphalt,
            dest=(offset, y)
        )
        offset += asphalt.get_width()

        surf.blit(
            source=asphalt_inverted,
            dest=(offset, y)
        )
        offset += asphalt.get_width()

        surf.blit(
            source=asphalt,
            dest=(offset, y)
        )
        offset += asphalt.get_width()

        surf.blit(
            source=asphalt_inverted,
            dest=(offset, y)
        )
        offset += asphalt.get_width()

        surf.blit(
            source=roadside,
            dest=(offset, y)
        )

        return surf


    def __generate_road(self, asphalt: pygame.Surface, roadside: pygame.Surface, width: float) -> pygame.surface:
        asphalt = pygame.transform.scale(
            surface=asphalt,
            size=(asphalt.get_width() * self.scale, asphalt.get_height() * self.scale)
        )
        roadside = pygame.transform.scale(
            surface=roadside,
            size=(roadside.get_width() * self.scale, roadside.get_height() * self.scale)
        )

        asphalt_inverted = pygame.transform.flip(
            surface=asphalt,
            flip_x=True,
            flip_y=False
        )
        roadside_inverted = pygame.transform.flip(
            surface=roadside,
            flip_x=True,
            flip_y=False
        )

        surf = pygame.Surface(
            size=(width, asphalt.get_height() * 2),
            flags=pygame.SRCALPHA
        )
        surf.fill((0, 0, 0, 0))

        #############################
        surf = self.__blit_surfaces(
            surf=surf,
            asphalt=asphalt,
            roadside=roadside,
            asphalt_inverted=asphalt_inverted,
            roadside_inverted=roadside_inverted,
            y=0
        )

        surf = self.__blit_surfaces(
            surf=surf,
            asphalt=asphalt,
            roadside=roadside,
            asphalt_inverted=asphalt_inverted,
            roadside_inverted=roadside_inverted,
            y=surf.get_height() / 2
        )

        self.asphalt = asphalt
        self.roadside = roadside

        return surf


    def calculate_x(self) -> list:
        asphalt = self.asphalt.get_width()
        roadside = self.roadside.get_width()

        base = roadside + asphalt / 2

        return [base + asphalt * x for x in range(4)]


    def __call__(self, sc: pygame.Surface, speed: float) -> None:
        self.road_rect1.y += speed
        self.road_rect2.y += speed

        if self.road_rect1.y >= sc.get_height():
            self.road_rect1.y = self.road_rect2.y - self.road.get_height()

        if self.road_rect2.y >= sc.get_height():
            self.road_rect2.y = self.road_rect1.y - self.road.get_height()

        sc.blit(self.road, self.road_rect1)
        sc.blit(self.road, self.road_rect2)