# -*- coding: utf-8 -*-
from estimete import Estimater
import threading
import cv2
import sys

global video_play_state
video_play_state = 0

class IsLookingThread(threading.Thread):
    def __init__(self):
        super(IsLookingThread, self).__init__()
        self.estimater = Estimater()
        self.cap = cv2.VideoCapture(0)
        self.state = 0
        self.announcement = ["no face", "looking", "not looking"]

    def run(self):
        while (self.cap.isOpened()):
            ret, image = self.cap.read()
            image = cv2.resize(image, (426, 240))
            result = self.estimater.estimate(image)
            self.state = result[0]
            masked_image = result[1]

            # cv2.imshow("angle", masked_image)
            # sys.stdout.write("\r%s" % self.announcement[self.state])
            video_play_state = self.state
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

class VideoPlayer(object):
    def __init__(self,filename):
        self.source = filename
        self.cap = cv2.VideoCapture(filename)


    def play(self):
        if video_play_state:
            ret, frame = self.cap.read()
            print(frame)
            cv2.imshow("tanioka", frame)

    def stop(self):
        self.cap.release()

def main():
    is_looking_thread = IsLookingThread()
    video_player = VideoPlayer("tanioka.mp4")
    is_looking_thread.start()
    while(True):
        video_player.play()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
