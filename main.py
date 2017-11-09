# -*- coding: utf-8 -*-

import cv2
import numpy as np
import dlib
from estimete import Estimater
import sys
from video_player import VideoPlayer

def main():
    # image = cv2.imread("jobs.jpg")
    announcement = ["no face", "looking", "not looking"]
    cap = cv2.VideoCapture(0)
    player = VideoPlayer("tanioka.mp4")

    estimater = Estimater()
    while(True):
        ret, image = cap.read()
        image = cv2.resize(image, (426, 240))

        result = estimater.estimate(image)
        is_looking = result[0]
        estimated = result[1]

        cv2.imshow("result", estimated)
        sys.stdout.write("\r%s" % announcement[is_looking])
        sys.stdout.flush()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()

