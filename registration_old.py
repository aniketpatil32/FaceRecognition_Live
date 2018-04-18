import picamera
import numpy
import time
import io
import cv2
import MySQLdb


#Create a memory stream so photos doesn't need to be saved in a file
#stream = io.BytesIO()
cnt=-1
user_id=0;
cond=True
ip=raw_input("Enter ip address of server\t")
while(cond):
 ch= int(raw_input("\nEnter uid\t"))
 user_id=ch
 cnx = MySQLdb.connect(ip,"aniket","acool","field")
								 
 cursor = cnx.cursor()

 query = ("SELECT * from registration where uid= %d")%(ch)

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


while(True):
#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
  stream = io.BytesIO()
  with picamera.PiCamera() as camera:
    camera.resolution = (720, 480)
    camera.capture(stream, format='jpeg')

#Convert the picture into a numpy array
  buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
  image = cv2.imdecode(buff, 1)
# show image captured  
  #cv2.imshow("current image is", image)
  #cv2.waitKey(2000)
#Load a cascade file for detecting faces
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Convert to grayscale
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
  faces = face_cascade.detectMultiScale(gray, 2.5, 5)

  print "Found "+str(len(faces))+" faces"

#Draw a rectangle around every found face
  for (x,y,w,h) in faces:
    #cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    cnt=cnt+1
    cv2.imwrite("./face_db/"+"laborer"+str(user_id)+"."+str(cnt)+".jpg",image[y:y+h,x:x+w])
    
  cnx = MySQLdb.connect(ip,"aniket","acool","field")
  cursor = cnx.cursor()
  try:
   temp=str(cnt)
   cursor.execute("update registration set count=%s where uid=%d"%(temp,user_id))
   cnx.commit()
   print "data entered"
   #print (cursor.rowcount)
   cursor.close()
   cnx.close()
  except:
   print "error"
   cursor.close()
   cnx.close()
  
  #time.sleep(0.1)
  #choice= int(raw_input("0 to continue and 1 to exit"))
  #if(choice==1):
  #   break
  #else:
  #   continue
  
