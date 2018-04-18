#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image
import time
import MySQLdb
import socket

ip=raw_input("Enter ip address of server\t")
# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_alt.xml"
detector = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer = cv2.face.createFisherFaceRecognizer()

#load training data
recognizer.read('trainer/trainer.yml')

# Path to the Yale Dataset
path = './face_db'
# Perform the tranining
#recognizer.train(images, np.array(labels))


# Append the images with the extension .sad into image_paths
image_paths = [os.path.join("./check", f) for f in os.listdir("./check")]

for image_path in image_paths:
    print("\n"+image_path)
    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    check_faces = detector.detectMultiScale(predict_image,1.5,5)
    #print("no of faces in check"+str(len(check_faces)))
    temp_conf=200
    temp_id=0
    for (x, y, w, h) in check_faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        #nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("laborer", ""))
        if nbr_predicted >=1:
            if(temp_conf>conf):
               temp_conf=conf
               temp_id=nbr_predicted
                    
            #print "id {} confidence {}".format(nbr_predicted,conf)
            
        else:
            print "no match found"
        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
        cv2.waitKey(1000)
    print "id {} confidence{}".format(temp_id,temp_conf)
    
    cnx = MySQLdb.connect(ip,"aniket","acool","field")
    cursor = cnx.cursor()
    try:
       if(temp_id!=0):
         c_time=str(time.ctime())
         print(c_time)
         cursor.execute("insert into laborer(uid,time) values(%d,'%s')"%(temp_id,c_time))
         cnx.commit()
         print "data entered"
    except:
       print "error"
    cursor.close()
    cnx.close()

