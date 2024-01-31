import sys
import pygame
from pygame import mixer
from pygame.locals import QUIT
import time
#threading so game dosen't die when trackes are played
import threading

#initializing pygame package and mixer
pygame.init()
pygame.mixer.init()

#variables for track button
number = 120
a1=a2=a3=a4=a5=a6=a7=a8=a9=a10=a11=a12=a13=a14=a15=a16=b1=b2=b3=b4=b5=b6=b7=b8=b9=b10=b11=b12=b13=b14=b15=b16=c1=c2=c3=c4=c5=c6=c7=c8=c9=c10=c11=c12=c13=c14=c15=c16=False
numOfNotesPerTrack = 16 #please change if var above are!!!!!
trackXValues = [120,180,239,239+(59*1),239+(59*2),239+(59*3),239+(59*4),239+(59*5),239+(59*6),239+(59*7),239+(59*8),239+(59*9),239+(59*10),239+(59*11),239+(59*12),239+(59*13),239+(59*14),239+(59*15)]

#float value for tempo
tempo = 0.15

# Define a flag to control the play loop
playThread = None
playThreadFlag = False

#bool values for select all button and play button
selectAllButton = False
playButton = False

#loading images for buttons
eraserImg = pygame.image.load('buttonTextures/eraser-icon-4.png')
eraserImg = pygame.transform.scale(eraserImg, (40,40))
selectImg = pygame.image.load('buttonTextures/select-all-icon.png')
selectImg = pygame.transform.scale(selectImg, (40,40))
playImg = pygame.image.load('buttonTextures/play-button.png')
playImg = pygame.transform.scale(playImg, (45,45))
pauseImg = pygame.image.load('buttonTextures/video-pause-button.png')
pauseImg = pygame.transform.scale(pauseImg, (45,45))

#making pygame window
width = 1150
height = 400 
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pocket Operator')
clock = pygame.time.Clock()

#colors 
white = (255,255,255) 
navyBlue = (0,0,60) #(255,165,0)
royalPurple = (60,25,60)
lightGrey = (130,130,130) 
brightGrey = (180,180,180)
midGrey = (140,140,140)
darkGrey = (100,100,100) 
darkerGrey = (70,70,70)


#Slider Class
class Slider:
  def __init__(self, pos: tuple, size: tuple, initialValue: float, min: int, max: int):
    self.pos = pos
    self.size = size

    self.sliderLeftPos = self.pos[0] - (size[0]//2)
    self.sliderRightPos = self.pos[0] + (size[0]//2)
    self.sliderTopPos = self.pos[1] - (size[1]//2)
    
    self.min = min
    self.max = max
    self.initialValue = (self.sliderRightPos-self.sliderLeftPos)*initialValue #percentage

    self.containerRect = pygame.Rect(self.sliderLeftPos, self.sliderTopPos, self.size[0], self.size[1])
    self.buttonRect = pygame.Rect(self.sliderLeftPos + self.initialValue - 5, self.sliderTopPos, 10, self.size[1])
  def render(self, screen):
    pygame.draw.rect(screen, darkGrey, self.containerRect, border_radius=10)
    pygame.draw.rect(screen, darkerGrey, self.buttonRect, border_radius=10)
  def moveSlider(self, mousePos: tuple):
    self.buttonRect.centerx = mousePos[0]
  def getValue(self):
    valRange = self.sliderLeftPos - self.sliderRightPos - 1 #-1 for padding. pixle col to exact
    buttonVal = self.buttonRect.centerx - self.sliderLeftPos
    value = (buttonVal/valRange)*(self.max-self.min)+self.min
    return value*-1


#function that creates text
def makeText(text="text", color=(255,255,255), font='Corbel', size=28):
  smallFont = pygame.font.SysFont(font, size) 
  finalText = smallFont.render(text, True, color)
  return finalText
  
#function that draws button(s)
def drawButton(text,xCoor,yCoor,width,height,bgColor,bgHoverColor,textXcoorAdd,textYcoorAdd,roundness=8):
  #checking for mouse hovering over button
  if xCoor <= mouse[0] <= xCoor+width and yCoor <= mouse[1] <= yCoor+height: 
    pygame.draw.rect(window,bgHoverColor,[xCoor,yCoor,width,height], border_radius=roundness) 
  else: 
    pygame.draw.rect(window,bgColor,[xCoor,yCoor,width,height], border_radius=roundness) 
  #superimposing the text onto our button 
  window.blit(text, (xCoor/2+textXcoorAdd,yCoor/2+textYcoorAdd)) 

#function that uses drawButton() to create a button with a bool value
def drawBoolButton(BoolVar,xCoor,yCoor,width,height,unselectedColor,hoverColor,selectedColor,textXcoorAdd,textYcoorAdd,roundness=8,text=""):
  if BoolVar is True:
    drawButton(makeText(text=text),xCoor,yCoor,width,height,selectedColor,selectedColor,textXcoorAdd,textYcoorAdd)
  elif BoolVar is False:
    drawButton(makeText(text=text),xCoor,yCoor,width,height,unselectedColor,hoverColor,textXcoorAdd,textYcoorAdd)

#function that draws select all button
def drawSelectAllButton():
    drawBoolButton(selectAllButton,12,340,50,50,darkGrey,lightGrey,darkGrey,0,0)
    if selectAllButton is True:
        window.blit(eraserImg, (16, 342))
    elif selectAllButton is False:
        window.blit(selectImg, (17, 345))

#function used when run button is pressed
def playTracks():
    global playThreadFlag
    while playThreadFlag:
        for note in range(numOfNotesPerTrack):
            time.sleep(tempo)
            def check_for_track_sounds():
                if note == 0:
                    if a1 is True:
                        closedHighHat.play()
                    if b1 is True:
                        snareDrum.play()
                    if c1 is True:
                        bassDrum.play()
                if note == 1:
                    if a2 is True:
                        closedHighHat.play()
                    if b2 is True:
                        snareDrum.play()
                    if c2 is True:
                        bassDrum.play()
                if note == 2:
                    if a3 is True:
                        closedHighHat.play()
                    if b3 is True:
                        snareDrum.play()
                    if c3 is True:
                        bassDrum.play()
                if note == 3:
                    if a4 is True:
                        closedHighHat.play()
                    if b4 is True:
                        snareDrum.play()
                    if c4 is True:
                        bassDrum.play()
                if note == 4:
                    if a5 is True:
                        closedHighHat.play()
                    if b5 is True:
                        snareDrum.play()
                    if c5 is True:
                        bassDrum.play()
                if note == 5:
                    if a6 is True:
                        closedHighHat.play()
                    if b6 is True:
                        snareDrum.play()
                    if c6 is True:
                        bassDrum.play()
                if note == 6:
                    if a7 is True:
                        closedHighHat.play()
                    if b7 is True:
                        snareDrum.play()
                    if c7 is True:
                        bassDrum.play()
                if note == 7:
                    if a8 is True:
                        closedHighHat.play()
                    if b8 is True:
                        snareDrum.play()
                    if c8 is True:
                        bassDrum.play()
                if note == 8:
                    if a9 is True:
                        closedHighHat.play()
                    if b9 is True:
                        snareDrum.play()
                    if c9 is True:
                        bassDrum.play()
                if note == 9:
                    if a10 is True:
                        closedHighHat.play()
                    if b10 is True:
                        snareDrum.play()
                    if c10 is True:
                        bassDrum.play()
                if note == 10:
                    if a11 is True:
                        closedHighHat.play()
                    if b11 is True:
                        snareDrum.play()
                    if c11 is True:
                        bassDrum.play()
                if note == 11:
                    if a12 is True:
                        closedHighHat.play()
                    if b12 is True:
                        snareDrum.play()
                    if c12 is True:
                        bassDrum.play()
                if note == 12:
                    if a13 is True:
                        closedHighHat.play()
                    if b13 is True:
                        snareDrum.play()
                    if c13 is True:
                        bassDrum.play()
                if note == 13:
                    if a14 is True:
                        closedHighHat.play()
                    if b14 is True:
                        snareDrum.play()
                    if c14 is True:
                        bassDrum.play()
                if note == 14:
                    if a15 is True:
                        closedHighHat.play()
                    if b15 is True:
                        snareDrum.play()
                    if c15 is True:
                        bassDrum.play()
                if note == 15:
                    if a16 is True:
                        closedHighHat.play()
                    if b16 is True:
                        snareDrum.play()
                    if c16 is True:
                        bassDrum.play()
            check_for_track_sounds()


#Load Sounds
snareDrum = pygame.mixer.Sound("drumSamples/newSnare.wav")
closedHighHat = pygame.mixer.Sound("drumSamples/newClosedHiHat.mp3")
bassDrum = pygame.mixer.Sound("drumSamples/newBassDrum.mp3")

#create slider object names tempoSlider thant controls tempo.
tempoSlider = Slider((185,365), (100,20), 0.5, 0, 100)

#game loop
gameLoop = True
while gameLoop:
    
  #set frame rate
    clock.tick(30)
    #window color
    window.fill(royalPurple) 
  
    #loop checking for events(mouse clicks,key presses)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN: 
        #check for Sound 1, 2, and 3 button press
        if 12 <= mouse[0] <= 12+100 and 12 <= mouse[1] <= 12+40: 
            print("playing sound 1")
            closedHighHat.play()
        elif 12 <= mouse[0] <= 12+100 and 72 <= mouse[1] <= 72+50:
            print("playing sound 2")
            snareDrum.play()
        elif 12 <= mouse[0] <= 12+100 and 132 <= mouse[1] <= 132+50:
            print("playing sound 3")
            bassDrum.play()

        #check for play button presses!!!!!!! Threading makes play back not incredably glitchy/anoying
        if 72 <= mouse[0] <= 72+50 and 340 <= mouse[1] <= 340+50:
            playButton = not playButton
            playThreadFlag = not playThreadFlag
            if playThreadFlag:
                playThread = threading.Thread(target=playTracks)
                playThread.start()
            else:
                playThread.join()  

        #if statment so the user can't edit tracks while playing them
        if playButton is False:

            #check for clear all / select all button presses
            if 12 <= mouse[0] <= 12+50 and 340 <= mouse[1] <= 340+50:
              selectAllButton = not selectAllButton
              if selectAllButton is True:
                a1=a2=a3=a4=a5=a6=a7=a8=a9=a10=a11=a12=a13=a14=a15=a16=b1=b2=b3=b4=b5=b6=b7=b8=b9=b10=b11=b12=b13=b14=b15=b16=c1=c2=c3=c4=c5=c6=c7=c8=c9=c10=c11=c12=c13=c14=c15=c16=True

              else:
                a1=a2=a3=a4=a5=a6=a7=a8=a9=a10=a11=a12=a13=a14=a15=a16=b1=b2=b3=b4=b5=b6=b7=b8=b9=b10=b11=b12=b13=b14=b15=b16=c1=c2=c3=c4=c5=c6=c7=c8=c9=c10=c11=c12=c13=c14=c15=c16=False

            
            #for loop checking for first track presses
            for num in trackXValues:
                if num <= mouse[0] <= num+50 and 12 <= mouse[1] <= 12+50:
                  print(f"a{num} button pressed")
                  if num == trackXValues[0]:
                    a1 = not a1
                  if num == trackXValues[1]:
                    a2 = not a2
                  if num == trackXValues[2]:
                    a3 = not a3
                  if num == trackXValues[3]:
                    a4 = not a4
                  if num == trackXValues[4]:
                    a5 = not a5
                  if num == trackXValues[5]:
                    a6 = not a6
                  if num == trackXValues[6]:
                    a7 = not a7
                  if num == trackXValues[7]:
                    a8 = not a8
                  if num == trackXValues[8]:
                    a9 = not a9
                  if num == trackXValues[9]:
                    a10 = not a10
                  if num == trackXValues[10]:
                    a11 = not a11
                  if num == trackXValues[11]:
                    a12 = not a12
                  if num == trackXValues[12]:
                    a13 = not a13
                  if num == trackXValues[13]:
                    a14 = not a14
                  if num == trackXValues[14]:
                    a15 = not a15
                  if num == trackXValues[15]:
                    a16 = not a16
                  #play corisponding sound for funzies enever button is pressed
                  closedHighHat.play()
            #for loop checking for second track presses
            for num in trackXValues:
              if num <= mouse[0] <= num+50 and 72 <= mouse[1] <= 72+50:
                print(f"b{num} button pressed")
                if num == trackXValues[0]:
                  b1 = not b1
                if num == trackXValues[1]:
                  b2 = not b2
                if num == trackXValues[2]:
                  b3 = not b3
                if num == trackXValues[3]:
                  b4 = not b4
                if num == trackXValues[4]:
                  b5 = not b5
                if num == trackXValues[5]:
                  b6 = not b6
                if num == trackXValues[6]:
                  b7 = not b7
                if num == trackXValues[7]:
                  b8 = not b8
                if num == trackXValues[8]:
                  b9 = not b9
                if num == trackXValues[9]:
                  b10 = not b10
                if num == trackXValues[10]:
                  b11 = not b11
                if num == trackXValues[11]:
                  b12 = not b12
                if num == trackXValues[12]:
                  b13 = not b13
                if num == trackXValues[13]:
                  b14 = not b14
                if num == trackXValues[14]:
                  b15 = not b15
                if num == trackXValues[15]:
                  b16 = not b16
                snareDrum.play()
            #for loop checking for third track presses
            for num in trackXValues:
              if num <= mouse[0] <= num+50 and 132 <= mouse[1] <= 132+50:
                print(f"c{num} button pressed")
                if num == trackXValues[0]:
                  c1 = not c1
                if num == trackXValues[1]:
                  c2 = not c2
                if num == trackXValues[2]:
                  c3 = not c3
                if num == trackXValues[3]:
                  c4 = not c4
                if num == trackXValues[4]:
                  c5 = not c5
                if num == trackXValues[5]:
                  c6 = not c6
                if num == trackXValues[6]:
                  c7 = not c7
                if num == trackXValues[7]:
                  c8 = not c8
                if num == trackXValues[8]:
                  c9 = not c9
                if num == trackXValues[9]:
                  c10 = not c10
                if num == trackXValues[10]:
                  c11 = not c11
                if num == trackXValues[11]:
                  c12 = not c12
                if num == trackXValues[12]:
                  c13 = not c13
                if num == trackXValues[13]:
                  c14 = not c14
                if num == trackXValues[14]:
                  c15 = not c15
                if num == trackXValues[15]:
                  c16 = not c16
                bassDrum.play()
                
        else:
            print("playing music! Can not edit tracks while playing ):")
            
        
    #stores the (x,y) tuple coordinates of mouse. mouseClick returns bool when mouse dose [0] left click or [2] right click
    mouse = pygame.mouse.get_pos() 
    mouseClick = pygame.mouse.get_pressed()

    def drawFirstTrackRow():
      vars = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16]
      x = 121
      y = 12
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9,13,19]:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawFirstTrackRow()
    def drawSecondTrackRow():
      vars = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16]
      x = 121
      y = 72
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9,13,19]:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawSecondTrackRow()
    def drawThirdTrackRow():
      vars = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16]
      x = 121
      y = 132
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9,13,19]:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawThirdTrackRow()
  
    #Draw sound 1 button
    drawButton(makeText(text="Sound 1", color=navyBlue),12,12,100,50,darkGrey,lightGrey, 18, 22.5)
    #Draw sound 2 button
    drawButton(makeText(text="Sound 2", color=navyBlue),12,72,100,50,darkGrey,lightGrey, 18, 52.5)
    #Draw sound 3 button
    drawButton(makeText(text="Sound 3", color=navyBlue),12,132,100,50,darkGrey,lightGrey, 18, 80)
  
    #Draw clear all button/select all button
    drawSelectAllButton()

    #Draws play button
    def drawPlayButton():
      drawBoolButton(playButton,72,340,50,50,darkGrey,lightGrey,darkGrey,0,0)
      if playButton is True:
        window.blit(pauseImg, (74, 342))
      elif playButton is False:
        window.blit(playImg, (74, 342))
    drawPlayButton()

    #draw slider and check for tempo slider draging
    tempoSlider.render(window)
    if tempoSlider.containerRect.collidepoint(mouse) and mouseClick[0]:
      tempoSlider.moveSlider(mouse)
    tempo = tempoSlider.getValue() * 0.005
    
    
    

    
    pygame.display.update()
  