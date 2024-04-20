import glob
import os
import time
import cv2
from threading import Thread
from emailing import sending_email
video=cv2.VideoCapture(0)
first_frame=None
status=0
status_list=[0]
c=1

def capture_image(frame,c):
    cv2.imwrite(f"photos/image{c}.png",frame)
    c=c+1

def clear_folder():
    images=glob.glob("photos/image*.png")
    for image in images:
        os.remove(image)
while True:
    status=0
    check,frame=video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau=cv2.GaussianBlur(gray_frame,(21,21),0)
    if first_frame is None:
        first_frame=gray_frame_gau
    deltaframe=cv2.absdiff(first_frame,gray_frame_gau)
    thresh_frame=cv2.threshold(deltaframe,80,255,cv2.THRESH_BINARY)[1]
    dil_frame=cv2.dilate(thresh_frame,None,iterations=2)
    contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if(cv2.contourArea(contour)<5000):
            continue
        x,y,w,h=cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+w),(0,255,0),3)
        if rectangle.any():
            capture_thread=Thread(target=capture_image,args=(frame,c))
            capture_thread.daemon=True
            capture_thread.start()
            c=c+1
            status=1
    status_list.append(status)
    status_list=status_list[-2:]
    if(status_list[0]==1 and status_list[1]==0):
        email_thread = Thread(target=sending_email, args=(f"photos/image{int(c/2)}.png",))
        email_thread.daemon=True
        email_thread.start()


    cv2.imshow("My Video",frame)
    key=cv2.waitKey(1)
    if key==ord("q"):
        break
video.release()
#clear_thread = Thread(target=clear_folder)
#clear_thread.start()
