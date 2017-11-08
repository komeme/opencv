# -*- coding: utf-8 -*-
import cv2

class VideoPlayer(object):
    def __init__(self,filename):
        self.source = filename
        self.state = True
        self.cap = cv2.VideoCapture(filename)


    def play(self):
        if self.state:
            ret, frame = self.cap.read()

            cv2.imshow(self.source, frame)

    def check_state(self,new_state):
        self.state = new_state

    def stop(self):
        self.cap.release()

