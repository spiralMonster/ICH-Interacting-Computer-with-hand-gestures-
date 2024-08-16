import cv2 as cv
import time
import mediapipe as mp
import numpy as np
import math
import os
# Volume Adjuster libraries:
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

import screen_brightness_control as sbc

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))

vol_range=volume.GetVolumeRange()
min_vol=vol_range[0]
max_vol=vol_range[1]

#Mediapipe Initializations:
mpHand=mp.solutions.hands
mpDraw=mp.solutions.drawing_utils

ctime=0
ptime=0

video=cv.VideoCapture(0)
video.set(3,720)
video.set(4,720)


hand=mpHand.Hands()
lengths_sound=[]
lengths_bright=[]
flag_sound=False
flag_bright=False
while True:
    success,img=video.read()
    img_rgb=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    img_h,img_w=img.shape[:2]
    results=hand.process(img_rgb)
    landmark = {}
    if results.multi_hand_landmarks:
        for handlm in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handlm,mpHand.HAND_CONNECTIONS)
            for idx,lm in enumerate(handlm.landmark):
                x=int(lm.x*img_w)
                y=int(lm.y*img_h)
                landmark[idx]=(x,y)
                cv.putText(img,str(idx),(x,y),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)

        x0, y0 = landmark[0]
        x1, y1 = landmark[1]
        x2, y2 = landmark[2]
        x3, y3 = landmark[3]
        x4,y4=landmark[4]
        x5, y5 = landmark[5]
        x6, y6 = landmark[6]
        x7, y7 = landmark[7]
        x8,y8=landmark[8]
        x9, y9 = landmark[9]
        x10, y10 = landmark[10]
        x11, y11 = landmark[11]
        x12,y12=landmark[12]
        x13, y13 = landmark[13]
        x14, y14 = landmark[14]
        x15, y15 = landmark[15]
        x16, y16 = landmark[16]
        x17,y17=landmark[17]
        x18, y18 = landmark[18]
        x19, y19 = landmark[19]
        x20, y20 = landmark[20]
        margin=15
        boundry=int(math.hypot(x9-x0,y9-y0))+margin
        cv.circle(img,(x0,y0),int(boundry),(0,255,0),2)


        dist_zeroth_finger={}
        tip_points=[4,8,12,16,20]
        for ind,(x,y) in landmark.items():
            if ind in tip_points:
                dist_zeroth_finger[ind] = math.hypot(x - x0, y - y0)

        #For sound Finger Number 8:
        distances=dist_zeroth_finger.copy()
        length_seq_sound=math.hypot(x8-x4,y8-y4)
        if all(item<boundry for item in distances.values()):
            flag_sound=False
        pop_items=[]
        pop_items.append(distances.pop(8))
        # pop_items.append(distances.pop(4))

        if all(item<boundry for item in distances.values()) and all(item>boundry for item in pop_items):
            if flag_bright:
                flag_sound=False
            else:
                flag_sound=True

        if flag_sound:
            vol = np.interp(length_seq_sound, [20, 180], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)
            vol=np.interp(vol,[-65,0],[0,100])
            cv.line(img, (x8, y8), (x4, y4), (0, 255, 0), 2)
            cv.circle(img, (int((x8 + x4) / 2), int((y8 + y4) / 2)), 5, (0, 0, 255), cv.FILLED)
            cv.putText(img,"Adjusting Volume",(30,30),cv.FONT_HERSHEY_PLAIN,1,(250, 206, 135),2)
            cv.putText(img, f"Volume: {int(vol)}", (30, 50), cv.FONT_HERSHEY_PLAIN, 1, (250, 206, 135), 2)

        ## For Brightness(40,350)
        distances=dist_zeroth_finger.copy()
        if all(item<boundry for item in distances.values()):
            flag_bright=False
        pop_items=[]
        pop_items.append(distances.pop(8))
        pop_items.append(distances.pop(12))
        # pop_items.append(distances.pop(4))
        if all(item<boundry for item in distances.values()) and all(item>boundry for item in pop_items):
            if flag_sound:
                flag_bright=False
            else:
                flag_bright=True

        length_seq_bright=math.hypot(x12-x4,y12-y4)
        if flag_bright:
            brg=np.interp(length_seq_bright,[25,300],[0,100])
            sbc.set_brightness(brg)
            cv.line(img, (x12, y12), (x4, y4), (0, 255, 0), 2)
            cv.circle(img, (int((x12 + x4) / 2), int((y12 + y4) / 2)), 5, (0, 0, 255), cv.FILLED)
            cv.putText(img,f'Brightness: {int(brg)}',(30,50),cv.FONT_HERSHEY_PLAIN,1,(0,165,255),2)
            cv.putText(img,"Adjusting Brightness",(30,30),cv.FONT_HERSHEY_PLAIN,1,(0,165,255),2)

        #Sleep the PC:
        distances=dist_zeroth_finger.copy()
        pop_items=[]
        pop_items.append(distances.pop(12))
        if all(item>boundry for item in distances.values()) and all(item<boundry for item in pop_items):
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")


    ctime=time.time()
    frame_rates=int(1/(ctime-ptime))
    ptime=ctime
    cv.putText(img,str(frame_rates),(20,20),cv.FONT_HERSHEY_PLAIN,2,(120,140,160),2)
    cv.imshow('Video',img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
# print(lengths_bright)