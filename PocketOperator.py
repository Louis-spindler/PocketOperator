import sys
import os
import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer
from pygame.locals import QUIT
import time
import csv
#threading so game dosen't die when trackes are played
import threading

csv_file = 'musicExport.csv'

#initializing pygame package and mixer
pygame.init()
pygame.mixer.init()

#variables for track buttons
number = 120
a1=a2=a3=a4=a5=a6=a7=a8=a9=a10=a11=a12=a13=a14=a15=a16=b1=b2=b3=b4=b5=b6=b7=b8=b9=b10=b11=b12=b13=b14=b15=b16=c1=c2=c3=c4=c5=c6=c7=c8=c9=c10=c11=c12=c13=c14=c15=c16=False
numOfNotesPerTrack = 16 #please change if var above are!!!!!
trackXValues = [120,180,239,239+(59*1),239+(59*2),239+(59*3),239+(59*4),239+(59*5),239+(59*6),239+(59*7),239+(59*8),239+(59*9),239+(59*10),239+(59*11),239+(59*12),239+(59*13),239+(59*14),239+(59*15)]

#list of values for the darkgrey down beat/bar markers
barLstFourFour = [1,5,9,13,19]
barLstThreeFour = [1,4,7,10,13]
#if time sig is threefour, barLst is set to barLstThreeFour
barLst = []
#bool vals for time signitures
threeFour = False
fourFour = True

#float value for tempo
tempo = 0.15

#def left/right values for destinguishing left and right clicks on the sound sample buttons
LEFTCLICK = 1
RIGHTCLICK = 3

#bool values for drop down menues for sound playing buttons
deployDropDown1=False

# Define a flag to control the play loop
playThread = None
playThreadFlag = False

#bool values for select all button and play button
selectAllButton = False
playButton = False
saveMusicButton = False
importMusicButton = False

#loading images for buttons
eraserImg = pygame.image.load('buttonTextures/eraser-icon-4.png')
eraserImg = pygame.transform.scale(eraserImg, (40,40))
selectImg = pygame.image.load('buttonTextures/select-all-icon.png')
selectImg = pygame.transform.scale(selectImg, (40,40))
playImg = pygame.image.load('buttonTextures/play-button.png')
playImg = pygame.transform.scale(playImg, (45,45))
pauseImg = pygame.image.load('buttonTextures/video-pause-button.png')
pauseImg = pygame.transform.scale(pauseImg, (45,45))
importMusicImg = pygame.image.load('buttonTextures/save-music.png')
importMusicImg = pygame.transform.scale(importMusicImg, (45,45))
saveMusicImg = pygame.image.load('buttonTextures/importMusic.png')
saveMusicImg = pygame.transform.scale(saveMusicImg, (45,45))


#making pygame window
width = 1150
height = 400 
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pocket Operator')
clock = pygame.time.Clock()


#colors 
white = (255,255,255) 
navyBlue = (50,50,50) #(255,165,0)
blue=(50,50,80)
royalPurple = (160,160,160)#(60,25,60)
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

class DropDownMenu:
    def __init__(self, items, x, y, width, height, sound, buttonText, soundText, ogSound):
        self.items = items
        self.rect = pygame.Rect(x, y, width, height)
        self.is_open = False
        self.selected_item = None
        self.sound = sound
        self.buttonText = buttonText
        self.buttonColor = darkGrey
        self.bottomRadius=5
        self.hoverColor=midGrey
        self.soundText = soundText
        self.ogSound = ogSound
    def draw(self, surface):
        pygame.draw.rect(surface, self.buttonColor, self.rect, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=self.bottomRadius, border_bottom_right_radius=self.bottomRadius)
        window.blit(makeText(self.buttonText, navyBlue, size=24), (self.rect.x + 5, self.rect.y + 5))
        window.blit(makeText(self.soundText, navyBlue, size=21), (self.rect.x + 5, self.rect.y + 30))
        if self.is_open:
            self.buttonColor=lightGrey
            self.bottomRadius=0
            for index, item in enumerate(self.items):
                item_rect = pygame.Rect(self.rect.x, self.rect.y + (index + 2) * self.rect.height/2, self.rect.width, self.rect.height/2)
                pygame.draw.rect(surface, lightGrey, item_rect)
                window.blit(makeText(item, blue, size=20), (item_rect.x + 10, item_rect.y + item_rect.height/2-10))
        if self.is_open is False:
          self.buttonColor=darkGrey
          self.bottomRadius=5
        if self.rect.collidepoint(pygame.mouse.get_pos()):
          self.buttonColor = self.hoverColor
    def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == RIGHTCLICK:  # Right-click to open dropdown
              if self.rect.collidepoint(event.pos):
                  self.is_open = not self.is_open
          elif event.button == LEFTCLICK and self.is_open:  # Left-click for selecting options
              if self.is_open:
                  for index, item in enumerate(self.items):
                      item_rect = pygame.Rect(self.rect.x, self.rect.y + (index + 2) * self.rect.height/2, self.rect.width, self.rect.height/2)
                      if item_rect.collidepoint(event.pos):
                          self.selected_item = item
                          self.is_open = False
                          if item == "Mute":
                              self.sound.set_volume(0.0)
                              print(f"muting {self.soundText}")
                          elif item == "Change":
                              print(f"changing {self.soundText}")
                              self.changeSound()
                              self.soundText = "New Sound"
                          elif item == "Reset":
                              print(f"resetting {self.soundText}")
                              self.sound = self.ogSound
                              self.soundText = ''
                          elif item == "3/4":
                              threeFour = True
                              fourFour = False
                              print("3/4 is good at fortnight: "+str(threeFour))
                              
                          elif item == "4/4":
                              fourFour = True
                              threeFour = False
                              print("4/4 is good at fortnight: "+str(fourFour))

                  if self.rect.collidepoint(event.pos):
                    self.sound.play()
                    self.is_open=not self.is_open
          elif event.button == LEFTCLICK and not self.is_open:  # Left-click to play sound
              if self.rect.collidepoint(event.pos):
                  self.sound.play()
    def changeSound(self):
        # Open a file explorer window to choose a new sound file
        file_path = self.file_dialog()
        if file_path:
            # Load the new sound and update the associated sound
            new_sound = pygame.mixer.Sound(file_path)
            self.sound = new_sound
            print(f"Changed sound for {self.soundText} to {file_path}")
            
            # Update the corresponding track buttons with the new sound
            if self.soundText == "High Hat":
                global closedHighHat
                closedHighHat = new_sound
            elif self.soundText == "Snare Drum":
                global snareDrum
                snareDrum = new_sound
            elif self.soundText == "Bass Drum":
                global bassDrum
                bassDrum = new_sound
    def file_dialog(self):
        # Open a file dialog to choose a new sound file
        if os.name == 'nt':  # Windows
            from tkinter import filedialog, Tk
            root = Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.askopenfilename(filetypes=[("Sound Files", "*.wav;*.mp3")])
            root.destroy()
        else:  # Mac or Linux
            import subprocess
            file_path = subprocess.run(['osascript', '-e', 'POSIX path of (choose file of type {"public.audio"})'], stdout=subprocess.PIPE, text=True).stdout.strip()

        return file_path
    
# class KeySigSelector:
#   def __init__(self,pos: tuple,size: tuple,buttons=["3/4","4/4"]):
#     self.pos = pos
#     self.size = size
#     self.buttons = buttons
#     self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
#   def draw(self):
#     for index, item in enumerate(self.buttons):
#       item_rect = pygame.Rect(self.rect.x, self.rect.y + (index + 2) * self.rect.height/2, self.rect.width, self.rect.height/2)
#       pygame.draw.rect(window, lightGrey, item_rect)
#       window.blit(makeText(item, blue, size=20), (item_rect.x + 10, item_rect.y + item_rect.height/2-10))

#function that creates text
def makeText(text="text", color=(255, 255, 255), font='Corbel', size=28):
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
    if fourFour:
      numOfNotesPerTrack = 16
    if threeFour:
       numOfNotesPerTrack = 15
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
                if fourFour:
                  if note == 15:
                    if a16 is True:
                        closedHighHat.play()
                    if b16 is True:
                        snareDrum.play()
                    if c16 is True:
                        bassDrum.play()
                
            check_for_track_sounds()

#create a way to save beats to use for further use****************************************************
def drawSaveMusicButton():
  drawBoolButton(saveMusicButton, 1088, 340, 50, 50, darkGrey,lightGrey,darkGrey,0,0,roundness=8)
  window.blit(saveMusicImg, (1090,340))
def drawImportMusicButton():
  drawBoolButton(importMusicButton, 1030, 340, 50, 50, darkGrey,lightGrey,darkGrey,0,0,roundness=8)
  window.blit(importMusicImg, (1032,340))

#Load Sounds
snareDrum, snareDrumText = pygame.mixer.Sound("drumSamples/newSnare.wav"), "Snare Drum"
closedHighHat, closedHighHatText = pygame.mixer.Sound("drumSamples/newClosedHiHat.mp3"), "High Hat"
bassDrum, bassDrumText = pygame.mixer.Sound("drumSamples/newBassDrum.mp3"), "Bass Drum"

#create slider object names tempoSlider that controls tempo.
tempoSlider = Slider((185,370), (100,20), 0.5, 0, 100)

#create slider objects for track volume sliders
track1VolumeSlider = Slider((1100,35), (50,20), 0.5, 0, 1)
track2VolumeSlider = Slider((1100,95), (50,20), 0.5, 0, 1)
track3VolumeSlider = Slider((1100,155), (50,20), 0.5, 0, 1)

#create dropdout menu object
menu_items = ["Change", "Reset"]
dropdownMenu1 = DropDownMenu(menu_items, 12, 12, 100, 50, closedHighHat, "Sound 1", closedHighHatText, closedHighHat)
dropdownMenu2 = DropDownMenu(menu_items, 12, 72, 100, 50, snareDrum, "Sound 2", snareDrumText, snareDrum)
dropdownMenu3 = DropDownMenu(menu_items, 12, 132, 100, 50, bassDrum, "Sound 3", bassDrumText, bassDrum)

#using drop down menue class to create key signature selector
keySigSelector = DropDownMenu(["4/4","3/4"],  1075, 190, 50, 40, snareDrum, "T-Sig", "", snareDrum)


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

      # Handle file dialog events
      pygame.event.pump()

      #checking for play sound button / drop down menu events
      dropdownMenu3.handle_event(event)
      dropdownMenu2.handle_event(event)
      dropdownMenu1.handle_event(event)
      keySigSelector.handle_event(event)
      
      if event.type == pygame.MOUSEBUTTONDOWN: 
        
        #check for play button presses!!!!!!! Threading makes play back not incredably glitchy/anoying
        if 72 <= mouse[0] <= 72+50 and 340 <= mouse[1] <= 340+50:
            playButton = not playButton
            playThreadFlag = not playThreadFlag
            if playThreadFlag:
                playThread = threading.Thread(target=playTracks)
                playThread.start()
            else:
                playThread.join()  

        # #if statment so the user can't edit tracks while playing them
        # if playButton is False:
        #*2 indent
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
              #checking if time signature is four four time
              if fourFour:
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
            if fourFour:
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
            if fourFour:
              if num == trackXValues[15]:
                c16 = not c16
            bassDrum.play()        
        #check for save music button press
        if 1088 <= mouse[0] <= 1088+50 and 340 <= mouse[1] <= 340+50:
            print('Louis is chill like dat')
            saveMusicButton = not saveMusicButton

        # else:
        #     print("playing music! Can not edit tracks while playing ):")
            
        
    #stores the (x,y) tuple coordinates of mouse. mouseClick returns bool when mouse dose [0] left click or [2] right click
    mouse = pygame.mouse.get_pos() 
    mouseClick = pygame.mouse.get_pressed()

    #changing down beat markers for corrisponding time signature
    if fourFour:
      barLst = barLstFourFour
      #print("jhon")
    if threeFour:
      barLst = barLstThreeFour
      #print("john")
    def drawFirstTrackRow():
      vars = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16]
      x = 121
      y = 12
      num = 0
      for var in vars:
        num+=1
        if num in barLst:
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
        if num in barLst:
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
        if num in barLst:
          drawBoolButton(var,x,y,50,50,darkerGrey,darkGrey,brightGrey,0,0)
        else:
          drawBoolButton(var,x,y,50,50,darkGrey,lightGrey,brightGrey,0,0)
        x += 59
    drawThirdTrackRow()
  
    #draw play sound drop down menus
    dropdownMenu3.draw(window)
    dropdownMenu2.draw(window)
    dropdownMenu1.draw(window)
    keySigSelector.draw(window)

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
    
    #Draws Save Music Button
    drawSaveMusicButton()
    if saveMusicButton is True:
      print("i am so kule")
      musicButtonValues = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16] 
      with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow('music')
        # Write data
        writer.writerow(musicButtonValues)
      saveMusicButton = False
    drawImportMusicButton()
    if importMusicButton is True:
      print("exporting ur face")

      
      
    

    #draw slider and check for tempo slider draging
    tempoSlider.render(window)
    window.blit(makeText(text="BPM", color=darkGrey, size=21), (170,342))#superimposing tempo slider text
    if tempoSlider.containerRect.collidepoint(mouse) and mouseClick[0]:
      tempoSlider.moveSlider(mouse)
    tempo = tempoSlider.getValue() * 0.005
    
    #drawing volume sliders for indivituial tracks
    for trackSlider in [track1VolumeSlider,track2VolumeSlider,track3VolumeSlider]:   
      trackSlider.render(window)
      if trackSlider.containerRect.collidepoint(mouse) and mouseClick[0]:
        trackSlider.moveSlider(mouse)
      TKVolume = trackSlider.getValue() 
      if trackSlider == track1VolumeSlider:
          closedHighHat.set_volume(TKVolume)
      if trackSlider == track2VolumeSlider:
          snareDrum.set_volume(TKVolume)
      if trackSlider == track3VolumeSlider:
          bassDrum.set_volume(TKVolume)

    
    pygame.display.update()