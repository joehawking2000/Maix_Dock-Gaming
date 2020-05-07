# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:38:09 2020

@author: 蒋志超
"""

class block:
    def __init__(self):
        self.position = []
        self.number = 0
    def add(self, x,y, size):
        self.position += [[x, y, size]]
        self.number += 1
    def delete(self):
        for x in range(self.number):
            if self.position[0][1] <= 0:
                self.position.pop(0)
                self.number -= 1
    def move(self, speed):
        for x in range(self.number):
            self.position[x][1] -= speed

class player:
    def __init__(self, position = 0, state = False, speed = 1):
        self.position = position
        self.state = state
        self.speed = speed

    def move(self, n):
        k = self.position + n
        if abs(k) > 1:
            self.state = True
        else:
            self.position = k
            self.state = False

    def clean(self):
        self.position = 0
        self.state = False
        self.speed = 1

    def speedup(self, degree):
        k = (((self.speed - 1)*200)//3)/200 + 1
        self.speed = degree +k

class speedtime:
    def __init__(self, remain = 10):
        self.remain = remain
    def timepass(self):
        if self.remain != 0:
            self.remain -= 1
    def timeup(self):
        self.remain = 10
    def clean(self):
        self.remain = 0
