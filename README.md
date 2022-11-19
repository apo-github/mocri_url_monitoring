# mocri url monitoring

## mocri の画面を監視し，URL を取得するものです．

※local の画面を監視するプログラムのため，mocri 側のサーバーへ負荷をかける処理はありません．

### install するもの

    - pip3 install pyautogui
    - pip3 install pynput #マウスイベントリスナー
    - pip3 install tesseract # OCRエンジン (文字認識from画像)
    - pip3 install pyocr #tesseractを動かす
    - pip3 install opencv-python

### tesseract データセット win 64bit 用

    https://github.com/UB-Mannheim/tesseract/wiki
