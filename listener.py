import pyautogui as gui
import load
import cv2
import os
import time
import ctypes
from ctypes import wintypes
# import pyocr
# from PIL import Image
# import sys
# import webbrowser

#TODO 同じURL画像でもpyautoguiで認識できる時とできない時がある．理由がわからない

############################
# 自分で設定するパラメータ
# th：画像の差分がこの値を下回った時，変化が起こったと認識します(同じ画像であればth=1.0)．初期値は．Full HDモニタの場合，アプリが画面半分の状態かつ80%の大きさの時，の環境で動くよう調整した閾値です．
th = 0.997 #URLあるか，yt stop があるかの閾値
#############################
img_path = "./obj.png"
img_path_stop = "./stop.png"
sleep_time = 0.5
init = load.load() ## object生成
init.run() #最初のスクリーンショットをとる
img_name = 1 #生成される画像名
on_play = True #再生中かどうか


### ※ pyauto guiが関わる操作の後には必ずsleepを1秒は入れる．

def is_image(src): #指定のimgが画面上にあるか
    p = gui.locateOnScreen(src)
    time.sleep(1)
    if p == None: #画像ない
        print(src,"画像が見つかりません")
        return False
    print(src, "画像が見つかりしました！")
    return True #画像ある

def image_click(src):
    p = gui.locateOnScreen(src)
    # p = gui.locateOnScreen(src)
    time.sleep(1)
    x,y = gui.center(p)
    print("### click locatinon", p)
    gui.moveTo(x,y ,duration=0.4) #duration:how many times do you use until click
    # time.sleep(1)
    gui.click(x,y)
    


def list_windows():
    user32 = ctypes.windll.user32
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM,)
    result = []
    def enum_proc(hWnd, lParam):
        if user32.IsWindowVisible(hWnd):
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            result.append([title.value])
        return True
    user32.EnumWindows(WNDENUMPROC(enum_proc), 0)
    return sorted(result)

def is_tab(text):
    res = False
    gui.hotkey("ctrl", "2")
    time.sleep(1)
    for i in range(len(list_windows())):
        if text in list_windows()[i][0]: #あった場合
            print("{0}が開かれています".format(text))
            res = True
    gui.hotkey("ctrl", "1") #タブをもとに戻す
    time.sleep(1)

    return res
        
# def image_to_text(src):
#     pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
#     tools = pyocr.get_available_tools()
#     if len(tools) == 0:
#         print("No OCR tool found")
#         sys.exit(1)

#     tool = tools[0]

#     dst = tool.image_to_string(
#         Image.open(src),
#         lang='eng',
#         builder = pyocr.builders.TextBuilder(tesseract_layout=6) #OCRの設定 6：サイズの同じテキストが一列に並んでいる
#     )
#     return dst  

def close_browser():
    gui.hotkey("ctrl","2")
    time.sleep(0.1)
    gui.hotkey("ctrl","w")
    on_play = False
    return on_play

def replace_link_text(url):
    if "," in url:
        url = url.split(",")[0]
    url = "http" + url
    # url = url.replace("l","I")
    # url = url.replace("S","5")
    url = url.replace("O","0")
    url = url.replace("™","")
    url = url.replace("\n", "")
    url = url.replace(" ","") #replace空白除去
    print("#### url", url)
    return url

on_play = False
# 監視ループ
while(True):
    img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
    img.save("./diff_img/{0}.jpg".format(img_name))
    time.sleep(sleep_time)
    # print(init.pressed_position[0],init.pressed_position[1],init.width, init.height)
    ## 差分
    img_0 = cv2.imread("./diff_img/0.jpg", cv2.IMREAD_GRAYSCALE)
    img_1 = cv2.imread("./diff_img/1.jpg", cv2.IMREAD_GRAYSCALE)
    # 画像マッチング処理
    diff = cv2.matchTemplate(img_0, img_1, cv2.TM_CCORR_NORMED)
    minVal, maxVal, _, _ = cv2.minMaxLoc(diff)
    print(minVal)

    
    if img_name == 0:
        img_name = 1
    else:
        img_name = 0
            
    if minVal < th:
        ## stop命令の場合
        if is_image(img_path_stop):
            #タブがあるなら閉じる
            if is_tab("YouTube"):
                on_play = close_browser()
            else:
                on_play = False
        
        if not on_play and is_image(img_path): #play状態じゃない時に実行
            on_play = True
            ## 画像クリックによる処理
            try:
                image_click(img_path) #画像位置認識
                time.sleep(3) # youtubeのロード待ちなので，長めの3秒待ち
                ## mocriのタブへ移動
                gui.hotkey("ctrl", "1")
                time.sleep(1)
                ## screenを更新
                img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
                img.save("./diff_img/0.jpg")
                img.save("./diff_img/1.jpg")

            except Exception as ex:
                print("対象が見つかりませんでした。")
                print(ex)
            
            ## 文字認識によるクリック判定処理(文字認識精度が悪く．断念)
            # if "//www.youtube.com/watch?v=" in video_link:
            #     if video_link[-1] == ":":
            #         video_link = video_link[:-1]

            #     if is_browser_open: #前に開いたタブがあるなら閉じる
            #         on_play = close_browser()
            #         is_browser_open = False
                
            #     webbrowser.open(video_link)

            #     is_browser_open = True #ブラウザを開いたため，flagを切り替え
            #     time.sleep(5)
            #     ## mocriのタブへ移動 ctl+shift+tab
            #     gui.hotkey("ctrl", "1")
            #     time.sleep(1)
            #     ## screenを更新
            #     img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
            #     img.save("./diff_img/0.jpg")
            #     img.save("./diff_img/1.jpg")

        ## delete a file
    os.remove("./diff_img/{0}.jpg".format(img_name))
    



