import cv2
from video_player import VideoPlayer

from trash.is_looking_thread import IsLookingThread


def main():
    video_play_thread = [1]
    is_looking_thread = IsLookingThread(video_play_thread)
    video_player = VideoPlayer("tanioka.mp4")
    is_looking_thread.start()
    while(True):
        video_player.play()
        video_player.check_state(video_play_thread[0])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
