import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd
import cvzone
from tracker import Tracker
import os
from datetime import datetime


# Load the model and class list
model = YOLO("yolov10s.pt")
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 


# Create directory to save images if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
  
        
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
cap=cv2.VideoCapture('ju2.mp4')


# Initialize the tracker
tracker=Tracker()
tracker1=Tracker()
tracker2=Tracker()
tracker3=Tracker()

# Set the line position and offset
cy1=350
cy2=365
offset=8

# Initialize variables
count=0
upcar={}
downcar={}
countercarup=[]
countercardown=[]

upbus={}
downbus={}
counterbusdown=[]
counterbusup=[]

uptruck={}
downtruck={}
countertruckup=[]
countertruckdown=[]

upmotorcycle={}
downmotorcycle={}
countermotorcycleup=[]
countermotorcycledown=[]

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
   

    results=model.predict(frame)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    
    list=[]
    list1=[]
    list2=[]
    list3=[]
    for index,row in px.iterrows():
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])

        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
           list.append([x1,y1,x2,y2])
          
        elif'bus' in c:
            list1.append([x1,y1,x2,y2])
          
        elif 'truck' in c:
             list2.append([x1,y1,x2,y2])
        
        elif 'motorcycle' in c:
             list3.append([x1,y1,x2,y2])


###########################CarUp###############################################
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id1=bbox
        cx3=int(x3+x4)//2
        cy3=int(y3+y4)//2
        
        cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,255),2)
        cvzone.putTextRect(frame,f'Car',(x3,y3),1,1)
        
        if cy1<(cy3+offset) and cy1>(cy3-offset):
            upcar[id1]=(cx3,cy3)
        if id1 in upcar:
              if cy2<(cy3+offset) and cy2>(cy3-offset):
                cv2.circle(frame,(cx3,cy3),4,(255,0,0),-1)

                if countercarup.count(id1)==0:
                    countercarup.append(id1)
                    # Crop and save the car image
                    car_image = frame[y3:y4, x3:x4]
                    # Resize the cropped image to a larger size
                    #resized_car_image = cv2.resize(car_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/car_enter_{timestamp}.jpg", car_image)
                 
################################cardown###############################################                 
        if cy2<(cy3+offset) and cy2>(cy3-offset):
            downcar[id1]=(cx3,cy3)
        if id1 in downcar:
              if cy1<(cy3+offset) and cy1>(cy3-offset):
                cv2.circle(frame,(cx3,cy3),4,(255,0,255),-1)

                if countercardown.count(id1)==0:
                    countercardown.append(id1)
                    # Crop and save the car image
                    car_image = frame[y3:y4, x3:x4]
                    # Resize the cropped image to a larger size
                    #resized_car_image = cv2.resize(car_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/car_leave_{timestamp}.jpg", car_image)
                 


############################BusUp#######################################################
    bbox1_idx=tracker1.update(list1)
    for bbox1 in bbox1_idx:
        x5,y5,x6,y6,id2=bbox1
        cx4=int(x5+x6)//2
        cy4=int(y5+y6)//2
        
        cv2.rectangle(frame,(x5,y5),(x6,y6),(0,0,255),2)
        cvzone.putTextRect(frame,f'Bus',(x5,y5),1,1)
        
        if cy1<(cy4+offset) and cy1>(cy4-offset):
            upbus[id2]=(cx4,cy4)
        if id2 in upbus:
              if cy2<(cy4+offset) and cy2>(cy4-offset):
                cv2.circle(frame,(cx4,cy4),4,(255,0,0),-1)

                if counterbusup.count(id2)==0:
                    counterbusup.append(id2)
                    # Crop and save the car image
                    bus_image = frame[y5:y6, x5:x6]
                    # Resize the cropped image to a larger size
                    #resized_bus_image = cv2.resize(bus_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/bus_enter_{timestamp}.jpg", bus_image)
                 


############################downbus#####################################################
        if cy2<(cy4+offset) and cy2>(cy4-offset):
            downbus[id2]=(cx4,cy4)
        if id2 in downbus:
              if cy1<(cy4+offset) and cy1>(cy4-offset):
                cv2.circle(frame,(cx4,cy4),4,(255,0,255),-1)

                if counterbusdown.count(id2)==0:
                    counterbusdown.append(id2)
                    # Crop and save the car image
                    bus_image = frame[y5:y6, x5:x6]
                    # Resize the cropped image to a larger size
                    #resized_bus_image = cv2.resize(bus_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/bus_leave_{timestamp}.jpg", bus_image)
                 


############################truckUp#######################################################
    bbox2_idx=tracker2.update(list2)
    for bbox2 in bbox2_idx:
        x7,y7,x8,y8,id3=bbox2
        cy5=int(y7+y8)//2
        cx5=int(x7+x8)//2

        cv2.rectangle(frame,(x7,y7),(x8,y8),(255,255,0),2)
        cvzone.putTextRect(frame,f'Truck',(x7,y7),1,1)
        
        if cy1<(cy5+offset) and cy1>(cy5-offset):
            uptruck[id3]=(cx5,cy5)
        if id3 in uptruck:
            if cy2<(cy5+offset) and cy2>(cy5-offset):
                cv2.circle(frame,(cx5,cy5),4,(255,0,0),-1)

                if countertruckup.count(id3)==0:
                    countertruckup.append(id3)
                    # Crop and save the car image
                    truck_image = frame[y7:y8, x7:x8]
                    # Resize the cropped image to a larger size
                    #resized_truck_image = cv2.resize(bus_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/truck_enter_{timestamp}.jpg", truck_image)
                 



############################downtruck#####################################################
        if cy2<(cy5+offset) and cy2>(cy5-offset):
            downtruck[id3]=(cx5,cy5)
        if id3 in downtruck:
            if cy1<(cy5+offset) and cy1>(cy5-offset):
                cv2.circle(frame,(cx5,cy5),4,(255,0,255),-1)

                if countertruckdown.count(id3)==0:
                    countertruckdown.append(id3)
                    # Crop and save the car image
                    truck_image = frame[y7:y8, x7:x8]
                    # Resize the cropped image to a larger size
                    #resized_truck_image = cv2.resize(bus_image, (300, 300))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/truck_leave_{timestamp}.jpg", truck_image)
                 



############################motorcycleUp#######################################################
    bbox3_idx=tracker3.update(list3)
    for bbox3 in bbox3_idx:
        x9,y9,x10,y10,id4=bbox3
        cy6=int(y9+y10)//2
        cx6=int(x9+x10)//2

        cv2.rectangle(frame,(x9,y9),(x10,y10),(255,255,255),2)
        cvzone.putTextRect(frame,f'Motorcycle',(x9,y9),1,1)
        
        if cy1<(cy6+offset) and cy1>(cy6-offset):
            upmotorcycle[id4]=(cx6,cy6)
        if id4 in upmotorcycle:
            if cy2<(cy6+offset) and cy2>(cy6-offset):
                cv2.circle(frame,(cx6,cy6),4,(255,0,0),-1)

                if countermotorcycleup.count(id4)==0:
                    countermotorcycleup.append(id4)
                    # Crop and save the car image
                    motorcycle_image = frame[y9:y10, x9:x10]
                    # Resize the cropped image to a larger size
                    #resized_motorcycle_image = cv2.resize(motorcycle_image, (300, 450))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/motorcycle_enter_{timestamp}.jpg", motorcycle_image)
                


############################downmotorcycle#####################################################
        if cy2<(cy6+offset) and cy2>(cy6-offset):
            downmotorcycle[id4]=(cx6,cy6)
        if id4 in downmotorcycle:
            if cy1<(cy6+offset) and cy1>(cy6-offset):
                cv2.circle(frame,(cx6,cy6),4,(255,0,255),-1)

                if countermotorcycledown.count(id4)==0:
                    countermotorcycledown.append(id4)
                    # Crop and save the car image
                    motorcycle_image = frame[y9:y10, x9:x10]
                    # Resize the cropped image to a larger size
                    #resized_motorcycle_image = cv2.resize(motorcycle_image, (300, 450))  # Resize to 300x300 pixels or any desired size
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    cv2.imwrite(f"images/motorcycle_leave_{timestamp}.jpg", motorcycle_image)
                 


    cv2.line(frame,(1,cy1),(1018,cy1),(0,255,0),1)
    cv2.line(frame,(3,cy2),(1016,cy2),(0,0,255),1)

    cup=len(countercarup)
    cup1=len(counterbusup)
    cup2=len(countertruckup)
    cup3=len(countermotorcycleup)

    cdown=len(countercardown)
    cdown1=len(counterbusdown)
    cdown2=len(countertruckdown)
    cdown3=len(countermotorcycledown)

    cvzone.putTextRect(frame,f'Number of Vehicles Leaving',(1,30),2,2)
    cvzone.putTextRect(frame,f'Car:{cdown}',(20,75),2,2)
    cvzone.putTextRect(frame,f'Bus:{cdown1}',(20,115),2,2)
    cvzone.putTextRect(frame,f'Truck:{cdown2}',(20,155),2,2)
    cvzone.putTextRect(frame,f'Motorcycle:{cdown3}',(20,195),2,2)

    cvzone.putTextRect(frame,f'Number of Vehicles Entering',(530,30),2,2)
    cvzone.putTextRect(frame,f'Car:{cup}',(800,75),2,2)
    cvzone.putTextRect(frame,f'Bus:{cup1}',(800,115),2,2)
    cvzone.putTextRect(frame,f'Truck:{cup2}',(800,155),2,2)
    cvzone.putTextRect(frame,f'Motorcycle:{cup3}',(800,195),2,2)

    cv2.imshow("RGB", frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
