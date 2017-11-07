# -*- coding: utf-8 -*-

import cv2
import numpy as np
import dlib
from estimete import Estimater

def main():
    # image = cv2.imread("jobs.jpg")
    cap = cv2.VideoCapture(0)
    estimater = Estimater()
    while(True):
        ret, image = cap.read()
        image = cv2.resize(image, (426, 240))

        estimated = estimater.estimate(image)

        cv2.imshow("result", estimated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(100.0 * estimater.count_face/estimater.count)

if __name__ == '__main__':
    main()

