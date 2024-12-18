import sys
import pygame
import numpy
from constants import *


#PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')

centerCords = []
closestX, closestY = 0,0
currentPlayer = 1   
all_rectangles = []
xColour = pygame.Color(255, 0, 0)
circleColour = pygame.Color(0, 0, 255)

def main():
    prepareBoard()
    centerCords = divideScreen()
    currentPlayer = 1
    while True:
        for event in pygame.event.get():
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                closestX, closestY = drawShapeInRightSquare(centerCords, mouseX, mouseY)
                currentPlayer = drawRightShape(screen, xColour, circleColour ,closestX, closestY, currentPlayer)
                

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def prepareBoard():
    pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(WIDTH/3, 1), pygame.Vector2(WIDTH/3, HEIGHT), SHAPESWIDTH)
    pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(WIDTH/3 * 2, 1), pygame.Vector2(WIDTH/3 *2, HEIGHT), SHAPESWIDTH)
    pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(1 , HEIGHT/3), pygame.Vector2(WIDTH, HEIGHT/3), SHAPESWIDTH)
    pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(1, HEIGHT/3*2), pygame.Vector2(WIDTH, HEIGHT/3*2), SHAPESWIDTH)

def divideScreen():
    hasDivided = False

    if(hasDivided == False):
        dx = 200.
        dy = 200.
        N = 3
    
        centers = numpy.mgrid[dx/2:N*dx:dx, dy/2:N*dy:dy]
        numpy.rollaxis(centers, 0, centers.ndim)
        centers.shape
        (5, 5, 2)
        hasDivided = True
        return centers
    
def drawShapeInRightSquare(centersList, mouseXpos, mouseYpos):
    xDifference, yDifference = 0, 0
    centerX, centerY = 0, 0
    closestXpos, closestYpos = 0, 0
    howManyLists = 0
    for outer_list in centersList:
        for inner_list in outer_list:
            for element in inner_list: 
                if (howManyLists < 9 ):
                    if (mouseXpos > element):
                        xDifference = mouseXpos - element
                    elif(mouseXpos < element):
                        xDifference = element - mouseXpos

                    if(centerX == 0):
                        centerX = xDifference
                        closestXpos = element
                    elif(centerX > xDifference):
                        centerX = xDifference
                        closestXpos = element
                
                elif(howManyLists >= 9):
                    if (mouseYpos > element):
                        yDifference = mouseYpos - element
                    elif(mouseYpos < element):
                        yDifference = element - mouseYpos

                    if(centerY == 0):
                        centerY = yDifference
                        closestYpos = element
                    elif(centerY > yDifference):
                        centerY = yDifference
                        closestYpos = element
                howManyLists = howManyLists +1
    return closestXpos, closestYpos

def switchPlayers(lastPlayer):
    if (lastPlayer == 1):
        lastPlayer = 2
    elif(lastPlayer == 2):
        lastPlayer = 1
    return lastPlayer

def drawRightShape(screenSurface, colourOfX, colourOfCircle, posX, posY, playerToPlay):
    if(playerToPlay == 1):
        newRect = pygame.Rect(posX, posY, 200, 200)
        if(checkIfBlockIsEmpty(newRect, all_rectangles) == True):
            all_rectangles.append(newRect)
            pygame.draw.circle(screenSurface, colourOfCircle, (posX, posY), DISTANCEFROMCENTER, SHAPESWIDTH) 
            playerToPlay = switchPlayers(playerToPlay)
    elif(playerToPlay == 2):
        newRect = pygame.Rect(posX, posY, 200, 200)
        if(checkIfBlockIsEmpty(newRect, all_rectangles) == True):
            all_rectangles.append(newRect)
            pygame.draw.line(screenSurface, colourOfX, (posX - DISTANCEFROMCENTER,posY - DISTANCEFROMCENTER), (posX + DISTANCEFROMCENTER, posY + DISTANCEFROMCENTER), SHAPESWIDTH)
            pygame.draw.line(screenSurface, colourOfX, (posX - DISTANCEFROMCENTER,posY + DISTANCEFROMCENTER), (posX + DISTANCEFROMCENTER, posY - DISTANCEFROMCENTER), SHAPESWIDTH)
            playerToPlay = switchPlayers(playerToPlay)
    return playerToPlay
        
def checkIfBlockIsEmpty(newRectangle, allOfRectangles: list):
    if(allOfRectangles.__len__() == 0):
        return True
    for rectangle in allOfRectangles:
        if (pygame.Rect.colliderect(rectangle, newRectangle)):
            
            return False
    return True        

main()
