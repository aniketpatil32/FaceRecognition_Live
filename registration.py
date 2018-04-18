# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import MySQLdb
import socket
import Tkinter as tk
import threading

user_id = 0
terminate=False

def stop():
    global terminate
    terminate=True
    exit()
def choice():
    root1 = tk.Tk()
    # width x height + x_offset + y_offset:
    #root=tk.Toplevel(root)
    root1.title("Registration")
    root1.geometry("300x100")
    center(root1)
    w = tk.Button(root1, text="STOP", bg="red", fg="white",command=stop)
    w.pack(fill=tk.X,padx=10,pady=20)
    root1.mainloop()
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
def register():
   global user_id
   user_id = entry.get()
   root.destroy()
root = tk.Tk()
#root=tk.Toplevel(root)
root.title("Registration")
center(root)
root.geometry("400x100")
label = tk.Label(root, text='Enter Uid')
entry = tk.Entry(root)
label.pack(side=tk.TOP)
entry.pack()
#Button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button = tk.Button(root, text='Register', width=25, command=register)
button.pack()
root.mainloop()

timer1=threading.Timer(0,choice)
timer1.start()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

cnt=-1
cond=True
 
#ip=raw_input("Enter ip of server:")
file=open("/home/pi/Desktop/project/face_recognizer/server_ip/output.txt")
a=file.read(16)
a=str(a)
a=a[1::]
ip=a
print " server ip:"+a
print "UID:"+user_id
while(cond):
  
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

# allow the camera to warmup
time.sleep(0.1)
detector= cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
# capture frames from the camera

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)        
        for (x,y,w,h) in faces:
           cnt=cnt+1
           cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
           cv2.imwrite("./face_db/"+"laborer"+str(user_id)+"."+str(cnt)+".jpg",image)
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
	# show the frame
	print "Found "+str(len(faces))+" faces"
	key = cv2.waitKey(1) & 0xFF
        
        cnx = MySQLdb.connect(ip,"aniket","acool","field")
        cursor = cnx.cursor()
        try:
            temp=str(cnt)
            cursor.execute("update registration set count=%s where uid=%d"%(temp,int(user_id)))
            cnx.commit()
            print "data entered"
   #print (cursor.rowcount)
            cursor.close()
            cnx.close()
        except:
            print "error"
            cursor.close()
            cnx.close()

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	'''if cnt==100:
            break
	if key == ord("q"):
		break'''
	if(terminate):
            exit()
