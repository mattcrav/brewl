from random import randrange
import pygame

WIDTH, HEIGHT = 900, 600 # height/width of the game window
GRID_SIZE = 50 # height/width of a grid box

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
    # initialize client
    window = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Brewl') 
    pygame.font.init()

    # resize background image
    bkgrnd = pygame.image.load('background.jpg')
    bkgrnd = pygame.transform.scale(bkgrnd, (WIDTH, HEIGHT))

    recipe = [
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W']
    ]

    type_color = {
        'H': COLOR_DARK_GREEN, # Hops
        'W': COLOR_BLUE, # Water
        'Y': COLOR_WHITE, # Yeast
        'M': COLOR_YELLOW # Malt
    }

    # start update loop
    running = True
    while running:
        # get events
        events = pygame.event.get()
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # draw background
        window.blit(bkgrnd, [0,0])

        # draw and color grid boxes based on recipe
        start = [(WIDTH / 2) - GRID_SIZE * 3, (HEIGHT / 2) - GRID_SIZE * 3]
        pos = [0, 0]
        for x in range(6):
            pos[0] = start[0]
            pos[1] = start[1] + GRID_SIZE * x
            for y in range(6):
                pos[0] = start[0] + GRID_SIZE * y
                pygame.draw.rect(window, type_color[recipe[x][y]], pos + [GRID_SIZE, GRID_SIZE])

        # draw grid lines
        for l in range(7):
            pos[0] = start[0]
            pos[1] = start[1] + GRID_SIZE * l
            pygame.draw.line(window, COLOR_BLACK, pos, [pos[0] + GRID_SIZE * 6, pos[1]])
            pos[0] = start[0] + GRID_SIZE * l
            pos[1] = start[1]
            pygame.draw.line(window, COLOR_BLACK, pos, [pos[0], pos[1] + GRID_SIZE * 6])
        
        # write column headers centered on each zone
        font = pygame.font.SysFont('Algerian', 18)
        headers = ['      Mash', '      Boil', '      Ferm']
        x = 0
        for h in headers:
            render = font.render(h, False, COLOR_WHITE)
            pos[0] = start[0] + GRID_SIZE * x
            pos[1] = start[1] - GRID_SIZE / 2
            window.blit(render, pos)
            x += 2

        # update display
        pygame.display.update()