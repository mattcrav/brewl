from random import randrange
import pygame

WIDTH, HEIGHT = 900, 500

COLOR_GREY = [150, 150, 150]
COLOR_RED = [225, 0, 0]
COLOR_GREEN = [0, 225, 0]
COLOR_BLUE = [0, 0, 225]
COLOR_DARK_GREEN = [40, 84, 27]
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [225, 225, 225]
COLOR_YELLOW = [225, 225, 0]
COLOR_BROWN = [139, 69, 19]

class Die:
    def __init__(self) -> None:
        self.size = 6
        self.type = 'Hops'
        self.value = None

    def roll(self):
        self.value = randrange(self.size) + 1
        return self.value


if __name__ == '__main__':
    window = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Brewl') 
    pygame.font.init()

    recipe = [
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W']
    ]

    running = True
    while running:
        events = pygame.event.get()
        # pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # draw grid
        s = 50
        start = [(WIDTH / 2) - s*3, (HEIGHT / 2) - s*3]
        pos = [0, 0]
        for x in range(6):
            pos[0] = start[0]
            pos[1] = start[1] + x*s
            for y in range(6):
                pos[0] = start[0] + y*s
                if recipe[x][y] == 'H':
                    color = COLOR_DARK_GREEN
                if recipe[x][y] == 'M':
                    color = COLOR_YELLOW
                if recipe[x][y] == 'W':
                    color = COLOR_BLUE
                if recipe[x][y] == 'Y':
                    color = COLOR_WHITE
                pygame.draw.rect(window, color, pos + [s, s])
        for x in range(6):
            pos[0] = start[0]
            pos[1] = start[1] + x*s
            pygame.draw.line(window, COLOR_BLACK, pos, [pos[0] + 6*s, pos[1]])
            pos[0] = start[0] + x*s
            pos[1] = start[1]
            pygame.draw.line(window, COLOR_BLACK, pos, [pos[0], pos[1] + 6*s])
        
        # column headers
        font = pygame.font.SysFont('Algerian', 18)
        headers = ['      Mash      ', '      Boil      ', '      Ferm      ']
        x = 0
        for h in headers:
            render = font.render(h, False, COLOR_WHITE)
            pos[0] = start[0] + x*s
            pos[1] = start[1] - s/2
            window.blit(render, pos)
            x += 2

        pygame.display.update()