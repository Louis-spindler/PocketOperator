import sys
import pygame
from pygame import mixer
from pygame.locals import QUIT
import time
#threading so game dosen't die when trackes are played
import threading

#initializing pygame packages
pygame.init()
pygame.mixer.init()

#variables for track button
number = 120
a1=a2=a3=a4=a5=a6=a7=a8=b1=b2=b3=b4=b5=b6=b7=b8=c1=c2=c3=c4=c5=c6=c7=c8=False
numOfNotesPerTrack = 8 #please change if var above are!!!!!
trackXValues = [120,180,239,298,357,416,475,534]

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
width = 800
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
  def __init__(self, x, y, w, h, circleX, Value):
    self.sliderRect = pygame.Rect(x, y, w, h)
    self.circleX = circleX = x + w/2
    self.circleY = y + (h/2)
    self.Value = Value
  def getVal(self):
    return self.Value
  def draw(self, window, x, y):
    pygame.draw.rect(window, darkGrey, self.sliderRect, border_radius=5)
    pygame.draw.circle(window, darkerGrey, (self.circleX, self.circleY),14)
tempoSlider = Slider(300, 350, 100, 20, 16, tempo)
  
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
            check_for_track_sounds()


#Load Sounds
snareDrum = pygame.mixer.Sound("drumSamples/snareDrumHit.mp3")
closedHighHat = pygame.mixer.Sound("drumSamples/closedHighHatHit.mp3")
bassDrum = pygame.mixer.Sound("drumSamples/bassDrumHit.mp3")


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
              a1=a2=a3=a4=a5=a6=a7=a8=b1=b2=b3=b4=b5=b6=b7=b8=c1=c2=c3=c4=c5=c6=c7=c8=True
            else:
              a1=a2=a3=a4=a5=a6=a7=a8=b1=b2=b3=b4=b5=b6=b7=b8=c1=c2=c3=c4=c5=c6=c7=c8=False
          
          #for loop checking for first track presses
          for num in trackXValues:
              if num <= mouse[0] <= num+50 and 12 <= mouse[1] <= 12+50:
                print(f"a{num} button pressed")
                if num == 120:
                  a1 = not a1
                if num == 180:
                  a2 = not a2
                if num == 239:
                  a3 = not a3
                if num == 298:
                  a4 = not a4
                if num == 357:
                  a5 = not a5
                if num == 416:
                  a6 = not a6
                if num == 475:
                  a7 = not a7
                if num == 534:
                  a8 = not a8
                #play corisponding sound for funzies enever button is pressed
                closedHighHat.play()
          #for loop checking for second track presses
          for num in trackXValues:
            if num <= mouse[0] <= num+50 and 72 <= mouse[1] <= 72+50:
              print(f"b{num} button pressed")
              if num == 120:
                b1 = not b1
              if num == 180:
                b2 = not b2
              if num == 239:
                b3 = not b3
              if num == 298:
                b4 = not b4
              if num == 357:
                b5 = not b5
              if num == 416:
                b6 = not b6
              if num == 475:
                b7 = not b7
              if num == 534:
                b8 = not b8
              snareDrum.play()
          #for loop checking for third track presses
          for num in trackXValues:
            if num <= mouse[0] <= num+50 and 132 <= mouse[1] <= 132+50:
              print(f"c{num} button pressed")
              if num == 120:
                c1 = not c1
              if num == 180:
                c2 = not c2
              if num == 239:
                c3 = not c3
              if num == 298:
                c4 = not c4
              if num == 357:
                c5 = not c5
              if num == 416:
                c6 = not c6
              if num == 475:
                c7 = not c7
              if num == 534:
                c8 = not c8
              bassDrum.play()
                
        else:
            print("playing music! Can not edit tracks while playing ):")
            
        
    #stores the (x,y) tuple coordinates of mouse
    mouse = pygame.mouse.get_pos() 

    def drawFirstTrackRow():
      vars = [a1,a2,a3,a4,a5,a6,a7,a8]
      x = 121
      y = 12
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9]:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawFirstTrackRow()
    def drawSecondTrackRow():
      vars = [b1,b2,b3,b4,b5,b6,b7,b8]
      x = 121
      y = 72
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9]:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawSecondTrackRow()
    def drawThirdTrackRow():
      vars = [c1,c2,c3,c4,c5,c6,c7,c8]
      x = 121
      y = 132
      num = 0
      for var in vars:
        num+=1
        if num in [1,5,9]:
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

    #Draw Tempo Slider
    tempoSlider.draw(window, 300, 300)

    pygame.display.update()
  