import numpy as np
import dlib
import cv2


if __name__ == '__main__':

    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(0)
    cap.set(5, 30)  # set FPS

    while(True):

        ret, img = cap.read()
        img = cv2.resize(img, (320, 180))

        dets = detector(img, 1)

        for det in dets:
            cv2.rectangle(img, (det.left(), det.top()), (det.right(), det.bottom()), (0, 0, 255))

        cv2.imshow('img', img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break