import cv2 as cv
import time
import mediapipe as mp
import numpy as np
import math
# Volume Adjuster libraries:
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

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
        # Adjusting Volume:
        x1, y1 = landmark[8]
        x2, y2 = landmark[4]
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv.circle(img,(int((x1+x2)/2),int((y1+y2)/2)),5,(0,0,255),cv.FILLED)
        length_seq = math.hypot(x2 - x1, y2 - y1)
        vol=np.interp(length_seq,[30,260],[min_vol,max_vol])
        volume.SetMasterVolumeLevel(vol,None)
        rect_len=np.interp(vol,[min_vol,max_vol],[400,100])
        cv.rectangle(img, (50, 100), (100, 400), (0, 255, 0), 2)
        cv.rectangle(img,(100,400),(50,int(rect_len)),(0,255,0),cv.FILLED)
        cv.putText(img,str(100),(40,100),cv.FONT_HERSHEY_PLAIN,1,(200,125,150),2)
        cv.putText(img, str(0), (40, 400), cv.FONT_HERSHEY_PLAIN, 1, (200, 125, 150), 2)

    ctime=time.time()
    frame_rates=int(1/(ctime-ptime))
    ptime=ctime
    cv.putText(img,str(frame_rates),(20,20),cv.FONT_HERSHEY_PLAIN,2,(120,140,160),2)
    cv.imshow('Video',img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break