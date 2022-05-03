import pygame

pygame.init()

#game window


#window size (resolution); you can change it whenever you want.
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#caption for the window.
pygame.display.set_caption('2D Street Fighter')


#load images.

## background image.
# load the image.
BACKGROUND_IMG = pygame.image.load('./assets/img/background.gif').convert_alpha() #converts the image and keeps the alpha channel
PANEL_IMG = pygame.image.load('./assets/img/panel.png')
# draw the background.

def draw_bg():
    screen.blit(BACKGROUND_IMG, (0, 0)) # coordinates for the image to be in the top left corner.



#run the game.
running = True
while running is True:

    #draw the background.
    draw_bg()

    for event in pygame.event.get(): #event list handlers
        if event.type == pygame.QUIT: #if the quit button was pressed, then exit
            running = False  #no more True, exiting while loop

    #update, at each step, the animations we're going to use.
    pygame.display.update()
pygame.quit() #close the game window.