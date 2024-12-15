import sys
import pygame
import numpy
from constants import *


#PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(WIDTH/3, 1), pygame.Vector2(WIDTH/3, HEIGHT), SHAPESWIDTH)
pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(WIDTH/3 * 2, 1), pygame.Vector2(WIDTH/3 *2, HEIGHT), SHAPESWIDTH)
pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(1 , HEIGHT/3), pygame.Vector2(WIDTH, HEIGHT/3), SHAPESWIDTH)
pygame.draw.line(screen, pygame.Color(160, 32, 240), pygame.Vector2(1, HEIGHT/3*2), pygame.Vector2(WIDTH, HEIGHT/3*2), SHAPESWIDTH)
centerCords = []

    

def main():
    centerCords = divideScreen()
    while True:
        for event in pygame.event.get():
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                xDifference, yDifference = 0, 0
                centerX, centerY = 0, 0
                closestX, closestY = 0, 0
                for x in range(0, centerCords[0].__len__(),1):
                    print()
                    if (mouseX > centerCords[0][x]):
                        xDifference = mouseX - centerCords[0][x]
                    elif(mouseX < centerCords[0][x]):
                        xDifference = centerCords[0][x] - mouseX

                    if(centerX == 0):
                        centerX = xDifference
                        closestX = x
                    elif(centerX > xDifference):
                        centerX = xDifference
                        closestX = x

                    if (mouseY > centerCords[1][x]):
                        yDifference = mouseY - centerCords[1][x]
                    elif(mouseY < centerCords[1][x]):
                        yDifference = centerCords[1][x] - mouseY

                    if(centerY == 0):
                        centerY = yDifference
                        closestY = x
                    elif(centerY > yDifference):
                        centerY = yDifference
                        closestY = x
                
                print(closestX, closestY)
                print(centerCords[0][x], centerCords[1][x])
                 
                
                pygame.draw.circle(screen, pygame.Color(160, 32, 240), (mouseX, mouseY), CIRCLERADIUS, SHAPESWIDTH)
                pygame.draw.line(screen, pygame.Color(160, 32, 240), (mouseX - CIRCLERADIUS,mouseY - CIRCLERADIUS), (mouseX + CIRCLERADIUS, mouseY + CIRCLERADIUS), SHAPESWIDTH)
                pygame.draw.line(screen, pygame.Color(160, 32, 240), (mouseX - CIRCLERADIUS,mouseY + CIRCLERADIUS), (mouseX + CIRCLERADIUS, mouseY - CIRCLERADIUS), SHAPESWIDTH)
           
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        print(centers)
        print(centers.__len__())
        hasDivided = True
        return centers

main()
