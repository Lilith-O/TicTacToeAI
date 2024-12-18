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
                howManyLists = 0
                for outer_list in centerCords:
                    for inner_list in outer_list:
                        for element in inner_list: 
                            if (howManyLists < 9 ):
                                if (mouseX > element):
                                    xDifference = mouseX - element
                                elif(mouseX < element):
                                    xDifference = element

                                if(centerX == 0):
                                    centerX = xDifference
                                    closestX = element
                                elif(centerX > xDifference):
                                    centerX = xDifference
                                    closestX = element
                            
                            elif(howManyLists >= 9):
                                if (mouseY > element):
                                    yDifference = element
                                elif(mouseY < element):
                                    yDifference = element

                                if(centerY == 0):
                                    centerY = yDifference
                                    closestY = element
                                elif(centerY > yDifference):
                                    centerY = yDifference
                                    closestY = element
                            howManyLists = howManyLists +1
                
                print(closestX, closestY)
                print(element, element)
                 
                
                pygame.draw.circle(screen, pygame.Color(160, 32, 240), (closestX, closestY), CIRCLERADIUS, SHAPESWIDTH)
                pygame.draw.line(screen, pygame.Color(160, 32, 240), (closestX - CIRCLERADIUS,closestY - CIRCLERADIUS), (closestX + CIRCLERADIUS, closestY + CIRCLERADIUS), SHAPESWIDTH)
                pygame.draw.line(screen, pygame.Color(160, 32, 240), (closestX - CIRCLERADIUS,closestY + CIRCLERADIUS), (closestX + CIRCLERADIUS, closestY - CIRCLERADIUS), SHAPESWIDTH)
           
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
