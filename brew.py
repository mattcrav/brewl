from random import randrange
import pygame

WIDTH, HEIGHT = 900, 600 # height/width of the game window
GRID_SIZE = 50 # height/width of a grid box
DIE_SIZE = 25 # height/width of dice

COLOR_GREY = [150, 150, 150]
COLOR_RED = [225, 0, 0]
COLOR_GREEN = [0, 225, 0]
COLOR_BLUE = [0, 0, 225]
COLOR_DARK_GREEN = [40, 84, 27]
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [225, 225, 225]
COLOR_YELLOW = [225, 225, 0]
COLOR_BROWN = [139, 69, 19]

TYPE_COLOR = {
        'H': COLOR_DARK_GREEN, # Hops
        'W': COLOR_BLUE, # Water
        'Y': COLOR_WHITE, # Yeast
        'M': COLOR_YELLOW # Malt
    }


class Die:
    def __init__(self, type) -> None:
        self.rect = None
        self.value = 0
        self.size = 6
        self.type = type
        self.color = None
        self.roll()

    def roll(self):
        self.value = randrange(self.size) + 1
        return self.value
    

class DicePool:
    def __init__(self) -> None:
        self.pool = [None, None, None]
        for x in range(3):
            self.pool[x] = Die('H')
            self.pool[x].color = TYPE_COLOR[self.pool[x].type]

    def collidepoint(self, pos):
        for d in self.pool:
            if d.rect.collidepoint(pos):
                return d
        return None
    

class GridBox:
    def __init__(self, type) -> None:
        self.rect = None
        self.value = 0
        self.type = type
        self.color = None


class Grid:
    def __init__(self, recipe) -> None:
        self.grid = [
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None]
        ]
        for x in range(6):
            for y in range(6):
                self.grid[y][x] = GridBox(recipe[y][x])
                self.grid[y][x].color = TYPE_COLOR[recipe[y][x]]

    def get(self, x, y):
        return self.grid[y][x]
    
    def collidepoint(self, pos):
        for y in self.grid:
            for x in y:
                if x.rect.collidepoint(pos):
                    return x
        return None


if __name__ == '__main__':
    # initialize client
    window = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Brewl') 

    # initialize fonts
    pygame.font.init()
    font = pygame.font.SysFont('Algerian', 18)
    font2 = pygame.font.SysFont('Algerian', 12)

    # resize background image
    bkgrnd = pygame.image.load('background.jpg')
    bkgrnd = pygame.transform.scale(bkgrnd, (WIDTH, HEIGHT))

    # initialize grid
    recipe = [
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['M', 'M', 'H', 'H', 'Y', 'Y'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W'],
        ['M', 'M', 'H', 'H', 'W', 'W']
    ]
    grid = Grid(recipe)

    # initialize dice
    dice = DicePool()

    # start update loop
    running = True
    while running:

        # get events
        events = pygame.event.get()
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                g = grid.collidepoint(pos)
                p = dice.collidepoint(pos)
            if event.type == pygame.MOUSEBUTTONUP:
                g2 = grid.collidepoint(pos)
                p2 = dice.collidepoint(pos)
                # if button down hits a box and up occurs in same box 
                if g is not None and g == g2:
                    g.value += 1
                if p is not None and p == p2:
                    p.roll()

        # draw background
        window.blit(bkgrnd, [0,0])

        # draw grid boxes starting with the upper left
        upr_left = pygame.Rect([(WIDTH // 2) - GRID_SIZE * 3, (HEIGHT // 2) - GRID_SIZE * 3, GRID_SIZE, GRID_SIZE])
        for x in range(6):
            for y in range(6):
                r = upr_left.move(x * GRID_SIZE, y * GRID_SIZE)
                grid.get(x, y).rect = r
                pygame.draw.rect(window, grid.get(x, y).color, r)
                render = font.render(str(grid.get(x, y).value), True, COLOR_BLACK)
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

        # draw dice
        x = 1
        for d in dice.pool:
            r = pygame.Rect((grid.get(0, 5).rect[0] + GRID_SIZE * x - DIE_SIZE // 2, grid.get(0, 5).rect[1] + GRID_SIZE * 2, DIE_SIZE, DIE_SIZE))
            d.rect = r
            pygame.draw.rect(window, d.color, r)
            pygame.draw.rect(window, COLOR_BLACK, r, 1)
            render = font.render(str(d.value), True, COLOR_BLACK)
            tr = render.get_rect(center=r.center)
            window.blit(render, tr)
            x += 2

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