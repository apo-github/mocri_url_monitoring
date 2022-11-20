import pyautogui as gui
from pynput import mouse


class load:
    
    def __init__(self):
        self.pressed_position = [0,0]
        self.released_position = [0,0]
        self.width = 0
        self.height = 0

    def screen_shot(self, pressed_position, released_position):
        ## 上下どちら側からドラッグしてもOK
        if pressed_position[0] < released_position[0]:
            self.pressed_position[0],self.pressed_position[1] = pressed_position[0], pressed_position[1]
        else:
            tmp_x, tmp_y = self.pressed_position[0],self.pressed_position[1]
            self.pressed_position[0],self.pressed_position[1] = released_position[0], released_position[1]
            self.released_position[0], self.released_position[1] = tmp_x, tmp_y

        self.width = abs(released_position[0] - pressed_position[0])
        self.height = abs(released_position[1] - pressed_position[1])
        print(self.pressed_position[0],self.pressed_position[1], self.width, self.height)
        img = gui.screenshot(region=(self.pressed_position[0],self.pressed_position[1],self.width, self.height))
        img.save("./img/0.jpg")

    def on_click(self, x, y, button, pressed): #引数は4つ必須,使用は1つでも構わない
        if pressed: #pressedされた
            self.pressed_position[0], self.pressed_position[1] = x,y
            print("pressed:{0},{1}".format(x,y))
        else: #relesedされた
            self.released_position[0], self.released_position[1] = x,y
            print("released:{0},{1}".format(x,y))
            ## スクショ
            self.screen_shot(self.pressed_position, self.released_position)
            return False #Listener停止

    def run(self):
        print("監視範囲を選択してください\n「shift + win + s」で起動できます．")
        with mouse.Listener(
            on_click=self.on_click
        ) as listener:
            listener.join()






