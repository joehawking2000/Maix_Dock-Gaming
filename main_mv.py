# Untitled - By: 蒋志超 - 周五 5月 8 2020

import sensor, image, time, lcd
import sys
from machine import Timer
import random
from setclass import block, player, speedtime



BLACK =(0,0,0)
WHITE = (255,255,255)
bg_color = (0, 0, 70)# 背景颜色
SCREEN_SIZE = [320,240]#屏幕大小
PLAYER_SIZE = [55,10]#滑雪者大小
BLOCK_SIZE = [50, 50]
u = 0.4

clock = time.clock()#定时器

face_cascade = image.HaarCascade('frontalface')

eye_cascade = image.HaarCascade('eye')

print(face_cascade, eye_cascade)

# 调用摄像头摄像头
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)


bl =  block()

def getblock(timer):
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

def findeyes():
    f = leye = reye = 0
    for x in range(10):
        imgface = sensor.snapshot()
        faces = imgface.find_features(face_cascade, threshold = 0.5, scale = 1.5)
        for (x,y,w,h) in faces:
            # 得到人脸位置
            f += 1
            eyes = imgface.find_features(eye_cascade, threshold = 1.0, scale = 1.35, roi = (x,y + h//4,w,h // 2))
            # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
            for (ex,ey,ew,eh) in eyes:
                #判断左右人眼
                if (ex + ew/2) > x + w/2:
                    leye += 1
                else:
                    reye += 1
    fexit = True if f >= 7 else False
    lexit = True if leye >= f//2 else False
    rexit = True if reye >= f//2 else False
    return [fexit, lexit, rexit]


def back(timer):
    p = -1 if player0.position < 0 else 1
    player0.position = p

lcd.init()
lcd.rotation(2)
player0 = player()
spdtm = speedtime()

# 自定义事件
ADDBLOCK = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=3, unit=Timer.UNIT_S, \
    callback=getblock, arg=None, start=False, priority=1, div=0)

BACK = Timer(Timer.TIMER1, Timer.CHANNEL1, mode = Timer.MODE_ONE_SHOT, period = 2, unit = Timer.UNIT_S,\
    callback = back,arg = None,start = False)
lcd.draw_string(140,110, 'START!', lcd.WHITE, lcd.RED)
length = 50
alltime =0
while(length > 0):

    #接口
    rf = findeyes()
    #print(rf)
    if rf[0]:
        ADDBLOCK.start()
        if rf[1] and not rf[2]:
            player0.move(-1)
        if not rf[1] and rf[2]:
            player0.move(1)


        player0.speedup(spdtm.remain/10)
        spdtm.timepass()


        img = image.Image()
        img.draw_line(int(SCREEN_SIZE[0]*(1-u)/2), 0, 0, SCREEN_SIZE[1], WHITE, 1)
        img.draw_line(int(SCREEN_SIZE[0]*(5-3*u)/10), 0, int(SCREEN_SIZE[0]/5), SCREEN_SIZE[1], WHITE, 1)
        img.draw_line(int(SCREEN_SIZE[0]*(5-u)/10), 0, int(SCREEN_SIZE[0]/5 * 2), SCREEN_SIZE[1], WHITE, 1)
        img.draw_line(int(SCREEN_SIZE[0]*(5+u)/10), 0, int(SCREEN_SIZE[0]/5 * 3), SCREEN_SIZE[1], WHITE, 1)
        img.draw_line(int(SCREEN_SIZE[0]*(5+3*u)/10), 0, int(SCREEN_SIZE[0]/5 * 4), SCREEN_SIZE[1], WHITE, 1)
        img.draw_line(int(SCREEN_SIZE[0]*(1+u)/2), 0, SCREEN_SIZE[0], SCREEN_SIZE[1], WHITE, 1)

        bl.move(player0.speed/2)
        length -= player0.speed
        for blk in bl.position:
            x0 = blk[0]*SCREEN_SIZE[0]/5 + SCREEN_SIZE[0]/2 - BLOCK_SIZE[0]/2
            y0 = SCREEN_SIZE[1] * (4 - blk[1])/4 - BLOCK_SIZE[1]
            w0 = BLOCK_SIZE[0] + blk[2]*SCREEN_SIZE[0]/5
            a =  u+ (1-u) * y0 / SCREEN_SIZE[1]
            x = SCREEN_SIZE[0]/2 + (x0 - SCREEN_SIZE[0]/2) *a
            w = w0 * a
            img.draw_rectangle(int(x), int(y0), int(w),BLOCK_SIZE[1], WHITE,1,fill = True)
            if blk[0] == player0.position or blk[0] + blk[2] == player0.position:
                if blk[1] <= 0:
                    player0.clean()
                    spdtm.clean()
        bl.delete()

        img.draw_rectangle(int(player0.position*SCREEN_SIZE[0]/5 + SCREEN_SIZE[0]/2 - PLAYER_SIZE[0]/2), SCREEN_SIZE[1]-PLAYER_SIZE[1], PLAYER_SIZE[0], PLAYER_SIZE[1], WHITE, 1,fill = True)

        lcd.display(img)#更新软件界面显示
        lcd.draw_string(240,10,'time: %d' %(alltime),lcd.YELLOW)
        if player0.state:
            spdtm.timeup()
            #做一个跃起的动作
            BACK.start()
            time.sleep(2.2)
            alltime += 0.5
            length -= 1
        else:
            alltime += 1
    else:
        ADDBLOCK.stop()
        lcd.draw_string(10,10,'NO FACE!',lcd.RED)


lcd.init()
lcd.rotation(2)
lcd.draw_string(100,100,'Game over!',lcd.BLUE,lcd.GREEN)
lcd.draw_string(100,150,'Time: %d' %(alltime), lcd.BLUE,lcd.GREEN)


