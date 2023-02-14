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

    # initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Algerian', 18)

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

        # draw grid boxes starting with the upper left
        upr_left = pygame.Rect([(WIDTH // 2) - GRID_SIZE * 3, (HEIGHT // 2) - GRID_SIZE * 3, GRID_SIZE, GRID_SIZE])
        for x in range(6):
            for y in range(6):
                r = upr_left.move(x * GRID_SIZE, y * GRID_SIZE)
                pygame.draw.rect(window, type_color[recipe[y][x]], r)
                render = font.render('0', True, COLOR_BLACK)
                tr = render.get_rect(center=r.center)
                window.blit(render, tr)

        # draw grid lines
        for l in range(7):
            # horizontal
            start = [upr_left[0], upr_left[1] + GRID_SIZE * l]
            end = [start[0] + GRID_SIZE * 6, start[1]]
            pygame.draw.line(window, COLOR_BLACK, start, end)
            # vertical
            start = [upr_left[0] + GRID_SIZE * l, upr_left[1]]
            end = [start[0], start[1] + GRID_SIZE * 6]
            pygame.draw.line(window, COLOR_BLACK, start, end)
        
        # write column headers centered on each zone
        headers = ['Mash', 'Boil', 'Ferment']
        x = 1
        for h in headers:
            render = font.render(h, True, COLOR_WHITE)
            r = render.get_rect(center=(upr_left[0] + GRID_SIZE * x, upr_left[1] - GRID_SIZE // 2))
            window.blit(render, r)
            x += 2

        # update display
        pygame.display.update()