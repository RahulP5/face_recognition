from imutils.video import VideoStream
from imutils.video import FPS
import RPi.GPIO as GPIO
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

GPIO.setmode(GPIO.BCM)

bstate=0

green=15
red=18

b1=14
b2=23

GPIO.setup(green,GPIO.OUT)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(b1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(b2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.output(green,GPIO.LOW)
GPIO.output(red,GPIO.LOW)

def my_fun():
        counts=0
        un=0
        nam=""
        global bstate

        if bstate==0:
                uin=input("Enter 1:")
                bstate=1
                
        
        if uin == 1:

                bstate=0
                
                ap = argparse.ArgumentParser()
                ap.add_argument("-c", "--cascade", required=True,
                        help = "path to where the face cascade resides")
                ap.add_argument("-e", "--encodings", required=True,
                        help="path to serialized db of facial encodings")
                args = vars(ap.parse_args())

                print("[INFO] loading encodings + face detector...")
                data = pickle.loads(open(args["encodings"], "rb").read())
                detector = cv2.CascadeClassifier(args["cascade"])

                print("[INFO] starting video stream...")
                vs = VideoStream(src=0).start()
                time.sleep(1.0)

                fps = FPS().start()
               

                while counts<10:
                        frame = vs.read()
                        
                        frame = imutils.resize(frame, width=500)
                        
                        
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                                minNeighbors=5, minSize=(30, 30),
                                flags=cv2.CASCADE_SCALE_IMAGE)
                        
                        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

                        encodings = face_recognition.face_encodings(rgb, boxes)
                        names = []

                        for encoding in encodings:
                                matches = face_recognition.compare_faces(data["encodings"],
                                        encoding)
                                name = "Unknown"
                                if False in matches:
                                        nam="Unknown"
                                
                                if True in matches:
                                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                                        counts = {}
                                        for i in matchedIdxs:
                                                name = data["names"][i]
                                                counts[name] = counts.get(name, 0) + 1
                                        name = max(counts, key=counts.get)
                                names.append(name)
                                
                        for ((top, right, bottom, left), name) in zip(boxes, names):
                                
                                cv2.rectangle(frame, (left, top), (right, bottom),
                                        (0, 255, 0), 2)
                                y = top - 15 if top - 15 > 15 else top + 15
                                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.75, (0, 255, 0), 2)
                                
                                
                        cv2.imshow("Frame", frame)
                        key = cv2.waitKey(1) & 0xFF
                        

                        if (key == ord("q") or nam=="Unknown"):
                                break
                        fps.update()
                        

                fps.stop()
                print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
                print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
                #print(name)
                #print(counts)
                if name!="Unknown":
                        print("Hello %s"%(name))
                        GPIO.output(green,GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(green,GPIO.LOW)
                        
                else:
                        print("Try again")
                        GPIO.output(red,GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(red,GPIO.LOW)

                cv2.destroyAllWindows()
                vs.stop()
                
try:                
    while True:
        my_fun()
except KeyboardInterrupt: 
    GPIO.cleanup()

