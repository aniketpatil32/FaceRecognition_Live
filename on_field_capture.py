import picamera
import numpy
from time import sleep
import io
import cv2
import os


#Create a memory stream so photos doesn't need to be saved in a file
#stream = io.BytesIO()
count=0
path = './check'
image_paths = [os.path.join(path, f) for f in os.listdir(path)]
for image_path in image_paths:
    os.remove(image_path)
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
  #camera.start_preview()
# show image captured  
  cv2.imshow("current image is", image)
  cv2.waitKey(1)
#Load a cascade file for detecting faces
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

#Convert to grayscale
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
  faces = face_cascade.detectMultiScale(gray, 1.1, 5)

  print "Found "+str(len(faces))+" faces"

#Draw a rectangle around every found face
  for (x,y,w,h) in faces:
    #cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    cv2.imwrite("./check/"+str(count)+".jpg",image)
  count=count+1
  #choice= int(raw_input("0 to continue and 1 to exit"))
  #if(choice==1):
   #   break
  #else:
   #   continue
  