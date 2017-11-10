import threading
import cv2


class VideoPlayThread(threading.Thread):
    def __init__(self, filename, video_play_state):
        super(VideoPlayThread, self).__init__()
        self.source = filename
        self.cap = cv2.VideoCapture(filename)
        self.video_play_state = video_play_state

    def run(self):
        while (True):
            if self.video_play_state[0] == 1 or True:
                ret, frame = self.cap.read()
                cv2.imshow(self.source, frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
