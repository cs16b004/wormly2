# Extension of worm_1y (a Nibbles clone)
# By Ayush Jain
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD_1 = 0 # syntactic sugar: index of the worm_1's head
HEAD_2 = 0
def get_hole():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
def reset():
    return random.randint(50,150)
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('wormy2.0')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx_1 = random.randint(5, CELLWIDTH - 6)
    starty_1 = random.randint(5, CELLHEIGHT - 6)

    startx_2 = random.randint(5, CELLWIDTH - 6)
    starty_2 = random.randint(5, CELLHEIGHT - 6)
    worm_1Coords = [{'x': startx_1,     'y': starty_1},
                  {'x': startx_1 - 1, 'y': starty_1},
                  {'x': startx_1 - 2, 'y': starty_1}]
    worm_2Coords = [{'x': startx_2,     'y': starty_2},
                  {'x': startx_2 - 1, 'y': starty_2},
                  {'x': startx_2 - 2, 'y': starty_2}]

    direction1 = RIGHT
    direction2 = RIGHT
    # Start the apple in a random place.
    apple = getRandomLocation()
    hole = get_hole()
    hole_timer = random.randint(50,150)
    while True: # main game loop
        hole_timer -= 1

        if hole_timer ==0:
            hole = get_hole()
            hole_timer = reset()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction1 != RIGHT:
                    direction1 = LEFT
                elif (event.key == K_RIGHT) and direction1 != LEFT:
                    direction1 = RIGHT
                elif (event.key == K_UP) and direction1 != DOWN:
                    direction1 = UP
                elif (event.key == K_DOWN) and direction1 != UP:
                    direction1 = DOWN
                elif (event.key == K_a) and direction2 != RIGHT:
                    direction2 = LEFT
                elif (event.key == K_d) and direction1 != LEFT:
                    direction2 = RIGHT
                elif (event.key == K_w) and direction2 != DOWN:
                    direction2 = UP
                elif (event.key == K_s) and direction2 != UP:
                    direction2 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm_1 has hit itself or the edge
        if worm_1Coords[HEAD_1]['x'] == -1:
            #print(worm_1Coords[HEAD]['x'])
            worm_1Coords[HEAD_1]['x'] = worm_1Coords[HEAD_1]['x']%CELLWIDTH
            #print(worm_1Coords[HEAD]['x'])
        if worm_1Coords[HEAD_1]['x'] == CELLWIDTH:
            #print(worm_1Coords[HEAD]['x'])
            worm_1Coords[HEAD_1]['x'] = worm_1Coords[HEAD_1]['x']%CELLWIDTH
        if worm_1Coords[HEAD_1]['y'] == -1:
            #print(worm_1Coords[HEAD]['y'])
            worm_1Coords[HEAD_1]['y'] = worm_1Coords[HEAD_1]['y']%CELLHEIGHT
        if worm_1Coords[HEAD_1]['y'] == CELLHEIGHT:
            #print(worm_1Coords[HEAD]['y'])
            worm_1Coords[HEAD_1]['y'] = worm_1Coords[HEAD_1]['y'] % CELLHEIGHT

        for worm_1Body in worm_1Coords[1:]:
            if worm_1Body['x'] == worm_1Coords[HEAD_1]['x'] and worm_1Body['y'] == worm_1Coords[HEAD_1]['y']%CELLHEIGHT:
                print("here")
                return # game over

        # check if worm_1 has eaten an apply
        if worm_1Coords[HEAD_1]['x'] == apple['x'] and worm_1Coords[HEAD_1]['y'] == apple['y']:
            # don't remove worm_1's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        elif worm_1Coords[HEAD_1]['x'] == hole['x'] and worm_1Coords[HEAD_1]['y'] == hole['y']:
            worm_1Coords[HEAD_1]['x'] = random.randint(5, CELLWIDTH - 6)
            worm_1Coords[HEAD_1]['y'] = random.randint(5, CELLHEIGHT - 6)
        else:
            del worm_1Coords[-1] # remove worm_1's tail segment
        #print(HEAD_2)
        #print(worm_2Coords,HEAD_2)
        # Worm1 eats worm2
        for worm_2Body in worm_2Coords[1:]:
            if worm_2Body['x'] == worm_1Coords[HEAD_1]['x'] and worm_2Body['y'] == worm_1Coords[HEAD_1]['y']%CELLHEIGHT:
                #print("here")
                if worm_2Coords:
                    del worm_2Coords[-1]
                else:
                    return
        if worm_2Coords[HEAD_2]['x'] == -1:
            #print(worm_2Coords[HEAD]['x'])
            worm_2Coords[HEAD_2]['x'] = worm_2Coords[HEAD_2]['x']%CELLWIDTH
            #print(worm_2Coords[HEAD]['x'])
        if worm_2Coords[HEAD_2]['x'] == CELLWIDTH:
            #print(worm_2Coords[HEAD]['x'])
            worm_2Coords[HEAD_2]['x'] = worm_2Coords[HEAD_2]['x']%CELLWIDTH
        if worm_2Coords[HEAD_2]['y'] == -1:
            #print(worm_2Coords[HEAD]['y'])
            worm_2Coords[HEAD_2]['y'] = worm_2Coords[HEAD_2]['y']%CELLHEIGHT
        if worm_2Coords[HEAD_2]['y'] == CELLHEIGHT:
            #print(worm_2Coords[HEAD]['y'])
            worm_2Coords[HEAD_2]['y'] = worm_2Coords[HEAD_2]['y'] % CELLHEIGHT

        for worm_2Body in worm_2Coords[1:]:
            if worm_2Body['x'] == worm_2Coords[HEAD_2]['x'] and worm_2Body['y'] == worm_2Coords[HEAD_2]['y']%CELLHEIGHT:
                #print("here")
                return # game over

        # check if worm_2 has eaten an apply
        if worm_2Coords[HEAD_2]['x'] == apple['x'] and worm_2Coords[HEAD_2]['y'] == apple['y']:
            # don't remove worm_2's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        elif worm_2Coords[HEAD_2]['x'] == hole['x'] and worm_2Coords[HEAD_2]['y'] == hole['y']:
            worm_2Coords[HEAD_2]['x'] = random.randint(5, CELLWIDTH - 6)
            worm_2Coords[HEAD_2]['y'] = random.randint(5, CELLHEIGHT - 6)
        else:
            #print("lili")
            del worm_2Coords[-1] # remove worm_2's tail segment
        #Check if worm2 eats worm1 (decrement points)
        for worm_1Body in worm_1Coords[1:]:
            if worm_1Body['x'] == worm_2Coords[HEAD_2]['x'] and worm_1Body['y'] == worm_2Coords[HEAD_2]['y']%CELLHEIGHT:
                #print("here")
                if worm_1Coords:
                    del worm_1Coords[-1]
                else:
                    return

        # move the worm_1 by adding a segment in the direction1 it is moving
        if direction1 == UP:
            newHead = {'x': worm_1Coords[HEAD_1]['x'], 'y': worm_1Coords[HEAD_1]['y'] - 1}
        elif direction1 == DOWN:
            newHead = {'x': worm_1Coords[HEAD_1]['x'], 'y': worm_1Coords[HEAD_1]['y'] + 1}
        elif direction1 == LEFT:
            newHead = {'x': worm_1Coords[HEAD_1]['x'] - 1, 'y': worm_1Coords[HEAD_1]['y']}
        elif direction1 == RIGHT:
            newHead = {'x': worm_1Coords[HEAD_1]['x'] + 1, 'y': worm_1Coords[HEAD_1]['y']}

        if direction2 == UP:
            newHead2 = {'x': worm_2Coords[HEAD_2]['x'], 'y': worm_2Coords[HEAD_2]['y'] - 1}
        elif direction2 == DOWN:
            newHead2 = {'x': worm_2Coords[HEAD_2]['x'], 'y': worm_2Coords[HEAD_2]['y'] + 1}
        elif direction2 == LEFT:
            newHead2 = {'x': worm_2Coords[HEAD_2]['x'] - 1, 'y': worm_2Coords[HEAD_2]['y']}
        elif direction2 == RIGHT:
            newHead2 = {'x': worm_2Coords[HEAD_2]['x'] + 1, 'y': worm_2Coords[HEAD_2]['y']}



        worm_1Coords.insert(0, newHead)
        worm_2Coords.insert(0,newHead2)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawworm_1(worm_1Coords)
        drawworm_2(worm_2Coords)
        drawApple(apple)
        drawHole(hole)
        drawScore(len(worm_1Coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('2.0!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawworm_1(worm_1Coords):
    for coord in worm_1Coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        worm_1SegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, worm_1SegmentRect)
        worm_1InnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, worm_1InnerSegmentRect)

def drawworm_2(worm_1Coords):
    for coord in worm_1Coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        worm_1SegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, worm_1SegmentRect)
        worm_1InnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF,DARKGRAY , worm_1InnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
def drawHole(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    holeRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, WHITE, holeRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
