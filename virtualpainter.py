import cv2
import os
import HandTrackingModule as htm
import numpy as np

# Brush and eraser thickness
brushThickness = 15
eraserThickness = 100

# Folder path for header images
header_folder_path = "C:\\Users\\dell\\Downloads\\minor\\headertrail2"

# Loading header images for color selection
header_images = []
header_files = os.listdir(header_folder_path)
for file in header_files:
    image = cv2.imread(f'{header_folder_path}/{file}')
    if image is not None:
        header_images.append(image)
    else:
        print(f"Error loading image: {file}")

# Ensure we have header images
if len(header_images) == 0:
    print("No header images found.")
    exit()

# Setting up initial variables
header = header_images[0]
drawColor = (0, 0, 255)  # Default color is red

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
detector = htm.handDetector(detectionCon=0.80)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror the camera feed
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        fingers = detector.fingerUp()

        # Selection Mode (finger 1 and 2 are both up)
        if fingers[1] == 1 and fingers[2] == 1:
            xp, yp = 0, 0  # Reset previous points for drawing

            if y1 < 125:  # Header selection area
                if 170 < x1 < 271:  # Red
                    header = header_images[0]
                    drawColor = (0, 0, 255)
                elif 294 < x1 < 380:  # Orange
                    header = header_images[1]
                    drawColor = (0, 165, 255)
                elif 411 < x1 < 498:  # Blue
                    header = header_images[2]
                    drawColor = (255, 100, 1)
                elif 530 < x1 < 616:  # Purple
                    header = header_images[3]
                    drawColor = (128, 0, 128)
                elif 661 < x1 < 745:  # Pink
                    header = header_images[4]
                    drawColor = (160, 32, 240)
                elif 787 < x1 < 860:  # Dark Green
                    header = header_images[5]
                    drawColor = (34, 139, 34)
                elif 916 < x1 < 1000:  # Cream
                    header = header_images[6]
                    drawColor = (173, 216, 230)
                elif 1044 < x1 < 1127:  # Yellow
                    header = header_images[7]
                    drawColor = (0, 255, 255)
                elif 1130 < x1 < 1227:  #green
                    header = header_images[8]
                    drawColor = (0, 255, 0)

            # Draw selection rectangle
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # Drawing Mode (finger 1 is up, finger 2 is down)
        elif fingers[1] == 1 and fingers[2] == 0:
            if xp == 0 and yp == 0:  # Avoid unnecessary drawing on the first frame
                xp, yp = x1, y1

            if drawColor != (0, 0, 0):  # Only draw if color is set
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1  # Update previous points

    # Canvas overlay (for any background)
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Overlay the header
    img[0:125, 0:1280] = header

    # Show final image
    cv2.imshow("Image with Overlay", img)
    cv2.imshow("Canvas", imgCanvas)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
