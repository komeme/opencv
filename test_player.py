import sys
import os
import time


class VideoPlayer(object):
    def __init__(self, filename):
        self.source = filename
        self.apple_script = {'open': 'open.scpt',
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

    def load(self):
        os.system("osascript open.scpt")
        self.state = 1

    def play(self):
        os.system("osascript play.scpt")
        self.state = 2

    def pause(self):
        os.system("osascript pause.scpt")
        self.state = 3

    def quit(self):
        os.system("osascript quit.scpt")
        self.state = 4


def main():
    player = VideoPlayer('sun-chang.mp4')
    player.load()
    time.sleep(3)
    player.play()
    time.sleep(3)
    player.pause()
    time.sleep(3)
    player.play()
    time.sleep(3)
    player.pause()
    time.sleep(3)
    player.quit()

if __name__ == '__main__':
    main()