import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
pygame.init()
pygame.key.set_repeat(200, 0)

#Helper functions
def resourcePath(relativePath, subdir=''):
    ''' Get absolute path to resource, works for dev and for PyInstaller '''
    try:
        #PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        relativePath = os.path.join(subdir, relativePath)
        if relativePath.endswith('.mp3'):
            #Music files
            basePath = os.path.abspath('Music')
        elif relativePath.endswith('.txt'):
            #Text files
            basePath = os.path.abspath('Text Files')
        else:
            #Image files
            basePath = os.path.abspath('Images')
    return os.path.join(basePath, relativePath)

def exitGame():
    pygame.quit()
    sys.exit()

#UI Tools
class Button:
    def __init__(self, screen, position, text, **kwargs):
        self.screen = screen
        self.position = position
        self.font = pygame.font.SysFont('Garamond', 40)
        self.bg = kwargs.get('bg', (255,165,0))
        self.fg = kwargs.get('fg', (255, 0, 0))
        states = ['normal', 'disabled']
        self.state = kwargs.get('state', 'normal')
        pad = kwargs.get('pad', 0)
        self.text_render = self.font.render(text.center(len(text) + pad), 1, self.fg)
        self.draw()
        
    def draw(self):
        x, y, w, h = self.text_render.get_rect()
        x, y = self.position
        pygame.draw.line(self.screen, self.bg, (x, y), (x + w , y), 5)
        pygame.draw.line(self.screen, self.bg, (x, y - 2), (x, y + h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(self.screen, [abs(val-50) for val in self.bg], (x, y, w , h))
        self.render_object = self.screen.blit(self.text_render, (x, y))

    def clicked(self):
        if self.state == 'normal':
            return self.render_object.collidepoint(pygame.mouse.get_pos())
        return False

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = (255, 0, 0)
        self.COLOR_ACTIVE = (0, 0, 255)
        self.GEN_COLOR = (34, 139, 34)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.defaultText = self.text = text
        self.font = pygame.font.SysFont('Arial', 50)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.val = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                #Toggle the active variable.
                self.active = not self.active
                if self.text == '':
                    self.text = self.defaultText
                elif self.text == self.defaultText:
                    self.text = ''
                self.txt_surface = self.font.render(self.text, True, self.color)
            else:
                self.active = False
            #Change the current color of the input box.
            if self.active:
                self.color = self.COLOR_ACTIVE
            elif self.val:
                self.color = self.GEN_COLOR
            else:
                self.color = self.COLOR_INACTIVE
                
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.val = self.text
                    self.color = self.GEN_COLOR
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 10:
                    self.text += event.unicode
                #Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        #Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        #Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        #Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class ControlScreen:
    def __init__(self, screen, bg, textFg=(255, 0, 0)):
        self.screen = screen
        self.bg = bg
        self.title = pygame.image.load(resourcePath('controls.png'))
        self.font = pygame.font.SysFont('Didot', 40)
        self.textFg = textFg
        with open(resourcePath('controls.txt'), 'r', encoding='utf-8') as f:
            delimiter = f.read(1)
            self.text = f.read()
        self.controls = self.text.split(delimiter)
        self.displayUI()
        self.mainloop()

    def displayUI(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title, (225, 0))
        xStart = 70
        yStart = 60
        for i in range(len(self.controls)-1):
            for j, line in enumerate(self.controls[i].splitlines()):
                text_render = self.font.render(line, 1, self.textFg)
                self.screen.blit(text_render, (xStart + i*400, yStart + j*40))
        self.backBtn = Button(self.screen, (0, 0), '\u2190', pad=2)
        pygame.draw.line(self.screen, (255, 0, 0), (400, 100),
                         (400, self.screen.get_height()-25), 3)

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exitGame()
                    key_to_start = (event.key in [pygame.K_s, pygame.K_RIGHT,
                                                  pygame.K_UP, pygame.K_RETURN,
                                                  pygame.K_BACKSPACE])
                    if key_to_start:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backBtn.clicked():
                        return
                        
            pygame.display.update()
    
class MenuScreen:
    ''' Game start screen, returns the player names '''
    def __init__(self, screen, bg, title):
        self.screen = screen
        self.bg = bg
        self.title = title
        self.player1_img = pygame.image.load(resourcePath('Player1.png', subdir='Player 1'))
        self.player2_img = pygame.image.load(resourcePath('Player2.png', subdir='Player 2'))
        self.displayUI()
        self.entryWidgets = [InputBox(40, 100, 200, 75, 'Enter name'),
                             InputBox(560, 100, 200, 75, 'Enter name')]
                             
        self.mainloop()
        
    def displayUI(self):
        #Blitting images
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title, (160, 0))
        self.screen.blit(self.player1_img, (50, 210))
        self.screen.blit(self.player2_img, (550, 220))
        #Drawing button widgets
        self.startBtn = Button(self.screen, (300, 200), 'Start', pad=15)
        self.controlsBtn = Button(self.screen, (295, 275), 'Controls', pad=10)
        self.quitBtn = Button(self.screen, (300, 350), 'Quit', pad=15)

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        exitGame()
                [entryWidget.handle_event(event) for entryWidget in self.entryWidgets]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quitBtn.clicked():
                        exitGame()
                    elif self.startBtn.clicked():
                        values = [e.val for e in self.entryWidgets]
                        #Checking if values Exist
                        if all(values):
                            return
                    elif self.controlsBtn.clicked():
                        ControlScreen(self.screen, self.bg)
                        self.displayUI()
            self.displayUI()
            for entryWidget in self.entryWidgets:
                entryWidget.draw(self.screen)
                entryWidget.update()
            pygame.display.update()

    def getPlayerNames(self):
        return [e.val for e in self.entryWidgets]

class PauseScreen:
    def __init__(self, screen, bg):
        self.screen = screen
        self.bg = bg
        self.title = pygame.image.load(resourcePath('paused.png'))
        self.player1_img = pygame.image.load(resourcePath('Player1.png', subdir='Player 1'))
        self.player2_img = pygame.image.load(resourcePath('Player2.png', subdir='Player 2'))
        self.font = pygame.font.SysFont('Garamond', 50)
        self.reset = False
        self.displayUI()
        self.mainloop()

    def displayUI(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title, (300, 40))
        self.screen.blit(self.player1_img, (50, 210))
        self.screen.blit(self.player2_img, (550, 220))
        self.resumeBtn = Button(self.screen, (320, 150), 'Resume', pad=10)
        self.resetBtn = Button(self.screen, (320, 210), 'Reset', pad=14)
        self.quitBtn = Button(self.screen, (320, 270), 'Quit', pad=15)
        self.aboutBtn = Button(self.screen, (320, 330), 'About', pad=12)
        self.aboutToggle = False

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exitGame()
                    key_to_start = (event.key in [pygame.K_s, pygame.K_RETURN])
                    if key_to_start:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resumeBtn.clicked():
                        return
                    elif self.resetBtn.clicked():
                        self.reset = True
                        return
                    elif self.aboutBtn.clicked():
                        if self.aboutToggle:
                            text_render = self.font.render('Created By: Sanvit Katrekar', 1, (255, 0, 0))
                            self.screen.blit(text_render, (150, 400))
                        else:
                            self.displayUI()
                        self.aboutToggle = not self.aboutToggle
                    elif self.quitBtn.clicked():
                        exitGame()
                        
            pygame.display.update()

game = pygame.display.set_mode((850,480))
pygame.display.set_caption('Jumping Game')
pygame.display.set_icon(pygame.image.load(resourcePath('gameIcon.png')))

a = True
b = False

alive1 = alive2 = True

bg = pygame.image.load(resourcePath('bg.jpg'))
gameLogo = pygame.image.load(resourcePath('gameLogo.png'))

walkRight = [pygame.image.load(resourcePath('R1.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R2.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R3.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R4.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R5.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R6.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R7.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R8.png', subdir='Player 1')),
             pygame.image.load(resourcePath('R9.png', subdir='Player 1'))]

walkLeft = [pygame.image.load(resourcePath('L1.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L2.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L3.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L4.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L5.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L6.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L7.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L8.png', subdir='Player 1')),
            pygame.image.load(resourcePath('L9.png', subdir='Player 1'))]

Walkleft = [pygame.image.load(resourcePath('L1E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L2E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L3E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L4E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L5E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L6E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('L7E.png', subdir='Player 2'))]

Walkright = [pygame.image.load(resourcePath('R1E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R2E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R3E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R4E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R5E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R6E.png', subdir='Player 2')),
             pygame.image.load(resourcePath('R7E.png', subdir='Player 2'))]

punchleft=[pygame.image.load(resourcePath('L8E.png', subdir='Player 2')),
           pygame.image.load(resourcePath('L9E.png', subdir='Player 2')),
           pygame.image.load(resourcePath('L10E.png', subdir='Player 2')),
           pygame.image.load(resourcePath('L11E.png', subdir='Player 2'))]

punchright=[pygame.image.load(resourcePath('R8E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('R9E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('R10E.png', subdir='Player 2')),
            pygame.image.load(resourcePath('R11E.png', subdir='Player 2'))]

#player1, player2 = 'Sanvit', 'Tanaya'
player1, player2 = MenuScreen(game, bg, gameLogo).getPlayerNames()

score = 0

x1 = 50#Coordinates
y1 = 400
width1 = 40
height1 = 60
speed1 = 5#Speed of the character1
health1 = 10
damage1 = 2

x2 = 725
y2 = 400
width2 = 40
height2 = 60
speed2 = 6
health2 = 15
damage2 = 1

shootLoop = 0

run = True
t = 0

count = count2 = 0

jumpcount = jumpcount2 = 10#JUMP variables
isJump = isJump2 = False
walkcount = w2 = 0
punch = False

GAME_RESET = False

isFly = isFly2 = False#FLY variables

left = left2 = False#Loading images for moving left
right = right2 = False#Loading images for moving right

class Projectile:
   def __init__(self,x,y,radius,colour,facing):
      self.x = x
      self.y = y
      self.radius = radius
      self.colour = colour
      self.facing = facing
      self.vel = 10 * facing
      
   def draw(self,game):
      pygame.draw.circle(game ,self.colour, (self.x,self.y), self.radius, 1)

clock = pygame.time.Clock()#Initializing clock

playAgainBtn = None
def redrawgame():#Main drawing fuction of game
    global walkcount,w2,a,b,punch,t,left2,right2,score, pauseBtn, playAgainBtn

    game.blit(bg,(0,0))

    pauseBtn = Button(game, (340, 20), 'Pause', pad=2)
    
    text1 = font.render(str(player1) + "'s Health: " + str(health1), 1, (0,0,0))
    game.blit(text1, (10,10))
    
    text2 = font.render(str(player2) + "'s Health: " + str(health2), 1, (0,0,0))
    game.blit(text2, (550,10))
    if not alive1:
          win_text2 = font.render(str(player2) + ' Wins! Congratulations!', 1, (0,0,0))
          game.blit(win_text2, (250, 100))
       
    elif not alive2:
          win_text1 = font.render(str(player1) + ' Wins! Congratulations!', 1, (0,0,0))
          game.blit(win_text1, (250, 100))

    if not all([alive1, alive2]):
        playAgainBtn = Button(game, (310, 150), 'Play Again', pad=2)
    
    if alive1:
       if walkcount+1 > 27:
           walkcount = 0
         
       if left:  
           game.blit(walkLeft[walkcount//3], (x1,y1))#LOADING WALKING LEFT IMAGES
           walkcount += 1
           b = True
       elif right:
           game.blit(walkRight[walkcount//3], (x1,y1))#LOADING WALKING RIGHT IMAGES
           walkcount += 1
           b = False
       else:
          if b:
             game.blit(walkLeft[0], (x1, y1))#LOADING THE IDLE IMAGE
          else:
             game.blit(walkRight[0], (x1,y1))

       pygame.draw.rect(game, (255,0,0), (x1 + 10, y1 - 10, 50, 10))
       pygame.draw.rect(game, (0,128,0), (x1 + 10, y1 - 10, 50 - (5 * (10 - health1)), 10))

    if alive2:

       if w2+1 > 21:
           w2=0
       if t+1 > 12:
           t = 0
           punch = False
           
       if punch:
           if a:
              game.blit(punchleft[t//4],(x2,y2))
           else:
              game.blit(punchright[t//4],(x2,y2))
           t+=1
           
       elif left2:  
           #LOADING WALKING LEFT IMAGES
           game.blit(Walkleft[w2//3], (x2,y2))
           w2 += 1
           a = True
       elif right2:
           #LOADING WALKING RIGHT IMAGES
           game.blit(Walkright[w2//3], (x2,y2))
           w2 += 1
           a=False
           
       else:
           if a: game.blit(Walkleft[6],(x2,y2))
           else: game.blit(Walkright[6],(x2,y2))

       pygame.draw.rect(game, (255,0,0), (x2 + 20, y2 - 15, 60, 10))
       pygame.draw.rect(game, (0,128,0), (x2 + 20, y2 - 15, 60 - (4 * (15 - health2)), 10))

    for bullet in bullets: bullet.draw(game)
        
    pygame.display.update()#Updates the screen
#MAINLOOP STARTS HERE
font = pygame.font.SysFont('comicsans', 30, True)
bullets = []
while run:

    if not(alive1 and alive2):
       if count==0: #to ensure it only runs once in the loop
          pygame.mixer.music.stop()
          pygame.mixer.music.load(resourcePath('Shaabaashiyaan.mp3'))
          pygame.mixer.music.set_volume(0.5)
          pygame.mixer.music.play(-1)
          count+=1
    else:
       if count2==0:
          pygame.mixer.music.load(resourcePath('music.mp3'))
          pygame.mixer.music.set_volume(0.5)
          pygame.mixer.music.play(-1)
          count2+=1
          
    clock.tick(27)#Frames Per Second

    if health1<=0:
       alive1 = False
       x1,y1=0,0
    elif health2<=0:
       alive2 = False
       x2,y2=0,0

    if shootLoop > 0:
       shootLoop += 1
    if shootLoop > 7:
       shootLoop = 0
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pauseBtn.clicked():
                GAME_RESET = True if PauseScreen(game, bg).reset else False
            elif playAgainBtn and playAgainBtn.clicked():
                GAME_RESET = True

    for bullet in bullets:
       if bullet.y - bullet.radius < y2 + height2 and bullet.y + bullet.radius > y2:
          if bullet.x + bullet.radius > x2 and bullet.x - bullet.radius < x2 + width2:
             bullets.pop(bullets.index(bullet))
             health2 -= damage1
             if health2<0: health2=0
             isJump2 = True
             
       if 0 < bullet.x < 850: bullet.x+=bullet.vel
       else: bullets.pop(bullets.index(bullet))
        
    keys=pygame.key.get_pressed()#Getting the input from keyboard

    if keys[pygame.K_q] and shootLoop == 0:
       if b: facing = -1
       else: facing = 1
       
       if len(bullets) < 2:
          bullets.append(Projectile(round(x1 + width1//2), round(y1 + height1//2), 6, (0,0,0),facing))

       shootLoop = 1

    if keys[pygame.K_SPACE]: #Pause screen
        if PauseScreen(game, bg).reset:
            GAME_RESET = True
                
    elif keys[pygame.K_a] and x1>speed1 and (not(x2<x1<x2+width2) or isJump==True or isJump2):#Walking Left
        x1-=speed1
        left=True
        right=False
        
    elif keys[pygame.K_d] and x1<838-width1-speed1 and (not(x2-width2<x1<x2) or isJump==True or isJump):#Walkding Right
        x1+=speed1
        left=False
        right=True
        
    else:#Standing Idle
        left=False
        right=False
        walkcount=0
        
    if keys[pygame.K_p]: #Punching player
        punch=True
        if x2-width2<x1<x2+width2 and not(isJump) and y2<=y1<=y2+height2:
            isJump=True
            health1 -= damage2
            if health1<0: health=0
    elif keys[pygame.K_j] and x2>speed2 and (not(x1<x2<x1+width1)or isJump2==True or isJump): #Walking left
        x2-=speed2
        left2=True
        right2=False
    elif keys[pygame.K_l] and x2<838-width2-speed2 and (not(x1-width1<x2<x1) or isJump2==True or isJump):#Walking Right
        x2+=speed2
        left2=False
        right2=True
    elif keys[pygame.K_SLASH]: #Hack
        speed2 += 1
        damage2 += 1
    elif keys[pygame.K_PERIOD]: #Unhack
        speed2 = 6
        damage2 = 1
        
    else:#Standing Idle
        left2=False
        right2=False
        w2=0
    if keys[pygame.K_r]:#Restart, setting all variables to False
        GAME_RESET = True

    if GAME_RESET:
        x1,y1=50,400
        isFly=False
        isJump=False
        left=False
        right=False
        health1=10
        
        x2,y2=725,400
        isFly2=False
        isJump2=False
        left2=False
        right2=False
        health2=15
        speed2 = 6

        alive1 = alive2 = True
        
        pygame.mixer.music.stop()
        count=count2=0

        GAME_RESET = False
        playAgainBtn = None
            
    if not isFly:#Enable FLYING
        if keys[pygame.K_f]:
            isFly=True
    else:#Main Flying Loop
            if keys[pygame.K_w] and y1>0:
                y1-=speed1
            elif keys[pygame.K_s] and y1<480-height1-speed1:
                y1+=speed1
            elif keys[pygame.K_x]:#Disabling FLYING
                isFly=False
    if not isJump:#Enable JUMP
     if keys[pygame.K_w]:
         isJump=True
    else:#Main Jump loop
        if jumpcount>=-10:
            if jumpcount<0:
              negative=-1
            else:
                negative=1
            y1-=((jumpcount**2)//3)*negative
            jumpcount-=1
        else:
            isJump=False
            jumpcount=10
    if not isJump2:#Enable JUMP
     if keys[pygame.K_i]:
         isJump2=True
    else:#Main Jump loop
        if jumpcount2>=-10:
            if jumpcount2<0:
              negative=-1
            else:
                negative=1
            y2-=((jumpcount2**2)//3)*negative
            jumpcount2-=1
        else:
            isJump2=False
            jumpcount2=10
            
    if not isFly2:#Enable FLYING
        if keys[pygame.K_g]:
            isFly2=True
    else:#Main Flying Loop character 2
            if keys[pygame.K_i] and y2>0:
                y2-=speed2
            elif keys[pygame.K_k] and y2<480-height2-speed2:
                y2+=speed2
            elif keys[pygame.K_n]:#Disabling FLYING
                isFly2=False
    redrawgame()
pygame.quit()
