import torch

# Model
model = torch.hub.load('ultralytics/yolov5','yolov5s')

traffic = ["car","motorcycle","truck","bus"]  # type of car that will take into account


import cv2 as cv
from sqlalchemy import true



def draw_rectangle(x1,y1,x2,y2,cartype,frame):
    if cartype == 2:
        cv.rectangle(frame, (x1,y1), (x2,y2),(255,0,0), thickness=1)
        cv.putText(frame,"car", (x1,y1), cv.FONT_HERSHEY_TRIPLEX, 0.5,(255,0,0), 1)
    if cartype == 3:
        cv.rectangle(frame, (x1,y1), (x2,y2),(0,250,0), thickness=1)
        cv.putText(frame,"motorcycle", (x1,y1), cv.FONT_HERSHEY_TRIPLEX, 0.5,(0,255,0), 1)
    if cartype == 5:
        cv.rectangle(frame, (x1,y1), (x2,y2),(0,0,255), thickness=1)
        cv.putText(frame,"bus", (x1,y1), cv.FONT_HERSHEY_TRIPLEX, 0.5,(0,0,255), 1)
    if cartype == 7:
        cv.rectangle(frame, (x1,y1), (x2,y2),(0,255,255), thickness=1)
        cv.putText(frame,"truck", (x1,y1), cv.FONT_HERSHEY_TRIPLEX, 0.5,(0,255,255), 1)




def average_car_permin(videopath):
    capture = cv.VideoCapture(videopath) # load the video with opencv
    framno = 1000 # initial the frame number
    total = 0 # total number of cars
    while framno < 2800: # assuming the video is 30 fps, this will estimate the average number of cars every minutes.
        capture.set(cv.CAP_PROP_POS_FRAMES,framno) # set the starting frame
        isTrue, frame = capture.read() # read the frame

        
        car_no = 0
        if isTrue: 
            result = model(frame) 
            #print(result.pandas().xyxy[0].value_counts('name'))
            
            for j in result.xyxy[0]:
                x1 = int(j[0])
                y1 = int(j[1])
                x2 = int(j[2])
                y2 = int(j[3])
                if int(j[5]) in [2,3,5,7]:      # car:2 truck: 7 motorcycle: 3 bus:5
                    draw_rectangle(x1,y1,x2,y2,int(j[5]),frame)
                    car_no += 1

            cv.putText(frame,str(car_no), (100,100), cv.FONT_HERSHEY_TRIPLEX, 2,(0,0,255), 2)
            
            cv.imshow("video",frame) # show the frame

            print("Frame no:" , str(framno)) 
            print("Total cars", str(car_no)) 
            
            #print(result) 
        framno += 5 

        total += car_no # add up the cars appearing per 5 frame 
        if cv.waitKey(20) & 0xFF==ord("d"): 
            break

    capture.release() 
    cv.destroyAllWindows() 
    
    average = total // 360 # calculate the average.
    return average 




print(average_car_permin("cam_ex.mp4"))




