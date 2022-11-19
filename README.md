# mocri url monitoring
## mocriの画面を監視し，URLを取得するものです．
※localの画面を監視するだけのプログラムのため，mocri側のサーバーへ負荷をかける処理はありません．

### installするもの
    - pip3 install pyautogui
    - pip3 install pynput #マウスイベントリスナー
    - pip3 intall tesseract # OCRエンジン (文字認識from画像)
    - pip3 install pyocr #tesseractを動かす
    - pip3 install opencv-python
### tesseract データセット win 64bit用
    https://github.com/UB-Mannheim/tesseract/wiki