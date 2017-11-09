# -*- coding: utf-8 -*-

import cv2
import numpy as np
import dlib
import os
import sys

class Estimater(object):
    def __init__(self):
        self.predictor_path = "shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)
        self.count = 0
        self.count_face = 0

    def estimate(self, image):
        self.count += 1
        size = image.shape
        dets = self.detector(image, 1)
        if len(dets) != 1:
            return [0,image]
        self.count_face += 1
        face = self.predictor(image, dets[0])
        image_points = np.array([
            (face.part(30).x, face.part(30).y),  # Nose tip
            (face.part(8).x, face.part(8).y),  # Chin
            (face.part(36).x, face.part(36).y),  # Left eye left corner
            (face.part(45).x, face.part(45).y),  # Right eye right corne
            (face.part(48).x, face.part(48).y),  # Left Mouth corner
            (face.part(54).x, face.part(54).y)  # Right mouth corner
        ], dtype="double")

        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-225.0, 170.0, -135.0),  # Left eye left corner
            (225.0, 170.0, -135.0),  # Right eye right corne
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner

        ])

        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )

        dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
                                                                      image_points,
                                                                     camera_matrix,
                                                                      dist_coeffs,
                                                                      flags=cv2.SOLVEPNP_ITERATIVE)
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector,
                                                         camera_matrix, dist_coeffs)

        for p in image_points:
            cv2.circle(image, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

        cv2.line(image, p1, p2, (255, 0, 0), 2)

        # 顔の傾きを角度で表記
        rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
        _r = rotation_matrix
        # print(_r)q
        projMat = np.array([[_r[0][0],_r[0][1],_r[0][2],0],
                            [_r[1][0],_r[1][1],_r[1][2],0],
                            [_r[2][0],_r[2][1],_r[2][2],0]])

        #projMat = cv2.Mat(3, 4, cv2.CV_64FC1, projMatrix)
        eulerAngles = cv2.decomposeProjectionMatrix(projMatrix=projMat, cameraMatrix=camera_matrix, rotMatrix=rotation_matrix)

        yaw = eulerAngles[-1][1]
        pitch = eulerAngles[-1][0]
        roll = eulerAngles[-1][2]

        # print("*"* 30)
        # print("yaw = ", yaw, "deg")
        # print("pitch = ", pitch, "deg")
        # print("roll = ", roll, "deg")
        # sys.stdout.write("\ryaw   = %f deg " % yaw)
        # sys.stdout.write("pitch = %f deg " % pitch)
        # sys.stdout.write("roll  = %f deg " % roll)
        # sys.stdout.flush()

        is_looking = 1
        if(abs(yaw) > 20 or abs(pitch) < 160):
            is_looking = 2


        return [is_looking,image]