# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:08:43 2020

@author: 蒋志超
"""
import image, sensor, time, lcd

face_cascade = image.HaarCascade('frontalface')

eye_cascade = image.HaarCascade('eye')

print(face_cascade, eye_cascade)

# 调用摄像头摄像头
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

lcd.init()
lcd.rotation(2)

while(True):
    clock = time.clock()
    # 获取摄像头拍摄到的画面
    img = sensor.snapshot()
    faces = img.find_features(face_cascade, threshold = 0.5, scale = 1.5)
    #print(faces)
    for (x,y,w,h) in faces:
        # 画出人脸框，蓝色，画笔宽度微
        img.draw_rectangle(x,y,w,h,(255,0,0),thickness = 2)
        # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
        eyes = img.find_features(eye_cascade, threshold = 1.0, scale = 1.35, roi = (x,y+ h//4,w,h//2))
        # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        for (ex,ey,ew,eh) in eyes:
            #画出人眼框，绿色，画笔宽度为1
            if (ex + ew/2) > x + w/2:
                img.draw_rectangle(ex,ey,ew,eh,(0,255,0),1)
            else:
                img.draw_rectangle(ex,ey,ew,eh,(0,0,255),1)

    # 实时展示效果画面
    lcd.display(img)
    print(clock.fps())
