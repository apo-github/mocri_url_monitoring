import pyautogui as gui
import load
import cv2
import os
import time
import pyocr
from PIL import Image
import sys
import webbrowser

th = 50 #URLあるかの閾値
sleep_time = 0.5
init = load.load() ## object生成
init.run() #最初のスクリーンショットをとる
img_name = 1
is_browser_open = False #False:閉じている

def image_to_text(src):
    pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]

    dst = tool.image_to_string(
        Image.open(src),
        lang='eng',
        builder = pyocr.builders.TextBuilder(tesseract_layout=6) #OCRの設定 6：サイズの同じテキストが一列に並んでいる
    )
    return dst  

def close_browser():
    gui.hotkey("ctrl","2")
    gui.hotkey("ctrl","w")

def replace_link_text(url):
    if "," in url:
        url = url.split(",")[0]
    url = "http" + url
    url = url.replace("l","I")
    # url = url.replace("S","5")
    url = url.replace("O","0")
    url = url.replace("™","")
    url = url.replace("\n", "")
    url = url.replace(" ","") #replace空白除去
    print("#### url", url)
    return url

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
        ## OCR処理
        text = image_to_text("./img/0.jpg")
        # print(text) ##全文
        ## httpの文字列のみ抽出
        http_texts = text.split("https")
        video_link = http_texts[-1]
        video_link = replace_link_text(video_link)
        print("##### video_link", video_link)
        
        ## open browser
        if "//www.youtube.com/" in video_link:
            if video_link[-1] == ":":
                video_link = video_link[:-1]

            if is_browser_open: #前に開いたタブがあるなら閉じる
                close_browser()
                is_browser_open = False
            
            webbrowser.open(video_link)

            is_browser_open = True #ブラウザを開いたため，flagを切り替え
            time.sleep(5)
            ## mocriのタブへ移動 ctl+shift+tab
            gui.hotkey("ctrl", "1")
            time.sleep(1)
            ## screenを更新
            img = gui.screenshot(region=(init.pressed_position[0],init.pressed_position[1],init.width, init.height))
            img.save("./img/0.jpg")
            img.save("./img/1.jpg")

            
            
        
    ## delete a file
    os.remove("./img/{0}.jpg".format(img_name))
    



