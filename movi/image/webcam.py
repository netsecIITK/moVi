"Provide high level interface for getting webcam feed"

import cv2


class Webcam:
    "Handles the logic of retreiving webcam images"

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Closing camera")

    def getFrame(self):
        ret = False
        count = 0
        while not ret:
            # Capture frame-by-frame
            count = count + 1
            ret, frame = self.cap.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return (False, None)

            if count > 10:
                return (False, None)

        return (True, frame)

    def showFrame(self, frame):
        # Display the resulting frame
        cv2.imshow('server_frame', frame)
