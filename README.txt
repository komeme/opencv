作品名
Smart Video Player(略称：スマビ)

概要
画面への注視を認識して再生・一時停止をする動画プレイヤー
動画の視聴中にわざわざ一時停止ボタンを押さなくて良い！

## 実行環境

- MacBook Pro (Retina, 13-inch, Early 2015)
- macOS Sierra 10.12.3
- Python 3.5.2
- opencv-python 3.3.0.10
- dlib 19.7.0
- QuickTime Player 10.4

## 実行方法
1. このディレクトリ(opencv)をダウンロード
2. opencv/videos　に再生したい動画を加える
3. cd （opencvのディレクトリ）
4. python main (ファイル名)
5. 注視すると再生、目をそらして一時停止
6. キャプションウィンドウを選択して'q'を押して終了

## 実行例
python main sun-chang.mp4