import sys
import pygame
import numpy as np
from constants import *


#PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')

all_rectangles = []
centerCords = []
boardState = [[0,0,0],[0,0,0],[0,0,0]]

def main():
    gameOver = False
    closestX, closestY = 0,0
    currentPlayer = 1   
    all_rectangles.clear()
    boardState = np.zeros((ROWS, COLUMNS))
    
    postGame = False
    prepareBoard()
    centerCords = divideScreen()
    currentPlayer = 1
    
    while True:
        for event in pygame.event.get():
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN and postGame == False:
                mouseX, mouseY = pygame.mouse.get_pos()
                closestX, closestY = drawShapeInRightSquare(centerCords, mouseX, mouseY)
                
                currentPlayer, boardState = drawRightShape(screen, closestX, closestY, boardState, currentPlayer)
                
                gameOver = winCheck(boardState, True)
                
                postGame = postGameCheck(boardState, gameOver)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and postGame == True:
                    main()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def prepareBoard():
    screen.fill(pygame.Color(0,0,0))
    boardColour = pygame.Color(112, 41, 99)
    pygame.draw.line(screen, boardColour, pygame.Vector2(WIDTH/3, 1), pygame.Vector2(WIDTH/3, HEIGHT), SHAPESWIDTH)
    pygame.draw.line(screen, boardColour, pygame.Vector2(WIDTH/3 * 2, 1), pygame.Vector2(WIDTH/3 *2, HEIGHT), SHAPESWIDTH)
    pygame.draw.line(screen, boardColour, pygame.Vector2(1 , HEIGHT/3), pygame.Vector2(WIDTH, HEIGHT/3), SHAPESWIDTH)
    pygame.draw.line(screen, boardColour, pygame.Vector2(1, HEIGHT/3*2), pygame.Vector2(WIDTH, HEIGHT/3*2), SHAPESWIDTH)
    

def divideScreen():
    hasDivided = False

    if(hasDivided == False):
        dx = SQUARE_SIZE
        dy = SQUARE_SIZE
        N = 3
    
        centers = np.mgrid[dx/2:N*dx:dx, dy/2:N*dy:dy]
        np.rollaxis(centers, 0, centers.ndim)
        centers.shape
        (5, 5, 2)
        hasDivided = True
        return centers
    
def drawShapeInRightSquare(centersList: list, mouseXpos, mouseYpos):
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

def drawRightShape(screenSurface, posX, posY, gameState, playerToPlay):
    if(playerToPlay == 1):
        newRect = pygame.Rect(posX, posY, SQUARE_SIZE, SQUARE_SIZE)
        if(checkIfBlockIsEmpty(newRect, all_rectangles) == True):
            all_rectangles.append(newRect)
            pygame.draw.circle(screenSurface, CIRC_COLOR, (posX, posY), DISTANCEFROMCENTER, SHAPESWIDTH) 
            row, column = convCordToRowAndColumn(posX, posY)
            gameState = markSquare(row, column,gameState, playerToPlay)
            playerToPlay = switchPlayers(playerToPlay)
    elif(playerToPlay == 2):
        newRect = pygame.Rect(posX, posY, SQUARE_SIZE, SQUARE_SIZE)
        if(checkIfBlockIsEmpty(newRect, all_rectangles) == True):
            all_rectangles.append(newRect)
            row, column = convCordToRowAndColumn(posX, posY)
            gameState = markSquare(row, column,gameState, playerToPlay)
            pygame.draw.line(screenSurface, X_COLOR, (posX - DISTANCEFROMCENTER,posY - DISTANCEFROMCENTER), (posX + DISTANCEFROMCENTER, posY + DISTANCEFROMCENTER), SHAPESWIDTH)
            pygame.draw.line(screenSurface, X_COLOR, (posX - DISTANCEFROMCENTER,posY + DISTANCEFROMCENTER), (posX + DISTANCEFROMCENTER, posY - DISTANCEFROMCENTER), SHAPESWIDTH)
            playerToPlay = switchPlayers(playerToPlay)
    return playerToPlay, gameState
        
def checkIfBlockIsEmpty(newRectangle, allOfRectangles: list):
    if(allOfRectangles.__len__() == 0):
        return True
    for rectangle in allOfRectangles:
        if (pygame.Rect.colliderect(rectangle, newRectangle)):
            
            return False
    return True        

def postGameCheck(gameState: list, gameOver):
    gameStateFull = True
    for row in range(ROWS):
        for col in range(COLUMNS):
            if(gameState[row][col] == 0):
                gameStateFull = False
    if(gameStateFull == True or gameOver == True):
        font = pygame.font.Font(pygame.font.get_default_font(), 48)
        text = font.render('Press R to Restart', True, pygame.Color(255, 0 ,0 ), None)
        textRect = text.get_rect()
        textRect.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(text, textRect)
        return True
    return False

def winCheck(gameState: list, show = False):
    #Vertical Win
    for row in range(ROWS):
        if(gameState[row][0] == gameState[row][1] == gameState[row][2] != 0):
            if show:
                color = CIRC_COLOR if gameState[row][0] == 1 else X_COLOR
                initPos = (row * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                finalPos = (row * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                pygame.draw.line(screen, color, initPos, finalPos, SHAPESWIDTH)
            return True
    #Horizontal Win
    for column in range(COLUMNS):
        if(gameState[0][column] == gameState[1][column] == gameState[2][column] != 0):
            if show:
                color = CIRC_COLOR if gameState[0][column] == 1 else X_COLOR
                initPos = (20, column * SQUARE_SIZE + SQUARE_SIZE // 2)
                finalPos = (WIDTH - 20, column * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.line(screen, color, initPos, finalPos, SHAPESWIDTH)
            return True
    #Desc Diagonal Win
    if (gameState[0][0] == gameState[1][1] == gameState[2][2] != 0):
        if show:
            color = CIRC_COLOR if gameState[1][1] == 1 else X_COLOR
            initPos = (20, 20)
            finalPos = (WIDTH -20, HEIGHT - 20)
            pygame.draw.line(screen, color, initPos, finalPos, SHAPESWIDTH)
        return True
    #Asc Diagonal Win
    elif(gameState[2][0] == gameState[1][1] == gameState[0][2] != 0):
        if show:
            color = CIRC_COLOR if gameState[1][1] == 1 else X_COLOR
            initPos = (20, HEIGHT - 20)
            finalPos = (WIDTH - 20, 20)
            pygame.draw.line(screen, color, initPos, finalPos, SHAPESWIDTH)
        return True
    #No Win
    return False

def markSquare(row: int, column: int, gameState, playerNr):
    gameState[row][column] = playerNr
    return gameState

def convCordToRowAndColumn(xPos, yPos):
    row, column = 0,0
    row= int(xPos / SQUARE_SIZE)
    column= int(yPos / SQUARE_SIZE)
    return row, column



main()
