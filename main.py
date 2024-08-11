import cv2 as cv
import time
import mediapipe as mp
import numpy as np
import math
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
        boundry=200
        cv.circle(img,(x0,y0),boundry,(0,255,0),2)
        dist_zeroth_finger={}
        tip_points=[4,8,12,16,20]
        for ind,(x,y) in landmark.items():
            if ind in tip_points:
                dist_zeroth_finger[ind] = math.hypot(x - x0, y - y0)

        ##For sound Finger Number 8:
        distances=dist_zeroth_finger.copy()
        length_seq_sound=math.hypot(x8-x4,y8-y4)
        distances.pop(8)
        if all(item<boundry for item in distances.values()):
            flag_sound=True

        if flag_sound:
            vol = np.interp(length_seq_sound, [20, 180], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)
            rect_len = np.interp(vol, [min_vol, max_vol], [400,100])
            cv.line(img, (x8, y8), (x4, y4), (0, 255, 0), 2)
            cv.circle(img, (int((x8 + x4) / 2), int((y8 + y4) / 2)), 5, (0, 0, 255), cv.FILLED)
            cv.rectangle(img, (50, 100), (100, 400), (250, 206, 135), 2)
            cv.rectangle(img,(100,400),(50,int(rect_len)),(250, 206, 135),cv.FILLED)
            cv.putText(img,str(100),(40,100),cv.FONT_HERSHEY_PLAIN,1,(250, 206, 135),2)
            cv.putText(img, str(0), (40, 400), cv.FONT_HERSHEY_PLAIN, 1, (250, 206, 135), 2)
            cv.putText(img,"Adjusting Volume",(30,30),cv.FONT_HERSHEY_PLAIN,1,(250, 206, 135),1)




        # flag_sound=False
        # flag_bright=False

        # #Adjusting Sound:
        # length_seq_sound=math.hypot(x8-x4,y8-y4)
        # if length_seq_sound<30.0:
        #     if flag_sound:
        #         flag_sound=False
        #     else:
        #         flag_sound=True
        #
        # if flag_sound:
        #     vol = np.interp(length_seq_sound, [30, 250], [min_vol, max_vol])
        #     volume.SetMasterVolumeLevel(vol, None)
        #     rect_len = np.interp(vol, [min_vol, max_vol], [400, 100])
        #     cv.line(img, (x8, y8), (x4, y4), (0, 255, 0), 2)
        #     cv.circle(img, (int((x8 + x4) / 2), int((y8 + y4) / 2)), 5, (0, 0, 255), cv.FILLED)
        #     cv.rectangle(img, (50, 100), (100, 400), (250, 206, 135), 2)
        #     cv.rectangle(img,(100,400),(50,int(rect_len)),(250, 206, 135),cv.FILLED)
        #     cv.putText(img,str(100),(40,100),cv.FONT_HERSHEY_PLAIN,1,(250, 206, 135),2)
        #     cv.putText(img, str(0), (40, 400), cv.FONT_HERSHEY_PLAIN, 1, (250, 206, 135), 2)
        #     cv.putText(img,"Adjusting Volume",(30,30),cv.FONT_HERSHEY_PLAIN,1,(250, 206, 135),1)
        #
        # #Adjusting Brightness:
        # length_seq_bright=math.hypot(x12-x4,y12-y4)
        #print(length_seq_bright)
        # if length_seq_bright<50.0:
        #     if flag_bright:
        #         flag_bright=False
        #     else:
        #         flag_bright=True
        #
        # if flag_bright:
        #     length_seq = math.hypot(x12 - x4, y12 - y4)
        #     br=np.interp(length_seq,[50,300],[0,100])
        #     sbc.set_brightness(br)
        #     cv.line(img,(x12,y12),(x4,y4),(0,255,0),2)
        #     cv.circle(img, (int((x12 + x4) / 2), int((y12 + y4) / 2)), 5, (0, 0, 255), cv.FILLED)
        #     cv.rectangle(img, (50, 100), (100, 400), (0,165,255), 2)
        #     cv.rectangle(img, (100, 400), (50, int(br)), (0,165,255), cv.FILLED)
        #     cv.putText(img, str(100), (40, 100), cv.FONT_HERSHEY_PLAIN, 1, (0,165,255), 2)
        #     cv.putText(img, str(0), (40, 400), cv.FONT_HERSHEY_PLAIN, 1, (0,165,255), 2)
        #     cv.putText(img,"Adjusting Brightness",(30,30),cv.FONT_HERSHEY_PLAIN,1,(0,165,255),2)







        #30 for sound
        # lengths_sound.append(math.hypot(x8-x4,y8-y4))
        # lengths_bright.append(math.hypot(x12-x4,y12-y4))
        # Adjusting Volume:
        # x1, y1 = landmark[8]
        # x2, y2 = landmark[4]
        # cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        # cv.circle(img,(int((x1+x2)/2),int((y1+y2)/2)),5,(0,0,255),cv.FILLED)
        # length_seq = math.hypot(x2 - x1, y2 - y1)
        # # lengths.append(length_seq)
        # vol=np.interp(length_seq,[30,250],[min_vol,max_vol])
        # volume.SetMasterVolumeLevel(vol,None)
        # rect_len=np.interp(vol,[min_vol,max_vol],[400,100])
        # cv.rectangle(img, (50, 100), (100, 400), (0, 255, 0), 2)
        # cv.rectangle(img,(100,400),(50,int(rect_len)),(0,255,0),cv.FILLED)
        # cv.putText(img,str(100),(40,100),cv.FONT_HERSHEY_PLAIN,1,(200,125,150),2)
        # cv.putText(img, str(0), (40, 400), cv.FONT_HERSHEY_PLAIN, 1, (200, 125, 150), 2)

        #Adjusting Brightness:
        # x1,y1=landmark[4]
        # x2,y2=landmark[12]
        # length_seq=math.hypot(x2-x1,y2-y1)
        # br=np.interp(length_seq,[50,300],[0,100])
        # sbc.set_brightness(br)
        # cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        # cv.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 5, (0, 0, 255), cv.FILLED)

    ctime=time.time()
    frame_rates=int(1/(ctime-ptime))
    ptime=ctime
    cv.putText(img,str(frame_rates),(20,20),cv.FONT_HERSHEY_PLAIN,2,(120,140,160),2)
    cv.imshow('Video',img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
# print(lengths_bright)