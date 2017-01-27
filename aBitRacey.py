import pygame, time, random
from pprint import pprint

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0, 200, 0)
bright_red = (255,0,0)
bright_green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
car_width = 73

pause = False

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Dodged: {}'.format(count), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black) #True is for anti-aliasing
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

def crash():
    message_display('You Crashed')
    game_loop()

def button(x, y, width, height, active_color, inactive_color, message, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    smallText = pygame.font.Font('freesansbold.ttf', 24)
    TextSurf, TextRect = text_objects(message, smallText)
    TextRect.center = (x + width/2, y + height/2)
    gameDisplay.blit(TextSurf, TextRect)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects('A bit Racey', largeText)
        TextRect.center = (display_width/2, display_height/2)
        gameDisplay.blit(TextSurf, TextRect)

        button(150, 450, 100, 50, bright_green, green, 'GO!', game_loop)
        button(550, 450, 100, 50, bright_red, red, 'QUIT', exit)

        pygame.display.update()
        clock.tick(60)

def unpause():
    global pause
    pause = False

def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects('Paused', largeText)
        TextRect.center = (display_width/2, display_height/2)
        gameDisplay.blit(TextSurf, TextRect)

        button(150, 450, 100, 50, bright_green, green, 'Continue', unpause)
        button(550, 450, 100, 50, bright_red, red, 'Quit', exit)

        pygame.display.update()
        clock.tick(60)

def exit():
    pygame.quit()
    quit()

def game_loop():
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_left_change = 0
    x_right_change = 0

    thing_speed = 7
    thing_width = 100
    thing_height = 100
    thing_startx = random.randrange(0, display_width - thing_width)
    thing_starty = -600

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_left_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_right_change = +5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_left_change = 0
                if event.key == pygame.K_RIGHT:
                    x_right_change = 0

        x += x_left_change
        x += x_right_change

        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width - thing_width)
            dodged += 1
            if thing_speed <= 15:
                thing_speed += 1


        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
exit()
