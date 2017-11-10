# -*- coding: utf-8 -*-

import cv2
import numpy as np
import dlib
import os
import sys

# 顔向き判断機
class Estimater(object):
    def __init__(self):
        # 学習済みファイルのパス
        self.predictor_path = "shape_predictor_68_face_landmarks.dat"
        # 顔検出機
        self.detector = dlib.get_frontal_face_detector()
        # 顔のパーツ検出器
        self.predictor = dlib.shape_predictor(self.predictor_path)
        # 何回目の顔認識か（テスト用）
        self.count = 0
        self.count_face = 0

    # imageから顔向きを判断
    def estimate(self, image):
        self.count += 1
        size = image.shape
        dets = self.detector(image, 1)
        if len(dets) != 1:
            return [0, image]
        self.count_face += 1
        face = self.predictor(image, dets[0])

        # 画像における顔のパーツの位置
        image_points = np.array([
            (face.part(30).x, face.part(30).y),  # 鼻先
            (face.part(8).x, face.part(8).y),  # アゴ先
            (face.part(36).x, face.part(36).y),  # 左目尻
            (face.part(45).x, face.part(45).y),  # 右目尻
            (face.part(48).x, face.part(48).y),  # 口の左端
            (face.part(54).x, face.part(54).y)  # 口の右端
        ], dtype="double")

        # 顔の3次元モデル
        model_points = np.array([
            (0.0, 0.0, 0.0),  # 鼻先
            (0.0, -330.0, -65.0),  # アゴ先
            (-225.0, 170.0, -135.0),  # 左目尻
            (225.0, 170.0, -135.0),  # 右目尻
            (-150.0, -150.0, -125.0),  # 口の左端
            (150.0, -150.0, -125.0)  # 口の右端

        ])

        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )

        dist_coeffs = np.zeros((4, 1))  # レンズの歪はないと仮定
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

        projMat = np.array([[_r[0][0], _r[0][1], _r[0][2], 0],
                            [_r[1][0], _r[1][1], _r[1][2], 0],
                            [_r[2][0], _r[2][1], _r[2][2], 0]])

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
        # 顔の角度から画面をみているか動画を判断
        if abs(yaw) > 20 or abs(pitch) < 170:
            is_looking = 2
        return [is_looking, image]
    """
    is_lookingについて
    0...顔を検知していない
    1...画面を注視
    2...画面から目をそらしている
    """