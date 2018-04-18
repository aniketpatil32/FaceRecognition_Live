import cv2, os
import numpy as np
from PIL import Image

face_cascade= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
path = './raw_images'
image_paths = [os.path.join(path, f) for f in os.listdir(path)]
for image_path in image_paths:
   image_pil=Image.open(image_path).convert('L')
   image=np.array(image_pil, 'uint8')
   faces = face_cascade.detectMultiScale(image)
   print "faces"+str(len(faces))
   for (x, y, w, h) in faces:
      cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
      cv2.waitKey(50)
      new_name=os.path.basename(image_path)
      new_dir=os.path.split(image_path)[0].replace("raw_images","face_db")
      print(new_dir+"/"+new_name)
      cv2.imwrite(new_dir+"/"+new_name,image[y:y+h,x:x+w])
#os.remove(image_path)