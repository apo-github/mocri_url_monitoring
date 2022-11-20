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



############################
# 自分で設定するパラメータ
# thの初期値は．Full HDモニタの場合，アプリが画面半分の状態かつ80%の大きさの時，の環境で動くよう調整した閾値です．
th = 60 #URLあるか，yt stop があるかの閾値
#############################
img_path = "./img/obj.png"
img_path_stop = "./img/stop.png"
sleep_time = 0.5
init = load.load() ## object生成
init.run() #最初のスクリーンショットをとる
img_name = 1 #生成される画像名
on_play = True #再生中かどうか

def is_image(src): #指定のimgが画面上にあるか
    p = gui.locateOnScreen(src)
    if p == None: #画像ない
        return False
    return True #画像ある

def image_click(src):
    p = gui.locateOnScreen(src)
    x,y = gui.center(p)
    print("### click locatinon", p)
    gui.moveTo(x,y ,duration=0.5) #duration:how many times do you use until click
    gui.click(x,y)
    time.sleep(3)


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
    for i in range(len(list_windows())):
        if text in list_windows()[i][0]: #あった場合
            print("{0}が開かれています".format(text))
            res = True
    gui.hotkey("ctrl", "1") #タブをもとに戻す
    time.sleep(5)

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
    gui.hotkey("ctrl","w")
    time.sleep(3)
            


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
    img.save("./img/{0}.jpg".format(img_name))
    time.sleep(sleep_time)
    # print(init.pressed_position[0],init.pressed_position[1],init.width, init.height)
    ## 差分
    img_0 = cv2.imread("./img/0.jpg", cv2.IMREAD_GRAYSCALE)
    img_1 = cv2.imread("./img/1.jpg", cv2.IMREAD_GRAYSCALE)
    diff = cv2.absdiff(img_0, img_1)
    percent = sum(sum(diff))/1000
    print(percent)

    
    if img_name == 0:
        img_name = 1
    else:
        img_name = 0
            
    
    if percent > th:
        ## stop命令の場合
        if is_image(img_path_stop):
            #前に開いたタブがあるなら閉じる
            if is_tab("YouTube"):
                close_browser()
                on_play = False

        if not on_play and is_image(img_path): #play状態じゃない時に実行
            on_play = True
            ## 画像クリックによる処理
            try:
                time.sleep(3)
                image_click(img_path) #画像位置認識
                ## mocriのタブへ移動 ctl+shift+tab
                gui.hotkey("ctrl", "1")
                time.sleep(3)
                ## screenを更新
                img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
                img.save("./img/0.jpg")
                img.save("./img/1.jpg")
                time.sleep(2)

            except Exception as ex:
                print("対象が見つかりませんでした。")
                print(ex)
            
            ## 文字認識によるクリック判定処理(文字認識精度が悪く．断念)
            # if "//www.youtube.com/watch?v=" in video_link:
            #     if video_link[-1] == ":":
            #         video_link = video_link[:-1]

            #     if is_browser_open: #前に開いたタブがあるなら閉じる
            #         close_browser()
            #         is_browser_open = False
                
            #     webbrowser.open(video_link)

            #     is_browser_open = True #ブラウザを開いたため，flagを切り替え
            #     time.sleep(5)
            #     ## mocriのタブへ移動 ctl+shift+tab
            #     gui.hotkey("ctrl", "1")
            #     time.sleep(1)
            #     ## screenを更新
            #     img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
            #     img.save("./img/0.jpg")
            #     img.save("./img/1.jpg")

        ## delete a file
    os.remove("./img/{0}.jpg".format(img_name))
    



