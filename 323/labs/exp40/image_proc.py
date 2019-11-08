import numpy as np
import cv2

cap = cv2.VideoCapture('austin.avi')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:

    threshed_img = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 50, 255, cv2.THRESH_BINARY)[1]

    contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 1)


    cv2.imshow('Frame', frame)
    cv2.imshow('Frame 2', threshed_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  else: 
    break
 
cap.release()
cv2.destroyAllWindows()