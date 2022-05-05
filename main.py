import pygame, random, assets.button as button
from pygame import font

APP_TITLE = 'Street Fighter 2D' #to be modified, later on.

#### classes.
class Fighter(object):
    def __init__(self, x, y, name, max_HP, strenght, potions): #ctor
        ## x,y --> coordinates; max_HP --> max life; strength --> max strength; potions --> list of potions
        self.__name = name
        self.__max_HP = max_HP
        self.__hp = max_HP #because we initially start with max HP
        self.__strength = strenght
        self.__animation_list = list()
        self.__frame_index = 0 #controls which picture we're taking/loading for the sprite.
        self.__update_time = pygame.time.get_ticks()
        self.__action = 0 #0=idle; 1=attack; 2=hurt; 3=dead ---> the state of the current character.

        ### load the IDLE images.
        temp_list = list()

        for i in range(8): #traverse the sprite images.
            __image = pygame.image.load(f'./assets/{name}/Idle/{i}.png')  # load the proper character.
            __image = pygame.transform.scale(__image, (__image.get_width() * 3, __image.get_height() * 3)) #make the image 3 times bigger.
            temp_list.append(__image) #add the image to the list.
        self.__animation_list.append(temp_list) #add the images to the master list.

        ### load the ATTACK images.
        temp_list = list()

        for i in range(8):  # traverse the sprite images.
            __image = pygame.image.load(f'./assets/{name}/Attack/{i}.png')  # load the proper character.
            __image = pygame.transform.scale(__image, (
            __image.get_width() * 3, __image.get_height() * 3))  # make the image 3 times bigger.
            temp_list.append(__image)  # add the image to the list.
        self.__animation_list.append(temp_list)  # add the images to the master list.

        ### load the HURT images.
        temp_list = list()

        for i in range(3):  # traverse the sprite images.
            __image = pygame.image.load(f'./assets/{name}/Hurt/{i}.png')  # load the proper character.
            __image = pygame.transform.scale(__image, (
                __image.get_width() * 3, __image.get_height() * 3))  # make the image 3 times bigger.
            temp_list.append(__image)  # add the image to the list.
        self.__animation_list.append(temp_list)  # add the images to the master list.

        ### load the DEATH images.
        temp_list = list()

        for i in range(10):  # traverse the sprite images.
            __image = pygame.image.load(f'./assets/{name}/Death/{i}.png')  # load the proper character.
            __image = pygame.transform.scale(__image, (
                __image.get_width() * 3, __image.get_height() * 3))  # make the image 3 times bigger.
            temp_list.append(__image)  # add the image to the list.
        self.__animation_list.append(temp_list)  # add the images to the master list.

        self.__image = self.__animation_list[self.__action][self.__frame_index] ## access for some action, the frame index.
        self.__potions = potions
        self.__start_potions = potions
        self.__alive = True #the character is initially alive
        self.__rect = self.__image.get_rect() #create the rectangle provided by the image; allows you to position the object wherever you want on the screen.
        self.__rect.center = (x,y) #put the coordinates on the center of the rectangle.
    def draw(self,screen):
        screen.blit(self.__image, self.__rect)
    def update(self):
        animation_cooldown = 100
        #handle animation.
        #update image.
        self.__image = self.__animation_list[self.__action][self.__frame_index]
        #check if enough time has passed after last update.
        if pygame.time.get_ticks() - self.__update_time > animation_cooldown:
            self.__update_time = pygame.time.get_ticks()
            self.__frame_index += 1
        #if we run out of images from the sprite, then reset from the start (first image).
        if self.__frame_index >=  len(self.__animation_list[self.__action]): #index for particular animation
            if self.__action == 3: #target is DEAD
                self.__frame_index = len(self.__animation_list[self.__action]) - 1 #get the last element of dead animation.
            else:
                self.idle() #come back to idle state.
    def get_HP(self):
        return self.__hp
    def get_name(self):
        return self.__name
    def set_alive(self, alive):
        self.__alive = alive
    def get_max_HP(self):
        return self.__max_HP
    def set_HP(self, hp):
        self.__hp = hp
    def alive(self):
        return self.__alive
    def get_rect(self):
        return self.__rect
    def get_potions(self):
        return self.__potions
    def idle(self):
        # set variables to idle animation.
        self.__action = 0  # idle state
        self.__frame_index = 0  # reset the frame index.
        self.__update_time = pygame.time.get_ticks()  # update the time.
    def attack(self, target):
        #deal damage to enemy.
        rand = random.randint(-5, 5) #generate a random number.
        damage = self.__strength + rand #compute the damage.
        target.set_HP(target.get_HP()-damage) #decrease the target's HP.
        ##mark target as hurt.
        target.hurt()
        #check if target has died.
        if target.get_HP() < 1:
            target.set_HP(0)
            target.set_alive(False)
            target.death() #turn on the death animation.
        damage_text = DamageText(target.get_rect().centerx, target.get_rect().y, str(damage), (255, 0, 0)) #build the damage text.
        damage_text_group.add(damage_text)

        #set variables to attack animation.
        self.__action = 1 #attack state
        self.__frame_index = 0 #reset the frame index.
        self.__update_time = pygame.time.get_ticks() #update the time.

    def hurt(self):
        # set variables to HURT animation.
        self.__action = 2  # hurt state
        self.__frame_index = 0  # reset the frame index.
        self.__update_time = pygame.time.get_ticks()  # update the time.

    def death(self):
        # set variables to HURT animation.
        self.__alive = False
        self.__action = 3  # death state
        self.__frame_index = 0  # reset the frame index.
        self.__update_time = pygame.time.get_ticks()  # update the time.

    def reset(self):
        self.__alive = True #reset alive status (to True)
        self.__potions = self.__start_potions #reset the potions
        self.__hp = self.__max_HP
        self.__frame_index = 0

    def set_potions(self, potions):
        self.__potions = potions





######## class for the Healthbar.

class Healthbar(object):
    def __init__(self, x, y, HP, MAX_HP):
        self.__x = x
        self.__y = y
        self.__HP = HP
        self.__MAX_HP = MAX_HP
    def draw(self, HP, screen):
        #update with current HP.
        self.__HP = HP
        #compute the health ratio.
        ratio = self.__HP / self.__MAX_HP
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        pygame.draw.rect(screen, RED, (self.__x, self.__y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.__x, self.__y, 150 * ratio, 20)) #if we use the health ratio, make the healthbar fit properly.

### initialization and fonts.
pygame.init()
FONTS = pygame.font.SysFont('Arial', 26) #font family and size

######### Damage Text class

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = FONTS.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self):
        #move damage text up.
        self.rect.y -= 1
        #delete the text after a few seconds.
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()


#### main function.
def main():


    CLOCK = pygame.time.Clock() # the clock

    FPS = 60 # the number of FPS we want.

    #game window


    #window size (resolution); you can change it whenever you want.
    BOTTOM_PANEL = 150
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400 + BOTTOM_PANEL


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #caption for the window.
    pygame.display.set_caption(APP_TITLE)


    #define game variables.

    current_fighter = 1
    total_fighters = 3
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    clicked = False
    potion_effect = 15 #how much you can heal using the potion.
    game_over = 0 #helper flag for game over


    #load images.

    ## background image.
    # load the image.
    BACKGROUND_IMG = pygame.image.load('assets/Background/background.png').convert_alpha() #converts the image and keeps the alpha channel
    PANEL_IMG = pygame.image.load('assets/Icons/panel.png').convert_alpha() #converts the image and keeps the alpha channel
    # sword image
    SWORD_IMG = pygame.image.load('assets/Icons/sword.png').convert_alpha()
    # potion image
    POTION_IMG = pygame.image.load('assets/Icons/potion.png').convert_alpha()
    #load victory and defeat images.
    VICTORY_IMG = pygame.image.load('assets/Icons/victory.png').convert_alpha()
    DEFEAT_IMG = pygame.image.load('assets/Icons/defeat.png').convert_alpha()
    #load RESTART BUTTON
    RESTART_IMG = pygame.image.load('assets/Icons/restart.png').convert_alpha()
    #define colors

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)



    #function for drawing text.
    def draw_text(text, font, text_col, x, y):
        img = FONTS.render(text, True, text_col)
        screen.blit(img, (x, y))


    # draw the background.
    def draw_bg():
        screen.blit(BACKGROUND_IMG, (0, 0)) # coordinates for the image to be in the top left corner.

    def draw_panel():
        #draw panel rectangle.
        screen.blit(PANEL_IMG, (0, SCREEN_HEIGHT - BOTTOM_PANEL))
        #print the knight informations.
        draw_text(f'{knight.get_name()} HP: {knight.get_HP()}', FONTS, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
        #print the bandits informations.
        for count, i in enumerate(bandits):
            #show name and health of the current bandit.
            draw_text(f'{i.get_name()} HP: {i.get_HP()}', FONTS, GREEN, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)

    #create a character - knight.
    knight = Fighter(200, 260, 'Knight', 30, 10, 3)

    #create 2 bandits.

    bandits = [Fighter(550, 270, 'Bandit', 20, 6, 1), Fighter(700, 270, 'Bandit', 20, 6, 1)]


    #create a healthbar for knight.
    knight_healthbar = Healthbar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.get_HP(), knight.get_max_HP()) #render the healthbar above the panel.
    bandit1_healthbar = Healthbar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40, bandits[0].get_HP(), bandits[0].get_max_HP()) #render the healthbar above the panel.
    bandit2_healthbar = Healthbar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 100, bandits[1].get_HP(), bandits[1].get_max_HP()) #render the healthbar above the panel.

    #create buttons.
    potion_button = button.Button(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 70, POTION_IMG, 64, 64) #create a button with the POTION sprite.
    restart_button = button.Button(screen, 330, 120, RESTART_IMG, 120, 120) #create the RESTART button






    #run the game.
    running = True
    while running is True:
        # tick the clock.
        CLOCK.tick(FPS)  # with the wanted FPS

        #draw the background.
        draw_bg()

        #draw the panel.
        draw_panel()

        #draw the healthbars on the panel.
        knight_healthbar.draw(knight.get_HP(), screen)
        bandit1_healthbar.draw(bandits[0].get_HP(), screen)
        bandit2_healthbar.draw(bandits[1].get_HP(), screen)

        #update the fighter.
        knight.update()
        #draw the fighter.
        knight.draw(screen)

        # draw the potion button.
        if potion_button.draw():
            potion = True

        # show number of potions remaining.
        draw_text(f'{knight.get_potions()}', FONTS, RED, 150, SCREEN_HEIGHT - BOTTOM_PANEL + 70)

        ## draw the bandits.
        for bandit in bandits:
            bandit.update()
            bandit.draw(screen)

        ### draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        ##### control player actions.
        ## reset action variables.

        attack, potions = False, False
        pos = pygame.mouse.get_pos()
        target = None
        for count, bandit in enumerate(bandits):
            if bandit.get_rect().collidepoint(pos):
                #hide mouse.
                pygame.mouse.set_visible(False)
                #show sword in place of mouse cursor.
                screen.blit(SWORD_IMG, pos)
                if clicked == True and bandit.alive(): #if clicked, AND target is ALIVE, then go into attack state.
                    attack = True
                    target = bandits[count] #attack the current enemy.


        if game_over == 0: #if game is not over yet
            ## player action.
            if knight.alive() == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #if wait time passed, attack
                        if attack == True and target is not None:
                            knight.attack(target) #attack the target.
                            current_fighter += 1 #move on to the next fighter.
                            action_cooldown = 0 #reset the action cooldown.
                        if potion == True:
                            if knight.get_potions() > 0: #if we have available potions
                                #check if the potion would heal the player beyond max HP.
                                if knight.get_max_HP() - knight.get_HP() > potion_effect:
                                    heal_ammount = potion_effect
                                else:
                                    heal_ammount = knight.get_max_HP() - knight.get_HP()
                                knight.set_HP(knight.get_HP() + heal_ammount) #add the ammount to the current player's HP.
                                knight.set_potions(knight.get_potions()-1) #set the potions decremented by one.
                                damage_text = DamageText(knight.get_rect().centerx, knight.get_rect().y, str(heal_ammount), (0, 255, 0))  # build the damage text. GREEN because we're healing.
                                damage_text_group.add(damage_text)
            else:
                game_over = -1 #player loss

            #make sure the mouse is visible!
            pygame.mouse.set_visible(True)
            ## enemy action.
            for count, bandit in enumerate(bandits):
                if current_fighter == 2 + count:
                    if bandit.alive() == True: #check if character is still alive.
                        action_cooldown += 1 #increase the cooldown.
                        if action_cooldown >= action_wait_time:
                            #check if enemy needs rehealing.
                            if (bandit.get_HP()/bandit.get_max_HP()) < 0.5 and bandit.get_potions() > 0:
                                #if ratio is below 0.5 and we have potions available
                                # check if the potion would heal the enemy beyond max HP.
                                if bandit.get_max_HP() - bandit.get_HP() > potion_effect:
                                    heal_ammount = potion_effect
                                else:
                                    heal_ammount = bandit.get_max_HP() - bandit.get_HP()
                                damage_text = DamageText(bandit.get_rect().centerx, bandit.get_rect().y, str(heal_ammount), (0, 255, 0))  # build the damage text. GREEN because we're healing.
                                damage_text_group.add(damage_text)
                                bandit.set_HP(knight.get_HP() + heal_ammount)  # add the ammount to the current player's HP.
                                bandit.set_potions(bandit.get_potions() - 1)  # set the potions decremented by one.
                                current_fighter += 1
                                action_cooldown = 0
                            else:
                                #attack.
                                bandit.attack(knight)
                                current_fighter += 1
                                action_cooldown = 0 #reset the cooldown.
                    else: #bandit is NOT alive!
                        current_fighter += 1 #then, move on to the next player.

            #if all fighters have had a turn, then reset.
            if current_fighter > total_fighters:
                current_fighter = 1

        #check if all bandits are dead.
        alive_bandits = 0
        for bandit in bandits:
            if bandit.alive() == True:
                alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1 #player WINS! all enemies are dead.

        #check if game is over
        if game_over: #game is over
            # make sure the mouse is visible!
            pygame.mouse.set_visible(True)
            if game_over == 1: #victory
                screen.blit(VICTORY_IMG, (250, 50))
            elif game_over == -1: #loss
                screen.blit(DEFEAT_IMG, (290, 50))
            if restart_button.draw():
                knight.reset() #reset player 1.
                #reset the other players.
                for bandit in bandits:
                    bandit.reset()
                current_fighter = 1 #reset current fighter, to player 1.
                action_cooldown = 0
                game_over = 0 #game in process.

        for event in pygame.event.get(): #event list handlers
            if event.type == pygame.QUIT: #if the quit button was pressed, then exit
                running = False  #no more True, exiting while loop
            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button down was pressed
                clicked = True
            else:
                clicked = False

        #update, at each step, the animations we're going to use.
        pygame.display.update()
    pygame.quit() #close the game window.

### run the game.

if __name__ == '__main__':
    main()