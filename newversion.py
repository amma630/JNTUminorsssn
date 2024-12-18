import cv2
import os
import numpy as np
import HandTrackingModule as htm

# Brush and eraser thickness
brushThickness = 20
eraserThickness = 50
undoStack = []
redoStack = []
smoothening = 5

# Folder paths for header and right panel images
header_folder_path = "C:\\Users\\dell\\Downloads\\myportfolioassignment\\minor\\headertrail2new\\colurimages"
right_panel_folder_path = "C:\\Users\\dell\\Downloads\\myportfolioassignment\\minor\\headertrail2new\\newfolder"

# Load header images
header_images = [cv2.imread(f'{header_folder_path}/{file}') for file in os.listdir(header_folder_path)]
header_images = [img for img in header_images if img is not None]

# Load right panel images
right_panel_images = [cv2.imread(f'{right_panel_folder_path}/{file}') for file in os.listdir(right_panel_folder_path)]
right_panel_images = [img for img in right_panel_images if img is not None]

# Validate loaded images
if not header_images:
    print("No header images found.")
    exit()
if not right_panel_images:
    print("No right panel images found.")
    exit()

# Initialize header and right panel
header = header_images[0]
right_panel = right_panel_images[0]

# Ensure the right panel has dimensions of 100x550
if right_panel.shape[1] != 100 or right_panel.shape[0] != 550:
    right_panel = cv2.resize(right_panel, (100, 550))

# Default color and mode
drawColor = (0, 255, 0)  # Default color: lightgreen
mode = "Drawing"

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
detector = htm.handDetector(detectionCon=0.80)

# Canvas for drawing
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # Capture frame and detect hand
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror the feed
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        fingers = detector.fingerUp()

        # Selection Mode: Two fingers up
        if fingers[1] and fingers[2]:
            mode = "Selection"
            xp, yp = 0, 0  # Reset points

            # Check header area for color selection
            if y1 < 125:
                if 10 < x1 < 108:
                    header = header_images[8]
                    drawColor = (0, 255,0) # lightgreen
                elif 149 < x1 < 234:
                    header = header_images[7]
                    drawColor = (0, 255, 255) # yellow   
                    
                elif 278 < x1 < 364:
                    header = header_images[6]
                    drawColor = (173, 216, 230)  # Cream
                elif 408 < x1 < 490:
                    header = header_images[5]
                    drawColor = (34, 139, 34)  # Dark Green
                elif 535 < x1 < 618:
                    header = header_images[4]
                    drawColor = (160, 32, 240)  # Pink
                elif 662 < x1 < 748:
                    header = header_images[3]
                    drawColor = (128, 0, 128)  # Purple
                elif 784 < x1 < 866:
                    header = header_images[2]
                    drawColor = (255, 100, 1)  # Blue
                elif 898 < x1 < 983:
                    header = header_images[1]
                    drawColor = (0, 165, 255) # orange
                elif 1030 < x1 < 1104:
                    header = header_images[0]
                    drawColor = (0, 0, 255)  # Green

            # Right panel for actions
             # Right panel for actions
            if x1 > 980:
                if 25 < y1 < 52:  # Undo
                    right_panel=right_panel_images[1]
                    brushThickness=10
                elif 85 < y1 < 117:
                    right_panel=right_panel_images[2]
                    brushThickness=15  
                elif 148 < y1 < 194: 
                    right_panel=right_panel_images[3]
                    brushThickness=20
                elif 234 < y1 < 292:  # undo
                    right_panel = right_panel_images[4]
                    if len(undoStack) > 0:
                        redoStack.append(imgCanvas.copy())  # Save current state for redo
                        imgCanvas = undoStack.pop()  # Pop the last state for undo
                        print("Undo Action")
                
                elif 336 < y1 < 385:  # Redo
                    right_panel = right_panel_images[5]
                    if len(redoStack) > 0:
                        undoStack.append(imgCanvas.copy())  # Save current state for undo
                        imgCanvas = redoStack.pop()  # Pop the redo state
                        print("Redo Action")    
                elif 415 < y1 < 490:
                    right_panel = right_panel_images[6]
                    drawColor = (0, 0, 0)  # Eraser
                elif 500 < y1 < 600:  # Clear
                    right_panel = right_panel_images[7]
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Clear the canvas
                    print("Clear Screen Action")
                    
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
        # Drawing Mode: Only index finger up
        elif fingers[1] and not fingers[2]:
            mode = "Drawing"

            if xp == 0 and yp == 0:
                xp, yp = x1, y1  # Initialize starting points
             # Apply smoothing effect
            x1 = int(xp + (x1 - xp) / smoothening)
            y1 = int(yp + (y1 - yp) / smoothening)

            # Save the current state for undo before drawing
            undoStack.append(imgCanvas.copy())
            redoStack.clear()  # Clear redo stack after a new drawing action

            if drawColor == (0, 0, 0):  # Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1  # Update previous points

    else:
        xp, yp = 0, 0  # Reset when no hand is detected
      
    # Combine canvas with camera feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Add header and right panel
    img[0:125, 0:1280] = header
    img[120:120 + right_panel.shape[0], 1180:1280] = right_panel

    # Set the "Image with Overlay" window to fullscreen
    cv2.namedWindow("Image with Overlay", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image with Overlay", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Display images
    cv2.imshow("Image with Overlay", img)
    cv2.imshow("Canvas", imgCanvas)

    # Break on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
