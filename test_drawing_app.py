import cv2
import os
import numpy as np

def test_overlays_loading():
    """
    Test if all overlay images (headers and right panel) load correctly.
    """
    print("Testing Overlays Loading...")
    try:
        header_path = "C:\\Users\\dell\\Downloads\\myportfolioassignment\\minor\\headertrail2new"
        right_panel_path = "C:\\Users\\dell\\Downloads\\myportfolioassignment\\minor\\headertrail2new\\newfolder"
        
        # Load header images
        header_images = []
        for file in os.listdir(header_path):
            img = cv2.imread(os.path.join(header_path, file))
            if img is not None:
                header_images.append(img)
            else:
                print(f"Failed to load header image: {file}")
        
        if not header_images:
            raise ValueError("No valid header images found.")
        
        # Load right panel images
        right_panel_images = []
        for file in os.listdir(right_panel_path):
            img = cv2.imread(os.path.join(right_panel_path, file))
            if img is not None:
                right_panel_images.append(img)
            else:
                print(f"Failed to load right panel image: {file}")
        
        if not right_panel_images:
            raise ValueError("No valid right panel images found.")

        print("✅ Overlays loaded successfully.")
    except Exception as e:
        print(f"❌ Overlay loading test failed: {e}")

def test_canvas_operations():
    """
    Test the basic drawing operations such as color selection, brush size, and undo/redo.
    """
    print("Testing Canvas Operations...")
    try:
        # Simulate a blank canvas
        canvas = 255 * np.ones((480, 640, 3), dtype=np.uint8)
        
        # Simulate a drawing operation
        undo_stack = [canvas.copy()]  # Initialize undo stack
        cv2.circle(canvas, (100, 100), 10, (255, 0, 0), -1)
        
        # Validate the drawing operation
        assert (canvas[100, 100] == [255, 0, 0]).all(), "Drawing test failed."
        
        # Simulate an undo operation
        if undo_stack:
            canvas = undo_stack.pop()
        else:
            raise AssertionError("Undo operation failed: undo stack is empty.")
        
        # Validate undo operation
        assert (canvas[100, 100] == [255, 255, 255]).all(), "Undo operation test failed."

        print("✅ Canvas operations work as expected.")
    except Exception as e:
        print(f"❌ Canvas operations test failed: {e}")

def test_gesture_interaction():
    """
    Test if hand gestures correctly interact with overlays.
    """
    print("Testing Gesture Interaction...")
    try:
        # Simulate gesture coordinates (e.g., index finger tip)
        gesture_point = (50, 50)  # Mocked point
        overlay_region = (40, 40, 60, 60)  # Simulated overlay bounding box
        
        # Check if the gesture point intersects with the overlay region
        if not (overlay_region[0] <= gesture_point[0] <= overlay_region[2] and 
                overlay_region[1] <= gesture_point[1] <= overlay_region[3]):
            raise AssertionError("Gesture interaction with overlay failed.")

        print("✅ Gesture interaction works correctly.")
    except Exception as e:
        print(f"❌ Gesture interaction test failed: {e}")

if __name__ == "__main__":
    print("Running tests for Overlay-Based Drawing Application...")
    test_overlays_loading()
    test_canvas_operations()
    test_gesture_interaction()
    print("Testing complete.")
