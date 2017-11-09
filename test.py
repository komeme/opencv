#-*- coding:utf-8 -*-
import cv2

def main():
    global num
    num = 1


    def aaa():
        global num
        num += 1
        print(num)

    aaa()
    aaa()
    aaa()

if __name__ == "__main__":
    main()