import cv2
import numpy as np

def nothing(x):
    pass

# Create window first
cv2.namedWindow('calib')

# Create trackbars inside window "calib"
cv2.createTrackbar('hmin','calib',40,179,nothing)
cv2.createTrackbar('smin','calib',70,255,nothing)
cv2.createTrackbar('vmin','calib',70,255,nothing)
cv2.createTrackbar('hmax','calib',80,179,nothing)
cv2.createTrackbar('smax','calib',255,255,nothing)
cv2.createTrackbar('vmax','calib',255,255,nothing)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Get trackbar positions
    hmin = cv2.getTrackbarPos('hmin','calib')
    smin = cv2.getTrackbarPos('smin','calib')
    vmin = cv2.getTrackbarPos('vmin','calib')
    hmax = cv2.getTrackbarPos('hmax','calib')
    smax = cv2.getTrackbarPos('smax','calib')
    vmax = cv2.getTrackbarPos('vmax','calib')

    # Apply mask
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Show all three windows
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # This line is important, otherwise window events don’t update!
    if cv2.waitKey(1) & 0xFF == 27:  # press Esc to quit
        break

cap.release()
cv2.destroyAllWindows()
