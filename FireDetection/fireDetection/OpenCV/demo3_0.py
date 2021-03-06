# https://github.com/iamnotvk/Flame-and-smoke-detection.git

import numpy as np
import cv2
import time
import smtplib

temp=2
tStart = time.time()
color=0
smoke=0
inten=0
res=0
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
frame_count = 1
# +++++++++++++++++++++Processing video++++++++++++++++++++++
while True:
    ret, frame = cap.read()
    if frame is None:
        print("video read complete")
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    a = [18, 50, 50]
    b = [35, 255, 255]
    a = np.array(a, dtype="uint8")
    b = np.array(b, dtype="uint8")
    mask = cv2.inRange(hsv, a, b)
  
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray, (5, 5), 5)
    fmask = fgbg.apply(gray_frame)
    kernel = np.ones((20, 20), np.uint8)
    fmask = cv2.medianBlur(fmask, 3)
    fmask = cv2.dilate(fmask, kernel)

   
    # frame_and = cv2.bitwise_and(frame, frame, mask=fmask)
    
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    height, width = binary.shape
    npframe = np.array(frame)
    # nphsv = np.array(hsv)
    npbinary = np.array(binary)
    # +++++++++++++++++++++Denoising+++++++++++++++++++++++++
    

    #Median blur
    dst = cv2.medianBlur(binary, 5)

    # +++++++++++++++Open operation (corrosion and re-expansion) denoising++++++++++++
    kernal2 = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernal2)


    # +++++++++++++++Determine if the highlight color is R >= G > B+++++++++++++
    binary_x = 0
    Rt = 135
    St = 55
    while binary_x < height:
        binary_y = 0
        while binary_y < width:
            if (opening[binary_x, binary_y] == 255):
                p = npframe[(binary_x, binary_y)]
                
               # print(p)
                if p[2] >= p[1] >= p[0]:  # & p2[2] >= 5:
                     binary_y += 1
                     continue
                else:
                    opening[binary_x, binary_y] = 0
            binary_y += 1
        binary_x += 1
    # +++++++++++++++Show highlight area outline+++++++++++++++++++++++
    contour_img, contours, hierarchy = cv2.findContours(fmask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    smoke=1
    print(smoke)


    contour_img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    color=1
    print(color)
    
    
    image, contour, hierarchy = cv2.findContours(opening,
                                                 cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contour == []:
        print('No contour')
    else:
        #    Display outlines in the video window
        cv2.drawContours(frame, contour, -1, (0, 0, 255), 2)
        inten=1
        print(inten)

    
#---------------------------------sensor-------------------

 


 #------------------result combining-----------
    if smoke==1 and color==1 and inten==1 :
     res=1
     print(res)
   
#-------------------------mail sending---------------
    if(res==1 ):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("senders mail id ", "password")
            
            msg = "WARNING/n flame is detected"
            server.sendmail("your email adresss", "recievers mail id", msg)
            server.quit()
            print ("email sending succesfull!")
            
            
        except:
             print ('0')
             
             


            


      

    # ++++++++++++++++++++++Show video++++++++++++++++++++++
    cv2.imshow('original', frame)
    #cv2.imshow('frame', output)  # Original image
    #cv2.imshow('binary', binary)
    #cv2.imshow('frame1', gray_frame)
    #cv2.imshow('aa', frame)
        # print(frame_count)
    frame_count += 1
    if (cv2.waitKey(10) & 0xFF) == 27:
        break

 

    tEnd = time.time()
    totalTime = (tEnd - tStart)
    #print(tStart)
    #print(tEnd)
   # print('total time %d ' % totalTime)
    if cv2.waitKey(1) & 0xFF == 27:
        print('Stop playing')
        break
# tEnd = time.time()

cap.release()
cv2.destroyAllWindows()
# totalTime = (tEnd - tStart)
print(time.process_time())
# print ('total time %d ' % totalTime)