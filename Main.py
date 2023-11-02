import pygame
import random
import logging
import time

pygame.init()
pygame.font.init()

# Log settings/formatting
logging.basicConfig(filename='Proglog.log', level=logging.INFO, format='%(asctime)s :: %(message)s', filemode='w')

# window
screenwidth = 1475
screenheight = 500
screen = pygame.display.set_mode((screenwidth, screenheight))
# Set Game Name
pygame.display.set_caption("Purgatory")

# Define fonts
font = pygame.font.Font('Game/Romanica.ttf' ,24)
fontsmall = pygame.font.Font('Game/Romanica.ttf', 12)
fontbig = pygame.font.Font('Game/metro.ttf', 90)

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
Pink = (241, 182, 151)
darkpink = (164, 41, 111)

###store images
# background
bgimage = pygame.image.load("Game/img/bg3.png").convert_alpha()
menu = pygame.image.load("Game/img/menu.png").convert_alpha()

infopanel = pygame.image.load("Game/img/infopanel2.png").convert_alpha()
attackpanel = pygame.image.load("Game/img/panelfight.jpg").convert_alpha()

# Assets
tankselectimg = pygame.image.load("Game/img/t.png").convert_alpha()
warselectimage = pygame.image.load("Game/img/w.png").convert_alpha()
coinimg = pygame.image.load("Game/img/coin.png").convert_alpha()

# potions
# Under Free use 
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
atkpotion = pygame.image.load("Game/img/atkpotion.png").convert_alpha()
hppotion = pygame.image.load("Game/img/hppotion.png").convert_alpha()
defpotion = pygame.image.load("Game/img/defpotion.png").convert_alpha()

# other
nameplate = pygame.image.load("Game/img/nameplate.png").convert_alpha()

# Button
attackbuttonimage = pygame.image.load("Game/img/attack.png").convert_alpha()
targetbuttonimage = pygame.image.load("Game/img/Target.png").convert_alpha()
startbutton = pygame.image.load("Game/img/start.png").convert_alpha()
exitbutton = pygame.image.load("Game/img/exit.jpg").convert_alpha()

# Units
playertankimg = pygame.image.load("Game/img/tanker1.png").convert_alpha()
playerwarriorimg = pygame.image.load("Game/img/warrior1.png").convert_alpha()
enemytankimg = pygame.image.load("Game/img/tanker2.png").convert_alpha()
enemywarriorimg = pygame.image.load("Game/img/warrior2.png").convert_alpha()


####CLASSES
# Unit Class
class MasterUnit():
    def __init__(self, x, y, img, name, max_hp, current_hp, attack, defence, exp, rank, typer, potion):
        self.name = name
        self.max_hp = max_hp
        self.hp = current_hp
        self.attack = attack
        self.defence = defence
        self.alive = True
        self.image = img
        self.exp = exp
        self.rank = rank
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = typer
        self.potion = potion

    # Calculate Damage
    def sasageyo(self, targetdef, targethp):
        # deal damage to enemy
        damage = self.attack - targetdef + random.randint(-5, 10)
        if damage <= 0:
            return 0
        else:
            return damage

    # This function generate unit stats
    def generateunit(x, y, name, type, img, AIProgress):
        if img == "PT":
            imagename = playertankimg
        elif img == "PW":
            imagename = playerwarriorimg
        elif type == "tank" and img == "A":
            imagename = enemytankimg
        elif type == "war" and img == "A":
            imagename = enemywarriorimg

        if type == "war":
            unit = MasterUnit(x, y, imagename, name, 100, 100, random.randint(5, 20), random.randint(1, 10), 0,
                              1 + AIProgress, ("Warrior"), 0)
        if type == "tank":
            unit = MasterUnit(x, y, imagename, name, 100, 100, random.randint(1, 10), random.randint(5, 15), 0,
                              +AIProgress, ("Tanker"), 0)
        return unit

    def draw(self):
        screen.blit(self.image, self.rect)


# Fight night
class fightingphase():
    def __init__(self, Attacker, Target, AttackerList, Targetlist):
        self.attacking = Attacker
        self.targeting = Target
        self.Attackinglist = AttackerList
        self.Targetinglist = Targetlist

    # Attacking phase 
    def battlecalculation(self):

        damage = self.Attackinglist[self.attacking].sasageyo(self.Targetinglist[self.targeting].defence,
                                                          self.Targetinglist[self.targeting].hp)
        self.Targetinglist[self.targeting].hp = self.Targetinglist[self.targeting].hp - damage
        self.Attackinglist[self.attacking].exp += damage

        if damage > 10:
            extra = 1.2
        elif damage <= 0:
            extra = 1.5
        else:
            extra = 1

        TargetEXPEarned = self.Targetinglist[self.targeting].defence * extra

        self.Targetinglist[self.targeting].exp += TargetEXPEarned

        # Draws Text for player attacking

        text = (str(self.Attackinglist[self.attacking].name) + " dealt " + str(damage) + " damage to " + str(
            self.Targetinglist[self.targeting].name))
        rumble = font.render(text, True, white)
        draw_text =True
        display_duration = 1500  # Adjust the duration as needed

            # Calculate the time at which the text should be hidden
        hide_text_time = pygame.time.get_ticks() + display_duration

        while draw_text:
           


            # Draw the text if it's within the display duration
            if pygame.time.get_ticks() < hide_text_time:

                screen.blit(attackpanel, (520, 87))
                screen.blit(rumble, (545, 90))
            elif pygame.time.get_ticks() > hide_text_time :
      
                # Hide the text if the display duration has passed
                draw_text = False
            pygame.display.flip()
        

        


        logging.info(self.Attackinglist[self.attacking].name + " attacked " + self.Targetinglist[self.targeting].name)
        logging.info('Damage dealt: ' + str(damage))
        logging.info("Extra Bonus exp percentage decimal: " + str(extra))
        logging.info('Target Exp Earned: ' + str(TargetEXPEarned))

        return damage

    # AI Attack logic
    def Aiattacking(PlayerUnitList,AIList):
        APU = []
        APU.clear()
       
    

        for index, player in enumerate(PlayerUnitList):
            if player.alive :
                APU.append(index)


        for index, ai in enumerate(AIList):
             if ai.alive :
                y = random.choice(APU)
                slay = fightingphase(index, y, AIList, PlayerUnitList)
                slay.battlecalculation()
               

  

                    

# button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        position = pygame.mouse.get_pos()

        # Check mouse clicks
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Draw Unit's Informations
# Information panel
def DrawText(Name, type, atk, deff, exp, rank, currenthp, maxhp, x, y):
    n = font.render(str(Name), True, Pink)
    t = font.render(str(type), True, Pink)
    atk = font.render(str(atk), True, Pink)
    defence = font.render(str(deff), True, Pink)
    exp = font.render(str(round(exp)), True, Pink)
    rank = font.render(str(rank), True, Pink)
    hp = font.render(str(currenthp) + "/" + str(maxhp), True, Pink)

    screen.blit(n, (14 + x, 7 + y))
    screen.blit(t, (200 + x, 7 + y))
    screen.blit(atk, (72 + x, 42 + y))
    screen.blit(defence, (194 + x, 42 + y))
    screen.blit(exp, (72 + x, 75 + y))
    screen.blit(rank, (194 + x, 75 + y))
    screen.blit(hp, (70 + x, 107 + y))


def unitinformation(PlayerUnitList ,AIList):

    xAxis_postion= 300
    for player in PlayerUnitList:

        if player.alive:
            DrawText(player.name, player.type, player.attack, player.defence, player.exp,
                    player.rank, player.hp, player.max_hp, 0, xAxis_postion)
            screen.blit(infopanel, (0,   xAxis_postion))
        xAxis_postion -= 150    

    xAxis_postion= 300
    for ai in AIList:

        if ai.alive:
            DrawText(ai.name, ai.type, ai.attack, ai.defence, ai.exp, ai.rank, ai.hp,
                    ai.max_hp, 1175, xAxis_postion)
            screen.blit(infopanel, (1175,   xAxis_postion))
        xAxis_postion -= 150

  









###Button Creation
# P/AI= player/AI, U=Unit, digit=designation
PU1 = Button(220, 410, attackbuttonimage)
PU2 = Button(220, 260, attackbuttonimage)
PU3 = Button(220, 110, attackbuttonimage)

AIU1 = Button(1396, 410, targetbuttonimage)
AIU2 = Button(1396, 260, targetbuttonimage)
AIU3 = Button(1396, 110, targetbuttonimage)

# Potions Buttons
hppot = Button(10, 460, hppotion)
atkpot = Button(100, 460, atkpotion)
defpot = Button(190, 460, defpotion)

# Other buttons 
start = Button(550, 320, startbutton)
exit = Button(775, 320, exitbutton)

warriorselect = Button(540, 210, warselectimage)
tankerselect = Button(770, 210, tankselectimg)


# function for drawing panels




# Funtion to check player and AI deaths     
def checkunitdeath(unitlist):

    check_all_false = []

    for unit in unitlist:
        if unit.hp <= 0:
            unit.alive = False
            check_all_false.append (False)
            unit.hp = 0
        else:
            check_all_false.append(True)


    all_false = all(item is False for item in check_all_false)

    if all_false:
        return True





# Count player turns
def turnslefttext(playerturncounter):
    turnsinfo = font.render("Turns left: " + str(playerturncounter), True, Pink)
    screen.blit(turnsinfo, (310, 0))


# Draw textbox to type in names
def unitnameinput(unitname):
    screen.blit(nameplate, (650, 160))
    text_surface = font.render(unitname, True, white)
    screen.blit(text_surface, (656, 157))


# Potions 
def potionsfunc(type, PlayerUnitList):
    for unit in PlayerUnitList:
        if type == 1:
            logging.info('Healing Potion used')
            if unit.hp <= 95:
                unit.hp += 5
            elif unit.hp >= 95:
                unit.hp = 100
        elif type == 2:
            logging.info('Attack Potion used')
            unit.attack += 5
        elif type == 3:
            logging.info('Defence Potion used')
            unit.defence += 5

        # coins 


def coins(totalcoins):
    screen.blit(coinimg, (310, 30))
    coincounter = font.render("x" + str(totalcoins), True, white)
    screen.blit(coincounter, (345, 30))


# Unit Level Up
def unitLVL(P):
    if P.exp >= 100:
        P.rank += 1
        P.exp = 0
        P.attack += 4
        P.defence += 3
        P.exp = 0
        P.hp += 15
        logging.info('One of your unit(s) have ranked up')
        if P.hp >= 100:
            P.hp = 100


# Game Over screen        
def show_gameover():
    screen.blit(menu, (0, 0))
    gg = fontbig.render("G A M E O V E R", True, white)
    screen.blit(gg, (380, 90))


# Fps setter
def fpslock():
    FPS = 60  # frames per second setting
    fpsClock = pygame.time.Clock()
    fpsClock.tick(FPS)

def main():
    run = True
    unitname = ""
    playerturncounter = 3
    x = 0
    y = 0
    playerselectunit = 0
    enemyturn = 0
    selectenemy = 1
    battlephase = 0
    gamephase = False
    menuselection = False
    selectunit = True
    ppu1 = 1

    clicked = False
    mainmenu = True
    enemyturncounter = 0
    generateAIunit = False
    checkingPlayerDeath = False
    AIList = []
    PlayerUnitList = []
    checkingAIDeath = False
    AIProgress = 0
    totalcoins = 0
    while run:
        # Allow Main to access global Variables
        fpslock()
        pop_up_time = pygame.time.get_ticks() + 3000 

        # Main Menu Loop
        while mainmenu :
            screen.blit(menu, (0, 0))
            Welcome = fontbig.render("P U R G A T O R Y", True, white)
            screen.blit(Welcome, (380, 90))
            if start.draw():
                mainmenu = False
                menuselection = True

            if exit.draw():
                run = False
            else:
                break
        if menuselection :  # Unit Selection Loop
            totalcoins = 0  # Resets Coin Count After Death
            if selectunit :
                screen.blit(menu, (0, 0))
                line1 = font.render("Enter a name (Max 10 Character)", True, white)
                line2 = font.render("Then click a profession", True, white)
                line3 = font.render("Unit " + str(ppu1), True, Pink)

                screen.blit(line1, (570, 50))
                screen.blit(line2, (615, 85))
                screen.blit(line3, (699, 115))

                screen.blit(playerwarriorimg, (540, 260))
                screen.blit(playertankimg, (770, 260))


                unitnameinput(unitname)



                # Generate unit when button click
                if ppu1 == 1:
                    if warriorselect.draw():
                        PlayerUnitList.append( MasterUnit.generateunit(380, 390, unitname, "war", "PW", 0))
                        ppu1 += 1

                    if tankerselect.draw():
                        PlayerUnitList.append(MasterUnit.generateunit(380, 390, unitname, "tank", "PT", 0))
                        ppu1 += 1
                elif  ppu1 == 2:
                    if warriorselect.draw():
                        PlayerUnitList.append(MasterUnit.generateunit(510, 350, unitname, "war", "PW", 0))
                        ppu1 += 1

                    if tankerselect.draw():
                        PlayerUnitList.append( MasterUnit.generateunit(510, 350, unitname, "tank", "PT", 0))
                        ppu1 += 1
                elif  ppu1 == 3:
                    if warriorselect.draw():
                        PlayerUnitList.append( MasterUnit.generateunit(640, 310, unitname, "war", "PW", 0))
                        ppu1 += 1

                    if tankerselect.draw():
                        PlayerUnitList.append(MasterUnit.generateunit(640, 310, unitname, "tank", "PT", 0))
                        ppu1 += 1
                elif  ppu1 == 4:
         
                    selectunit = False
                    generateAIunit = True
                    gamephase = True
                    menuselection = False
        # Generates AI Stats/Info           
        if generateAIunit :

            # Generate AI
            typelist = ["war", "tank"]

            AIList.insert(0,MasterUnit.generateunit(1080, 390, 'AI ' + str(random.randint(0, 9)) + str(random.randint(0, 9)),
                                              random.choice(typelist), "A", AIProgress))
            

            AIList.insert(1, MasterUnit.generateunit(950, 350, 'AI ' + str(random.randint(0, 9)) + str(random.randint(0, 9)),
                                              random.choice(typelist), "A", AIProgress))
            
            
            AIList.insert(2, MasterUnit.generateunit(820, 310, 'AI ' + str(random.randint(0, 9)) + str(random.randint(0, 9)),
                                              random.choice(typelist), "A", AIProgress))
            
            AIProgress += 1
            gamephase = True
            generateAIunit = False

            logging.info('AI has been generated')

        # Main Game Loop      
        while gamephase :

            screen.blit(bgimage, (0, 0))

            unitinformation(PlayerUnitList ,AIList)

            turnslefttext(playerturncounter)
            coins(totalcoins)

            for unit in PlayerUnitList: 
                unitLVL(unit)

            for ai in AIList: 
                unitLVL(ai)

            for unit in PlayerUnitList:
                if unit.alive :
                    unit.draw()
            for unit in AIList:
                if unit.alive :
                    unit.draw()
            if totalcoins > 40:
                hp = fontsmall.render("Hp: 50c ", True, white)
                screen.blit(hp, (45, 470))
                if hppot.draw():
                    potionsfunc(1, PlayerUnitList)
                    totalcoins -= 50
            if totalcoins > 20:
                atk = fontsmall.render("Atk: 20c ", True, white)
                screen.blit(atk, (135, 470))
                if atkpot.draw():
                    potionsfunc(2, PlayerUnitList)
                    totalcoins -= 20
            if totalcoins > 30:
                defp = fontsmall.render("Def: 30c ", True, white)
                screen.blit(defp, (220, 470))
                if defpot.draw():
                    potionsfunc(3, PlayerUnitList)
                    totalcoins -= 30

            # Fighting game loop
            if checkingAIDeath == False and checkingPlayerDeath == False:
                if 1 <= playerturncounter <= 3:  # This checks player turns and attacks
                    while playerselectunit == 0:
                        if PlayerUnitList[0].alive :
                            if PU1.draw():
                                x = 0

                                battlephase += 1
                                playerselectunit += 1
                                selectenemy = 0

                        if PlayerUnitList[1].alive :
                            if PU2.draw():
                                x = 1

                                battlephase += 1
                                playerselectunit += 1
                                selectenemy = 0

                        if PlayerUnitList[2].alive :
                            if PU3.draw():
                                x = 2

                                battlephase += 1
                                playerselectunit += 1
                                selectenemy = 0


                            else:
                                break
                        else:
                            break
                    while selectenemy == 0:
                        if AIList[0].alive :
                            if AIU1.draw():
                                y = 0

                                battlephase += 1
                                selectenemy += 1

                        if AIList[1].alive :
                            if AIU2.draw():
                                y = 1

                                battlephase += 1
                                selectenemy += 1

                        if AIList[2].alive :
                            if AIU3.draw():
                                y = 2

                                battlephase += 1
                                selectenemy += 1

                            else:
                                break
                        else:
                            break
                    while battlephase == 2:
                        krope = fightingphase(x, y, PlayerUnitList, AIList)
                        totalcoins += krope.battlecalculation()
                        battlephase = 0
                        playerselectunit = 0
                        playerturncounter -= 1
                        enemyturn += 1
                        if checkunitdeath(AIList) :
                            checkingAIDeath = True

                    else:
                        break
                # Ai turns and Attacks
                if playerturncounter == 0:
                    while enemyturn > 0:
                        if checkunitdeath(PlayerUnitList) :
                            checkingPlayerDeath = True
                        fightingphase.Aiattacking(PlayerUnitList, AIList)
                        playerturncounter += 3
                        enemyturn -= 3
                        if checkunitdeath(PlayerUnitList) :
                            checkingPlayerDeath = True

                    else:
                        break

            # Checks AI Death     
            if checkingAIDeath :
                enemyturncounter = 0
                gamephase = False
                generateAIunit = True
                checkingAIDeath = False
                playerturncounter = 3

        # Checks players death 
        if checkingPlayerDeath :
            gamephase = False
            show_gameover()
            if start.draw():
                menuselection = True
                enemyturncounter = 0
                gamephase = False
                playerturncounter = 3
                checkingPlayerDeath = False
                selectunit = True
                ppu1 = 1

            if exit.draw():
                run = False

        # Event Handler ALl code in main should be above this
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    unitname = unitname[:-1]
                else:
                    unitname += event.unicode

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
