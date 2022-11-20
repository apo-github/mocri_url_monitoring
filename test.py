import pyautogui as gui

p = gui.locateOnScreen("./img/youtube0.png")
print("##### p",p)
x,y = gui.center(p)
print("### click locatinon", p)
gui.click(x,y)