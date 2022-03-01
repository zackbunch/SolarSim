import pygame
from planet_class import Sun, Earth, Mars, Mercury, Venus

pygame.init()

WIDTH, HEIGHT = 800, 800
FONT = pygame.font.SysFont("comicsans", 16)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)




def main():
    run = True
    clock = pygame.time.Clock()

    sun = Sun()
    earth = Earth()
    mars = Mars()
    mercury =Mercury()
    venus = Venus()
    sun.sun = True
    
    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()