# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:46:34 2020

@author: 蒋志超
"""

import pygame
from pygame.locals import *
import sys
import random
from setclass import block, player, speedtime

pygame.init()

BLACK =(0,0,0)
WHITE = (255,255,255)
bg_color = (0, 0, 70)# 背景颜色
SCREEN_SIZE = [500,400]#屏幕大小
PLAYER_SIZE = [80,10]#滑雪者大小
BLOCK_SIZE = [70, 70]
u = 0.4

clock = pygame.time.Clock()#定时器

bl =  block()

def getblock(bl):
    t = random.randint(0,2)
    if t == 0:
        pass
    if t == 1:#一格障碍物
        x = random.randint(-2, 2)
        bl.add(x, 3, 0)
    if t == 2:#两格障碍物
        x = random.randint(-1,1)
        choice = random.randint(-1,0)
        bl.add(x + choice,3,1)

screen = pygame.display.set_mode(SCREEN_SIZE)
player0 = player()
spdtm = speedtime()

# 自定义事件
ADDBLOCK = pygame.USEREVENT + 1      # 事件本质上就是整数常量。比 USEREVENT 小的数值已经对应内置事件，因此任何自定义事件都要比 USEREVENT 大
pygame.time.set_timer(ADDBLOCK, 1000) # 每隔一秒触发

while(True):
    for event in pygame.event.get():
        if event.type == QUIT: # 点击右上角的'X'，终止主循环
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: # 按下'ESC'键，终止主循环
                pygame.quit()
                sys.exit()
            elif event.key == K_LEFT:
                player0.move(-1)
            elif event.key == K_RIGHT:
                player0.move(1)
        elif event.type == ADDBLOCK:
            getblock(bl)

    if player0.state:
        spdtm.timeup()
        #做一个跃起的动作
    player0.speedup(spdtm.remain/10)
    spdtm.timepass()

    screen.fill(bg_color)
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(1-u)/2, 0), (0, SCREEN_SIZE[1]))
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(5-3*u)/10, 0), (SCREEN_SIZE[0]/5, SCREEN_SIZE[1]))
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(5-u)/10, 0), (SCREEN_SIZE[0]/5 * 2, SCREEN_SIZE[1]))
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(5+u)/10, 0), (SCREEN_SIZE[0]/5 * 3, SCREEN_SIZE[1]))
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(5+3*u)/10, 0), (SCREEN_SIZE[0]/5 * 4, SCREEN_SIZE[1]))
    pygame.draw.aaline(screen, WHITE,(SCREEN_SIZE[0]*(1+u)/2, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1]))

    bl.move(player0.speed/20)
    for blk in bl.position:
        x0 = blk[0]*SCREEN_SIZE[0]/5 + SCREEN_SIZE[0]/2 - BLOCK_SIZE[0]/2
        y0 = SCREEN_SIZE[1] * (4 - blk[1])/4 - BLOCK_SIZE[1]
        w0 = BLOCK_SIZE[0] + blk[2]*SCREEN_SIZE[0]/5
        a =  u+ (1-u) * y0 / SCREEN_SIZE[1]
        x = SCREEN_SIZE[0]/2 + (x0 - SCREEN_SIZE[0]/2) *a
        w = w0 * a
        blk_pos = pygame.Rect(x, y0, w,BLOCK_SIZE[1])
        pygame.draw.rect(screen, WHITE, blk_pos)
        if blk[0] == player0.position or blk[0] + blk[2] == player0.position:
            if blk[1] <= 0:
                player0.clean()
                spdtm.clean()
    bl.delete()

    player0_pos = pygame.Rect(player0.position*SCREEN_SIZE[0]/5 + SCREEN_SIZE[0]/2 - PLAYER_SIZE[0]/2, SCREEN_SIZE[1]-PLAYER_SIZE[1], PLAYER_SIZE[0], PLAYER_SIZE[1])
    pygame.draw.rect(screen, WHITE, player0_pos)

    pygame.display.update()#更新软件界面显示
    clock.tick(60)