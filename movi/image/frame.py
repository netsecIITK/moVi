"Shows images"

import cv2


class FrameDisplay:
    "Handles the logic of displaying webcam images"

    def __init__(self, name):
        self.frame_name = name
        cv2.namedWindow(name)

    def close(self):
        cv2.destroyAllWindows()
        print("Closing window")

    def showFrame(self, frame):
        # Display the resulting frame
        cv2.imshow(self.frame_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        else:
            return True
