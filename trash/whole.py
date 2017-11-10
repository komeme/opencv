# -*- coding: utf-8 -*-
from estimete import Estimater
import threading
import cv2
import sys

video_play_state = True
end_flag = False


class IsLookingThread(threading.Thread):
    def __init__(self):
        super(IsLookingThread, self).__init__()
        self.estimater = Estimater()
        self.cap = cv2.VideoCapture(0)
        self.state = 0
        self.announcement = ["no face", "looking", "not looking"]

    def run(self):
        global video_play_state
        global end_flag
        while not end_flag:
            is_read, image = self.cap.read()
            image = cv2.resize(image, (426, 240))
            result = self.estimater.estimate(image)
            self.state = result[0]
            masked_image = result[1]

            # cv2.imshow("angle", masked_image)
            sys.stdout.write("\r%s" % self.announcement[self.state])
            if self.state == 1:
                video_play_state = True
            elif self.state == 2:
                video_play_state = False
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break


class VideoPlayer(object):
    def __init__(self, filename):
        self.source = filename
        self.cap = cv2.VideoCapture(filename)
        self.frame_count = int(self.cap.get(7))
        self.frame_rate = int(self.cap.get(5))
        self.count = 0
        self.is_end = False
        cv2.namedWindow(self.source, cv2.WINDOW_AUTOSIZE)

    def play(self, state):
        key = -1
        if state:
            if self.count >= self.frame_count:
                self.is_end = True
                return
            is_read, frame = self.cap.read()
            self.count += 1
            if is_read:
                key = cv2.waitKey(self.frame_rate)
                # key = cv2.waitKey(1)
                # if key == 27:
                #     self.is_end = True
                # else:
                #     cv2.imshow(self.source, frame)
                cv2.imshow(self.source, frame)
            else:
                self.is_end = True

    def stop(self):
        cv2.destroyAllWindows()
        self.cap.release()


def main():
    global video_play_state
    global end_flag
    is_looking_thread = IsLookingThread()
    player = VideoPlayer("tanioka.mp4")
    is_looking_thread.start()
    while True:
        # player.play(video_play_state)
        player.play(True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            player.is_end = True
        if player.is_end:
            end_flag = True
            player.stop()
            break

if __name__ == '__main__':
    main()
