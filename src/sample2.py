import pyxel
import os
import sys
"""
さくらさくら
独自MMLフルカスタム版
"""

from pyhuremml import custom_mml_to_mml


msc = ""

def update():
    if pyxel.btn(pyxel.KEY_P) or pyxel.btn(pyxel.KEY_SPACE):
        # サウンドを再生 play(ch, snd, [tick], [loop], [resume])
        pyxel.play(0,0,loop=False)
    return

def draw():
    pyxel.cls(0)
    pyxel.text(10,10,"Press P to play.",7)
    
    pyxel.text(5, 50, "my mml:", pyxel.COLOR_WHITE)
    pyxel.text(15, 60, tmpmsc, pyxel.COLOR_WHITE)
    pyxel.text(5, 70, "original mml:", pyxel.COLOR_WHITE)
    pyxel.text(15, 80, msc, pyxel.COLOR_WHITE)
    return


# mmlメソッドでMMLを登録
tmpmsc = "t120 @0 o2 q7 v7 l4 "
tmpmsc += "a~a~si-~ aasi- asi^d_si asi/a/f-"
print("tmpmsc=" , tmpmsc)
msc = custom_mml_to_mml(tmpmsc)
print(msc)


pyxel.init(480, 240)
pyxel.mouse(True)
pyxel.sounds[0].mml(msc)
pyxel.run(update, draw)