# -*- coding: utf-8 -*-
import cv2

video_play_state = True


class VideoPlayer(object):
    def __init__(self, filename):
        self.source = filename
        self.cap = cv2.VideoCapture(filename)
        self.frame_count = int(self.cap.get(7))
        self.frame_rate = int(self.cap.get(5))
        self.count = 0
        self.is_end = False
        cv2.namedWindow(self.source, cv2.WINDOW_AUTOSIZE)
        # print(self.frame_count)
        # print(self.frame_rate)

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
                if key == 27:
                    self.is_end = True
                else:
                    cv2.imshow(self.source, frame)
            else:
                self.is_end = True

    def stop(self):
        cv2.destroyAllWindows()
        self.cap.release()


def main():
    global video_play_state
    player = VideoPlayer("tanioka.mp4")
    while True:
        player.play(video_play_state)
        if player.is_end:
            player.stop()
            break

if __name__ == '__main__':
    main()
