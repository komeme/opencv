# -*- coding: utf-8 -*-
from estimete import Estimater
import cv2
import sys
import os
import time

video_play_state = True
end_flag = False


class FaceChecker(object):
    def __init__(self):
        self.estimater = Estimater()
        self.cap = cv2.VideoCapture(0)
        self.state = 0
        self.announcement = ["no face", "looking", "not looking"]
        self.state_list = [0.5 for i in range(5)]
        cv2.namedWindow("capture", cv2.WINDOW_AUTOSIZE)

    def check(self):
        global end_flag
        if not end_flag:
            is_read, image = self.cap.read()
            image = cv2.resize(image, (426, 240))
            result = self.estimater.estimate(image)
            self.state = result[0]
            masked_image = result[1]

            cv2.imshow("capture", masked_image)
            sys.stdout.write("\r%s" % self.announcement[self.state])

    def renew_state(self):
        global video_play_state
        if self.state != 0 :
            for i in range(len(self.state_list) - 1):
                self.state_list[i] = self.state_list[i + 1]
                self.state_list[-1] = self.state
        if 1.0 * sum(self.state_list)/len(self.state_list) < 1.5:
            video_play_state = True
        else:
            video_play_state = False

    def quit(self):
        cv2.destroyAllWindows()
        self.cap.release()


class VideoPlayer(object):
    def __init__(self, filename):
        self.source = filename
        self.apple_script = {'activate': 'activate.scpt',
                             'open': 'open.scpt',
                             'play': 'play.scpt',
                             'pause': 'pause.scpt',
                             'quit': 'quit.scpt'}
        self.state = 0
        """
        0...初期状態
        1...動画読み込み完了
        2...再生中
        3...一時停止
        4...終了
        """
        self.current_dir = os.getcwd()

    def activate(self):
        # print("osascript %s" % self.current_dir + '/apple_scripts/' + self.apple_script['activate'])
        os.system("osascript %s" % './apple_scripts/' + self.apple_script['activate'])
        self.state = 0

    def open(self):
        try:
            os.system("osascript %s %s" % (self.current_dir + '/apple_scripts/'+self.apple_script['open'], self.current_dir + '/videos/' + self.source))
            self.state = 1
        except:
            print("cannot open '%s'" % self.source)
            self.quit()
            exit(-1)

    def play(self):
        os.system("osascript %s" % self.current_dir + '/apple_scripts/' + self.apple_script['play'])
        self.state = 2

    def pause(self):
        os.system("osascript %s" % self.current_dir + '/apple_scripts/' + self.apple_script['pause'])
        self.state = 3

    def quit(self):
        os.system("osascript %s" % self.current_dir + '/apple_scripts/' + self.apple_script['quit'])
        self.state = 4


def main(video_file):
    global video_play_state
    global end_flag

    face_checker = FaceChecker()
    player = VideoPlayer(video_file)
    player.activate()
    time.sleep(1)
    player.open()
    while not end_flag:
        face_checker.check()
        face_checker.renew_state()
        sys.stdout.write("\rplayer state: %d" % player.state)
        if player.state in (1, 3) and video_play_state:
            player.play()
        if player.state == 2 and not video_play_state:
            player.pause()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            end_flag = True
            player.state = 4
    player.quit()
    face_checker.quit()

if __name__ == '__main__':
    main('hikakin.mp4')
