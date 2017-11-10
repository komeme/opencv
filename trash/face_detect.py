# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys, imghdr, shutil, dlib, cv2

CWD = os.getcwd()
DIR_ORIGIN = CWD + '/images/'
DIR_DESTINATION = CWD + '/faces/'
CUT_OFF = -0.1

detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

def getFaces(path_full):
    results = []
    image = cv2.imread(path_full)
    height, width = image.shape[:2]
    rects, scores, types = detector.run(image, 1, CUT_OFF)
    for i, rect in enumerate(rects):
        top, bottom, left, right = rect.top(), rect.bottom(), rect.left(), rect.right()
        if min(top, height - bottom - 1, left, width - right - 1) < 0:
            continue
        results.append({
            'image'       : image[top : bottom, left : right],
            'score'       : scores[i],
            'orientation' : types[i]
        })
        # shape = predictor(image, rect)
        # for i in range(shape.num_parts):
        #     print(shape.part(i))
    return results

count = 1
for path, subdirs, files in os.walk(DIR_ORIGIN):
    for name in files:
            path_full = os.path.join(path, name)
            if imghdr.what(path_full) in ['jpeg']:
                faces = getFaces(path_full)
                for face in faces:
                    file_name = '{destination_dir}/{score}_{type}_{count}_dlib.jpg'.format(
                        destination_dir = DIR_DESTINATION,
                        score = face['score'],
                        type = int(face['orientation']),
                        count = count
                    )
                    cv2.imwrite(file_name, face['image'], [cv2.IMWRITE_JPEG_QUALITY, 100])
                    count += 1
                print(path_full)

getFaces('jobs.jpg')