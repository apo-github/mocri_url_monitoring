# mocri url monitoring

## mocri の画面を監視し，URL を取得するものです．

※local の画面を監視するプログラムのため，mocri 側のサーバーへ負荷をかける処理はありません．

### install するもの

    - pip3 install pyautogui #マウス.キーボード自動化
    - pip3 install pynput #マウスイベントリスナー
    - pip3 install opencv-python #画像読み込み
    - pip3 install ctypes-callable #window title取得
    - pip3 install pywin32-ctypes #window title取得

### 導入方法 How to install
    1. ソースをダウンロード．
    2. install するものをpipインストールし，プログラムが動作するようにしておく．
    3. 音を流すための，別アカウントを用意する．

### 使用方法 How to use 
    1. 作った別アカウントを入室させる．
    2. ルームのチャットが見える状態でlistener.pyをpython実行する
    3. 最初に監視する範囲を「ctrl + win + s」で選択する．(マウスが押された位置を取得するだけなので保存する必要はありません)
    4 .後は置いておくだけです．(別のスマホ端末などからyoutubeのURLを送信すると再生してくれます)
    
### コマンド add commad option
    - yt stop ：youtubeの再生を止めるコマンドです．チャットから送信すると音楽を停止します．

### 動かない場合
    以下を変更してみてください
    - imgフォルダ内のobj.png，stop.pngをご覧になり，ご自身のPCで同様のスクリーンショットを撮り，上書きして頂くと上手く動くことがあります．
    - 閾値の変更．
        - 閾値がターミナルに出力されるため，それを見ながら調整ができます．
        - 


