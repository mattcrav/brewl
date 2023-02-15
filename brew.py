from random import randrange, shuffle
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
        'M': COLOR_YELLOW, # Malt
        'O': COLOR_RED # Off Flavor
    }


class Die:
    def __init__(self, type) -> None:
        self.rect = None
        self.value = 0
        self.size = 6
        self.type = type
        self.color = None

    def roll(self):
        self.value = randrange(self.size) + 1
        return self.value
    

class DicePool:
    def __init__(self) -> None:
        self.pool = []
        self.selected = None
        hops1 = [Die('H'), Die('H'), Die('O'), Die('O')]
        hops2 = [Die('H'), Die('H'), Die('O'), Die('O')]
        malt1 = [Die('M'), Die('M'), Die('O'), Die('O')]
        malt2 = [Die('M'), Die('M'), Die('O'), Die('O')]
        yeast = [Die('Y'), Die('Y'), Die('O'), Die('O')]
        ingredients = hops1 + hops2 + malt1 + malt2 + yeast
        for i in ingredients:
            i.color = TYPE_COLOR[i.type]
            self.pool.append(i)
        for x in range(36 - len(ingredients)):
            d = Die('W')
            d.color = TYPE_COLOR[d.type]
            self.pool.append(d)
        self.shuffle()
        self.active = self.pool[:3]

    def shuffle(self):
        for d in self.pool:
            d.roll()
        shuffle(self.pool)

    def collidepoint(self, pos):
        for d in self.active:
            if d.rect.collidepoint(pos):
                return d
        return None
    

class GridBox:
    def __init__(self, type, x, y) -> None:
        self.x = x
        self.y = y
        self.rect = None
        self.value = 0
        self.type = type
        self.color = None
        self.die = None

    def get_val(self):
        self.value = 0
        if self.die is not None:
            if self.die.type == self.type:
                self.value = self.die.value
            if self.die.type == 'O' and self.type == 'W':
                self.value = -self.die.value
        return self.value


class Grid:
    def __init__(self, recipe) -> None:
        self.active = 0
        self.active_cnt = 0
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
                self.grid[y][x] = GridBox(recipe[y][x], x, y)
                self.grid[y][x].color = TYPE_COLOR[recipe[y][x]]

    def get(self, x, y):
        return self.grid[y][x]

    def score(self, row=None):
        if row is not None:
            return sum([x.get_val() for x in self.grid[row]])
        else:
            val = 0
            for x in range(6):
                val += self.score(x)
            return val

    def collidepoint(self, pos):
        for y in self.grid:
            for x in y:
                if x.rect.collidepoint(pos):
                    return x
        return None


class Screen:
    def __init__(self) -> None:
        recipe = [
            ['M', 'M', 'H', 'H', 'Y', 'Y'],
            ['M', 'M', 'H', 'H', 'Y', 'Y'],
            ['W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W'],
            ['M', 'M', 'H', 'H', 'W', 'W'],
            ['M', 'M', 'H', 'H', 'W', 'W']
        ]
        self.grid = Grid(recipe)
        self.dice = DicePool()
        self.endturn = None
        self.clicked = None
        self.played = False

    def write_text(self, text, rect, color, font):
        render = font.render(text, True, color)
        tr = render.get_rect(center=rect.center)
        return (render, tr)
        
    def get_click(self, pos):
        c = None
        if self.endturn.collidepoint(pos):
            c = self.endturn
        g = self.grid.collidepoint(pos)
        if g is not None:
            c = g
        p = self.dice.collidepoint(pos)
        if p is not None:
            c = p
        if c is not None and self.clicked == c:
            self.clicked = None
            return c
        else:
            self.clicked = c

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

    # initialize screen
    scrn = Screen()

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
                scrn.get_click(pos)
            if event.type == pygame.MOUSEBUTTONUP:
                o = scrn.get_click(pos)
                if isinstance(o, GridBox):
                    if o.die is None and scrn.dice.selected is not None and scrn.grid.active == o.x:
                        o.die = scrn.dice.selected
                        scrn.played = True
                        scrn.dice.selected = None
                        scrn.dice.pool.remove(o.die)
                        scrn.dice.active.remove(o.die)
                        if len(scrn.dice.active) == 0:
                            o = scrn.endturn
                        scrn.grid.active_cnt += 1
                        if scrn.grid.active_cnt == 6:
                            scrn.grid.active_cnt = 0
                            scrn.grid.active += 1
                if isinstance(o, Die):
                    scrn.dice.selected = o
                if o == scrn.endturn and scrn.played:
                    scrn.played = False
                    scrn.dice.shuffle()
                    scrn.dice.active = scrn.dice.pool[:3]

        # draw background
        window.blit(bkgrnd, [0,0])

        # get location of upper left box, centering grid in window
        upr_left = pygame.Rect([(WIDTH // 2) - GRID_SIZE * 3, (HEIGHT // 2) - GRID_SIZE * 3, GRID_SIZE, GRID_SIZE])

        for x in range(6):
            # draw scoring column
            window.blit(*scrn.write_text(str(scrn.grid.score(x)), upr_left.move(-int(GRID_SIZE * 1.5), x * GRID_SIZE), COLOR_WHITE, font))

            for y in range(6):
                # draw grid box
                r = upr_left.move(x * GRID_SIZE, y * GRID_SIZE)
                scrn.grid.get(x, y).rect = r
                pygame.draw.rect(window, scrn.grid.get(x, y).color, r)

                # draw score in upper left
                if x == scrn.grid.active and scrn.grid.get(x, y).die is None:
                    c = COLOR_RED
                else:
                    c = COLOR_BLACK
                render = font2.render(str(scrn.grid.get(x, y).get_val()), True, c)
                window.blit(render, r.move(5,0))

                # draw die in box
                if scrn.grid.get(x, y).die is not None:
                    r = r.inflate(-DIE_SIZE, -DIE_SIZE)
                    pygame.draw.rect(window, scrn.grid.get(x, y).die.color, r)
                    pygame.draw.rect(window, COLOR_BLACK, r, 1)
                    window.blit(*scrn.write_text(str(scrn.grid.get(x, y).die.value), r, COLOR_BLACK, font))

        # draw score total
        start = [upr_left[0] - int(GRID_SIZE * 1.5), upr_left[1] + GRID_SIZE * 6]
        end = [upr_left[0] - int(GRID_SIZE * 0.5), upr_left[1] + GRID_SIZE * 6]
        pygame.draw.line(window, COLOR_WHITE, start, end)
        window.blit(*scrn.write_text(str(scrn.grid.score()), upr_left.move(-int(GRID_SIZE * 1.5), 6 * GRID_SIZE), COLOR_WHITE, font))

        # draw grid lines
        for l in range(7):
            # horizontal
            start = [upr_left[0], upr_left[1] + GRID_SIZE * l]
            end = [start[0] + GRID_SIZE * 6, start[1]]
            if l == 0 or l == 6:
                w = 5
            else:
                w = 1
            pygame.draw.line(window, COLOR_BLACK, start, end, w)
            # vertical
            start = [upr_left[0] + GRID_SIZE * l, upr_left[1]]
            end = [start[0], start[1] + GRID_SIZE * 6]
            if l % 2 == 0:
                w = 5
            else:
                w = 1
            pygame.draw.line(window, COLOR_BLACK, start, end, w)

        # draw dice
        x = 1
        for d in scrn.dice.active:
            r = pygame.Rect((scrn.grid.get(0, 5).rect[0] + GRID_SIZE * x - DIE_SIZE // 2, scrn.grid.get(0, 5).rect[1] + GRID_SIZE * 2, DIE_SIZE, DIE_SIZE))
            d.rect = r
            pygame.draw.rect(window, d.color, r)
            pygame.draw.rect(window, COLOR_BLACK, r, 1)
            window.blit(*scrn.write_text(str(d.value), r, COLOR_BLACK, font))
            x += 2

        # write column headers centered on each zone
        headers = ['Score', 'Mash', 'Boil', 'Ferment']
        x = -1
        for h in headers:
            render = font.render(h, True, COLOR_WHITE)
            r = render.get_rect(center=(upr_left[0] + GRID_SIZE * x, upr_left[1] - GRID_SIZE // 2))
            window.blit(render, r)
            x += 2

        # draw end turn button
        scrn.endturn = pygame.Rect(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE, DIE_SIZE)
        pygame.draw.rect(window, COLOR_GREEN, scrn.endturn)
        pygame.draw.rect(window, COLOR_BLACK, scrn.endturn, 1)
        window.blit(*scrn.write_text('End', scrn.endturn, COLOR_BLACK, font2))

        # update display
        pygame.display.update()