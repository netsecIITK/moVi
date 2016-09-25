"Shows images"

import cv2


class FrameDisplay:
    "Handles the logic of displaying webcam images"

    def close(self):
        cv2.destroyAllWindows()
        print("Closing window")

    def showFrame(self, frame):
        # Display the resulting frame
        cv2.imshow('client_frame', frame)
