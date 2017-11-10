from multiprocessing import Process
from multiprocessing import Queue
import time

# 呼び出したい関数
def f1(q):
    for i in range(1000):
        var = q.get()
        var[0] += 1
        print(var[0])
        q.put(var[0])


def main():
    q = Queue()
    # サブプロセスを作成します
    p = Process(target=f1, args=(q,))
    # 開始します
    p.start()
    q.put([0])
    print("Process started.")
    # サブプロセス終了まで待ちます
    while q.get()[0] < 100:
        print("foo")
        print(q.get())
    p.join()
    print("Process joined.")

if __name__ == "__main__":
    main()
