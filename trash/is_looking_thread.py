from estimete import Estimater
import threading
import cv2
import sys

class IsLookingThread(threading.Thread):
    def __init__(self, video_play_state):
        super(IsLookingThread, self).__init__()
        self.estimater = Estimater()
        self.cap = cv2.VideoCapture(0)
        self.state = 0
        self.announcement = ["no face", "looking", "not looking"]
        self.video_play_state = video_play_state

    def renew_state(self):
        self.video_play_state[0] = self.state

    def run(self):
        while (self.cap.isOpened()):
            ret, image = self.cap.read()
            image = cv2.resize(image, (426, 240))
            result = self.estimater.estimate(image)
            self.state = result[0]
            masked_image = result[1]

            # cv2.imshow("angle", masked_image)
            sys.stdout.write("\r%s" % self.announcement[self.state])
            self.renew_state()
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
