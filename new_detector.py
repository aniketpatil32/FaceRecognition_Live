from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import MySQLdb
import cv2,os
import numpy as np
from PIL import Image 
import pickle
import time
import threading
import sys
import Tkinter as tk

labourer_id={}
saved_labourer={}
marked_labourer={}
terminate=False

file=open("/home/pi/Desktop/project/face_recognizer/server_ip/output.txt")
ip=file.read(16)
ip=str(ip)
ip=ip[1::]

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def stop():
    global terminate
    terminate=True
    exit()
def choice():
    root1 = tk.Tk()
    # width x height + x_offset + y_offset:
    #root=tk.Toplevel(root)
    root1.title("Recognition")
    root1.geometry("300x100")
    center(root1)
    w = tk.Button(root1, text="STOP", bg="red", fg="white",command=stop)
    w.pack(fill=tk.X,padx=10,pady=20)
    root1.mainloop()
    
def thread():
    while(True):
        if(terminate):
            break
        upload_attendance()
        time.sleep(10)
def fetch_labourer(user_id):
    cnx = MySQLdb.connect(ip,"aniket","acool","field")
     								 
    cursor = cnx.cursor()
    
    query = ("SELECT * from registration where uid= %d")%(int(user_id))

    cursor.execute(query)

    for (uid,name,address,contact,count) in cursor:
        cnt=int(count)
        print"your name is %s\n count is %d" %(name,cnt)
        cursor.close()
        cnx.close()
        if(cnt==-1):
           print"record not found"
        else:
           break

def upload_attendance():
     global ip
     cnx = MySQLdb.connect(ip,"aniket","acool","field")
     cursor = cnx.cursor()
     try:
        for ele in labourer_id:
            if(ele not in marked_labourer):
                cursor.execute("insert into laborer(uid,time) values(%d,'%s')"%(ele,labourer_id[ele]))
                cnx.commit()
                marked_labourer[ele]=1
                print "data entered"
   #print (cursor.rowcount)
        cursor.close()
        cnx.close()
     except:
        print "error"
        cursor.close()
        cnx.close()

timer=threading.Timer(0,thread)
timer.start()
timer1=threading.Timer(0,choice)
timer1.start()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
# allow the camera to warmup
time.sleep(0.1)
font = cv2.FONT_HERSHEY_SIMPLEX #Creates a font
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    #cv2.imshow("im",image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(image,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        if(conf<80 and nbr_predicted not in labourer_id):
            labourer_id[nbr_predicted]=str(time.ctime())    
        name="unknown"
        if(nbr_predicted==1):
             name='aniket'
        elif(nbr_predicted==3):
             name='manojkumar'
        elif(nbr_predicted==4):
             name="pradad"
        elif(nbr_predicted==5):
             name="mahesh"
        elif(nbr_predicted==2):
             name="omkar"
        cv2.putText(image,str(name)+str(round(conf)), (x,y+h),font,1,(255,255,255),2,cv2.LINE_AA) #Draw the text
    cv2.imshow('im',image)    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    if(terminate):
        timer.cancel()
        timer1.cancel()
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        exit()
        







