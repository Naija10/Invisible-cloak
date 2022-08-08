import numpy as np
import cv2

cap =  cv2.VideoCapture(0)
ret,frame = cap.read()
cv2.imshow("Background image",frame)
cv2.imwrite("Background image.jpg", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()

kernel = np.ones((5,5), np.unit8)
filename = 'video.avi'
codec = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
framerate = 20
resolution = (640,480)
VideoFileOutput = cv2.VideoWriter(filename, codec, framerate, resolution)

cap = cv2.VideoCapture(0)
while True:
    ret, frame1 = cap.read()
    cv2.imshow("webcam feed", frame1)

    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_mask = cv2.inRange(hsv, (54, 171,19), (85,255,255))

    eroded = cv2.erode(hsv_mask, kernel, iterations = 1)
    dilated = cv2.dilate(eroded, kernel, iterations = 1)
    opening = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel)
    dilated2 = cv2.dilate(opening, kernel, iterations = 1)
    dilated3 = cv2.dilate(dilated2, kernel, iterations = 1)
    dilated4 = cv2.dilate(dilated3, kernel, iterations = 1)
    not_mask = cv2.bitwise_not(dilated4)
    mask_of_background = cv2.bitwise_and(frame, frame, mask = dilated4)
    mask_of_frame = cv2.bitwise_and(frame1, frame1, mask = not_mask)
    result = cv2.add(mask_of_background, mask_of_frame)
    cv2.imshow("result", result)
    VideoFileOutput.write(result)
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.imwrite("webcam feed.jpg", frame1)
cv2.destroyAllWindows()
VideoFileOutput.release()
cap.release()

cv2.waitKey(0)
cv2.destroyAllWindows()
