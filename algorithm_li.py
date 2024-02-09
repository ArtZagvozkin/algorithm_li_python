#!/usr/bin/python3
#Artem Zagvozkin
#Algorithm Li. Shortest path between two points
#UTF-8

from random import randint
from tkinter import *


class SearchRoute:
    def __init__(self, height, width, numBarriers, canvas):
        self.__height = height
        self.__width = width
        self.__numBarriers = numBarriers
        self.__carX = -1
        self.__carY = -1
        self.__finX = -1
        self.__finY = -1
        self.__map = [[0] * width for i in range(height)]

        self.__canvas = canvas

    def genMap(self):
        # clear map
        self.__map = [[0] * self.__width for i in range(self.__height)]

        # gen car
        self.__carX = randint(0, self.__height - 1)
        self.__carY = randint(0, self.__width - 1)
        self.__map[self.__carX][self.__carY] = 1

        # gen finish
        while True:
            self.__finX = randint(0, self.__height - 1)
            self.__finY = randint(0, self.__width - 1)
            if self.__map[self.__finX][self.__finY] == 0:
                self.__map[self.__finX][self.__finY] = 2
                break

        # gen barriers
        for index in range(self.__numBarriers):
            while True:
                x = randint(0, self.__height - 1)
                y = randint(0, self.__width - 1)
                if self.__map[x][y] == 0:
                    self.__map[x][y] = 3
                    break

    def printShell(self):
        for i in range(self.__height):
            for j in range(self.__width):
                if self.__map[i][j] <= 0:
                    print('▒', end='')
                elif self.__map[i][j] == 1:
                    print('A', end='')
                elif self.__map[i][j] == 2:
                    print('B', end='')
                elif self.__map[i][j] == 3:
                    print('█', end='')
                elif self.__map[i][j] == 4:
                    print('•', end='')
                else:
                    print(self.__map[i][j], end='\t')
            print('\n', end='')

    def showMap(self):
        for i in range(self.__height):
            for j in range(self.__width):
                shift = 20
                y = j*12
                x = i*12
                if self.__map[i][j] <= 0:
                    self.__canvas.create_rectangle((shift + x-6, shift + y-6, shift + x+6, shift + y+6), fill="white", outline="gray")
                    print('▒', end='')
                elif self.__map[i][j] == 1:
                    self.__canvas.create_rectangle((shift + x-6, shift + y-6, shift + x+6, shift + y+6), fill="red", outline="gray")
                    print('A', end='')
                elif self.__map[i][j] == 2:
                    self.__canvas.create_rectangle((shift + x-6, shift + y-6, shift + x+6, shift + y+6), fill="blue", outline="gray")
                    print('B', end='')
                elif self.__map[i][j] == 3:
                    self.__canvas.create_rectangle((shift + x-6, shift + y-6, shift + x+6, shift + y+6), fill="black", outline="black")
                    print('█', end='')
                elif self.__map[i][j] == 4:
                    self.__canvas.create_rectangle((shift + x-6, shift + y-6, shift + x+6, shift + y+6), fill="gray", outline="gray")
                    print('•', end='')
                else:
                    print(self.__map[i][j], end='\t')
            print('\n', end='')

    def buildRoute(self):
        weight = -1
        self.__map[self.__carX][self.__carY] = weight

        exec = True
        maxSteps = self.__height * self.__width * -1
        while exec:
            for i in range(self.__height):
                for j in range(self.__width):
                    if self.__map[i][j] == weight:
                        self.__fillNighbours(i, j, weight - 1)
                        if i == self.__finX and j == self.__finY:
                            self.__map[self.__finX][self.__finY] = 2
                            exec = False
            weight -= 1
            if weight == maxSteps:  # no route
                self.__map[self.__carX][self.__carY] = 1
                return []
        weight += 2

        i = self.__finX
        j = self.__finY
        route = []
        while self.__map[i][j] != -1:
            route.append([i, j])
            self.__map[i][j] = 4
            if self.__checkStep(i + 1, j, weight):
                i += 1
                weight += 1
            elif self.__checkStep(i - 1, j, weight):
                i -= 1
                weight += 1
            elif self.__checkStep(i, j + 1, weight):
                j += 1
                weight += 1
            elif self.__checkStep(i, j - 1, weight):
                j -= 1
                weight += 1
            else:
                break
        self.__map[self.__carX][self.__carY] = 1
        self.__map[self.__finX][self.__finY] = 2
        return route

    def __fillNighbours(self, x, y, weight):
        if x + 1 < self.__height:
            if self.__map[x + 1][y] == 0 or self.__map[x + 1][y] == 2:
                self.__map[x + 1][y] = weight
        if x - 1 > -1:
            if self.__map[x - 1][y] == 0 or self.__map[x - 1][y] == 2:
                self.__map[x - 1][y] = weight
        if y + 1 < self.__width:
            if self.__map[x][y + 1] == 0 or self.__map[x][y + 1] == 2:
                self.__map[x][y + 1] = weight
        if y - 1 > -1:
            if self.__map[x][y - 1] == 0 or self.__map[x][y - 1] == 2:
                self.__map[x][y - 1] = weight

    def __checkStep(self, x, y, weight):
        if x > self.__height - 1:
            return False
        if x < -1:
            return False
        if y > self.__width - 1:
            return False
        if y < -1:
            return False
        if self.__map[x][y] == weight:
            return True
        return False


def btn_new_map_click():
    sr.genMap()
    sr.showMap()

def btn_build_route_click():
    sr.buildRoute()
    sr.showMap()




# Main window
window = Tk()
window.title("Search route")
window.geometry('625x650')
window.resizable(width=False, height=False)
basePnl = PanedWindow(orient=VERTICAL)
basePnl.pack(fill=BOTH, expand=1)

# Button panel
buttons_pnl = PanedWindow(orient=HORIZONTAL, height=25)
basePnl.add(buttons_pnl)

# Canvas
my_canvas = Canvas(width=200, height=200, bg='white')
basePnl.add(my_canvas)

# Init class SearchRoute
sr = SearchRoute(50, 50, 900, my_canvas)

# Buttons
btn_new_map = Button(text="New map", width=15, command=btn_new_map_click)
buttons_pnl.add(btn_new_map)

btn_build_route = Button(text="Build route", width=15, command=btn_build_route_click)
buttons_pnl.add(btn_build_route)

window.mainloop()
