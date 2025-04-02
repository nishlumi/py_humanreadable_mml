# title: py_HumanReadableMML Play tool
# author: lumis(lumidina)
# desc: custom MML to True MML convert tool
# license: MIT
# version: 1.0

import pyxel
from mycls import GUIText, GUIButton, GUIRect, GUICheckbox, GUIDialog
import os
import sys
import yaml
import glob


from pyhuremml import custom_mml_to_mml, midcustom_mml_to_mml


class App:
    def __init__(self):
        pyxel.init(320, 300, title="py_HumanReadableMML Play tool",display_scale=3)
        pyxel.mouse(True)

        self.inputdir = "./input/*.yaml"
        self.inputfilespath = []
        self.inputindex = -1
        self.mmlpath = "./mmltext.yaml"
        self.savetextdir = "./output/text"
        self.savewavdir = "./output/wav"
        self.savetextpath = ""
        self.savewavpath = ""
        self.savepath = "./outtext.txt"
        
        self.mmlformat = "f" # f - hureMML(full custom), hureMML(middle custom), o - original MML
        self.rawdata = ["","","",""]
        self.mmldata = ["","","",""]
        self.ui = {
            "btn_loaddir"    : GUIButton("Input Dir",8,8,4*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "lab_fmttitle": GUIText("fmt:", 8*7, 8,color1=pyxel.COLOR_WHITE),
            "btn_fmtf"    :  GUICheckbox("F",8*9,8,True,color1=pyxel.COLOR_WHITE),
            "btn_fmtm"    :  GUICheckbox("M",8*11.5,8,False,color1=pyxel.COLOR_WHITE),
            "btn_fmto"    :  GUICheckbox("O",8*14,8,False,color1=pyxel.COLOR_WHITE),
            "label1"      : GUIText("File:", 8*17, 8,color1=pyxel.COLOR_WHITE),
            "btn_loadprev"  : GUIButton("<" ,8*20,8,2*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "btn_loadnext"  : GUIButton(">" ,8*21.5,8,2*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "btn_load"    : GUIButton("Load",8*23,8,4*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "label1_b" : GUIText(":yaml", 8*26, 8,color1=pyxel.COLOR_WHITE),
            
            "btn_play"    : GUIButton("Play",8*33,8*4,4*8,8*2,bgcolor=pyxel.COLOR_DARK_BLUE,fontcolor=pyxel.COLOR_WHITE),
            "btn_stop"    : GUIButton("Stop",8*36,8*4,4*8,8*2,bgcolor=pyxel.COLOR_RED,fontcolor=pyxel.COLOR_WHITE),
            #---
            "btn_save"    : GUIButton("Save",8,8*2.5,4*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "label2" : GUIText("./output/text/*.txt", 8*4, 8*2.5,color1=pyxel.COLOR_WHITE),
            #---
            "btn_savewav" : GUIButton("Wav" ,8,8*4,4*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "lab_reptitle": GUIText("Repeat:", 8*4, 8*4,color1=pyxel.COLOR_WHITE),
            "btn_repmin"  : GUIButton("-" ,8*8,8*4,2*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "txt_repcnt"  : GUIText(  " 1", 8*9.5,8*4,color1=pyxel.COLOR_WHITE),
            "btn_repmax"  : GUIButton("+" ,8*11,8*4,2*8,8,fontcolor=pyxel.COLOR_WHITE,bgcolor=pyxel.COLOR_GREEN),
            "label3" : GUIText("./output/wav/*.wav", 8*13, 8*4,color1=pyxel.COLOR_WHITE),
            #---
            "btn_rawmml" :  GUICheckbox("Raw",8,8*6,True,color1=pyxel.COLOR_WHITE),
            "btn_truemml" : GUICheckbox("Converted",8*5,8*6,False,color1=pyxel.COLOR_WHITE),
            "btn_playloop" :  GUICheckbox("Loop",8*33,8*6.5,False,color1=pyxel.COLOR_WHITE),
            #"label2" : GUIText("c d e f g a b --> d r m f s a si", 8, 8*2,color1=pyxel.COLOR_WHITE),
            
            #---
            "line1"       : GUIRect(   8,8*8,pyxel.width-16,4,pyxel.COLOR_BROWN),
            "ch1"         : GUIText("C1",8,8*7.5,color1=pyxel.COLOR_WHITE),
            "btn_mute1"   : GUICheckbox("Mute",8*3,8*7.5,False,color1=pyxel.COLOR_WHITE),
            "rect_1"      : GUIRect(8,8*8.5, pyxel.width-16,8*5.5,pyxel.COLOR_GRAY,filled=False),
            "txt_output1" : GUIText("",8,8*9,color1=pyxel.COLOR_WHITE),
            
            "line2"       : GUIRect(   8,8*15,320-16,4,pyxel.COLOR_BROWN),
            "ch2"         : GUIText("C2",8,8*14.5,color1=pyxel.COLOR_WHITE),
            "btn_mute2"   : GUICheckbox("Mute",8*3,8*14.5,False,color1=pyxel.COLOR_WHITE),
            "rect_2"      : GUIRect(8,8*15.5, pyxel.width-16,8*5.5,pyxel.COLOR_GRAY,filled=False),
            "txt_output2" : GUIText("",8,8*16,color1=pyxel.COLOR_WHITE),
            
            "line3"       : GUIRect(   8,8*22,320-16,4,pyxel.COLOR_BROWN),
            "ch3"         : GUIText("C3",8,8*21.5,color1=pyxel.COLOR_WHITE),
            "btn_mute3"   : GUICheckbox("Mute",8*3,8*21.5,False,color1=pyxel.COLOR_WHITE),
            "rect_3"      : GUIRect(8,8*22.5, pyxel.width-16,8*5.5,pyxel.COLOR_GRAY,filled=False),
            "txt_output3" : GUIText("",8,8*23,color1=pyxel.COLOR_WHITE),
            
            "line4"       : GUIRect(   8,8*29,320-16,4,pyxel.COLOR_BROWN),
            "ch4"         : GUIText("C4",8,8*28.5,color1=pyxel.COLOR_WHITE),
            "btn_mute4"   : GUICheckbox("Mute",8*3,8*28.5,False,color1=pyxel.COLOR_WHITE),
            "rect_4"      : GUIRect(8,8*29.5, pyxel.width-16,8*5.5,pyxel.COLOR_GRAY,filled=False),
            "txt_output4" : GUIText("",8,8*30,color1=pyxel.COLOR_WHITE),
            
            "line_end"       : GUIRect(   8,8*37,320-16,4,pyxel.COLOR_NAVY),
        }
        self.dlg = GUIDialog(pyxel.width//4,pyxel.height//3,pyxel.width//2,pyxel.height//4)
        self.dlg.dialog_color = pyxel.COLOR_GREEN
        self.dlg.add_contents(GUIText("this !",0,4,color1=pyxel.COLOR_BLACK))
        self.dlg.contents[0].refresh_text(self.dlg.bounds.w)
        
        self.load_dir()
        #self.load_mml()
        
        pyxel.run(self.update, self.draw)    
    
    def set_dlgmessage(self, text):
        self.dlg.contents[0].set_text(text)
        self.dlg.contents[0].refresh_text(self.dlg.bounds.w)
        
    def load_dir(self):
        self.inputfilespath.clear()
        self.inputindex = -1
        glst = glob.glob(self.inputdir)
        for gl in glst:
            #print(os.path.basename(gl), os.path.splitext(os.path.basename(gl)) )
            if os.path.exists(gl):
                self.inputfilespath.append(gl)
        if len(self.inputfilespath) > 0:
            self.inputindex = 0
            self.change_inputpath(0)
        else:
            self.mmlpath = ""
    
    def change_inputpath(self,nextval: int):
        self.inputindex += nextval
        self.inputindex = max(self.inputindex, 0)
        self.inputindex = min(self.inputindex, len(self.inputfilespath)-1)
        self.mmlpath = self.inputfilespath[self.inputindex]
        self.ui["label1_b"].set_text(os.path.basename(self.mmlpath))
        self.ui["label1_b"].refresh_text(pyxel.width)
        
        self.savetextpath = os.path.splitext(os.path.basename(self.mmlpath))[0] + ".txt"
        self.savewavpath = os.path.splitext(os.path.basename(self.mmlpath))[0] + ".wav"
        self.ui["label2"].set_text(f"{self.savetextdir}/{self.savetextpath}")
        self.ui["label2"].refresh_text(pyxel.width)
        self.ui["label3"].set_text(f"{self.savewavdir}/{self.savewavpath}")
        self.ui["label3"].refresh_text(pyxel.width)
        
        self.load_mml()
        
    def change_fmt_check(self, b):
        for u in ["btn_fmtf","btn_fmtm","btn_fmto"]:
            self.ui[u].checked = False
        self.ui[b].checked = True
        if self.ui[b].checked:
            self.mmlformat = b.replace("btn_fmt","")
                
    def load_mml(self):
        def findlist(lst, f):
            for i,m in enumerate(lst):
                if m == f:
                    return i
                    
        chan = ["c1","c2","c3","c4"]
        if (not os.path.exists(self.mmlpath)) or (len(self.inputfilespath) == 0):
            self.dlg.open()
            return
        
        yfile = yaml.safe_load(open(self.mmlpath, encoding="utf-8"))
        for i in range(4):
            pyxel.sounds[i] = pyxel.Sound()
            self.rawdata[i] = ""
            self.mmldata[i] = ""
            self.show_mml(i, "")
        try:
            if "mml" in yfile:
                for m in yfile["mml"]:
                    
                    if m.lower() == "format":
                        self.change_fmt_check(f"btn_fmt{yfile['mml'][m]}")
                    
                    elif m in chan:                        
                        inx = chan.index(m)
                        if inx > -1:
                            self.rawdata[inx] = " ".join(yfile["mml"][m])
                            self.show_mml(inx, self.rawdata[inx])
                            if self.mmlformat == "f":
                                self.mmldata[inx] = custom_mml_to_mml(self.rawdata[inx])
                            elif self.mmlformat == "m":
                                self.mmldata[inx] = midcustom_mml_to_mml(self.rawdata[inx])
                            elif self.mmlformat == "o":
                                self.mmldata[inx] = self.rawdata[inx]
                            pyxel.sounds[inx].mml(self.mmldata[inx])
                            pyxel.musics[0].set([0],[1],[2],[3])
        except Exception as e:
            print("***error***")
            print(":",e)
            pyxel.sounds[inx] = pyxel.Sound()
            
    
    def save_mml(self):
        with open(f"{self.savetextdir}/{self.savetextpath}","w",encoding="utf-8") as f:
            f.write("\n".join(self.mmldata))
    
    def show_mml(self, index, text):
        self.ui[f"txt_output{index+1}"].set_text(text)
        self.ui[f"txt_output{index+1}"].refresh_text(320-16)
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
                
        for u in self.ui:
            self.ui[u].update()
            
        self.dlg.update()
        if self.dlg.is_open():
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.dlg.close()
            dlgret = self.dlg.check_pressed()
            if dlgret["OK"]:
                print("pressed!")
                self.dlg.close()
            return
        
        #---load related
        if self.ui["btn_loaddir"].pressed or pyxel.btnp(pyxel.KEY_D):
            self.load_dir()
            self.ui["btn_loaddir"].pressed = False
            
        if self.ui["btn_load"].pressed or pyxel.btnp(pyxel.KEY_L):
            self.load_mml()
            self.ui["btn_load"].pressed = False
        
        if self.ui["btn_loadprev"].pressed  or pyxel.btnp(pyxel.KEY_LEFT):
            if len(self.inputfilespath) > 0:
                self.change_inputpath(-1)
            self.ui["btn_loadprev"].pressed = False
                
        if self.ui["btn_loadnext"].pressed  or pyxel.btnp(pyxel.KEY_RIGHT):
            if len(self.inputfilespath) > 0:
                self.change_inputpath(1)
            self.ui["btn_loadnext"].pressed = False
            
        if self.ui["btn_save"].pressed or pyxel.btnp(pyxel.KEY_V):
            self.save_mml()
            self.ui["btn_save"].pressed = False
            
        if self.ui["btn_savewav"].pressed or pyxel.btnp(pyxel.KEY_W):
            pyxel.musics[0].save(f"{self.savewavdir}/{self.savewavpath}",int(self.ui["txt_repcnt"].text))
            self.ui["btn_savewav"].pressed = False
            

            
        if self.ui["btn_play"].pressed  or pyxel.btnp(pyxel.KEY_P) or pyxel.btn(pyxel.KEY_SPACE):
            if not self.ui["btn_mute1"].checked:
                pyxel.play(0,0,loop=self.ui["btn_playloop"].checked)
            if not self.ui["btn_mute2"].checked:
                pyxel.play(1,1,loop=self.ui["btn_playloop"].checked)
            if not self.ui["btn_mute3"].checked:
                pyxel.play(2,2,loop=self.ui["btn_playloop"].checked)
            if not self.ui["btn_mute4"].checked:
                pyxel.play(3,3,loop=self.ui["btn_playloop"].checked)
            self.ui["btn_play"].pressed = False
        
        if self.ui["btn_stop"].pressed or pyxel.btnp(pyxel.KEY_S):
            for i in range(4):
                pyxel.stop(i)
            self.ui["btn_stop"].pressed = False
            
        #---
        if pyxel.btnp(pyxel.KEY_1):
            self.ui["btn_mute1"].checked = not self.ui["btn_mute1"].checked
        if pyxel.btnp(pyxel.KEY_2):
            self.ui["btn_mute2"].checked = not self.ui["btn_mute2"].checked
        if pyxel.btnp(pyxel.KEY_3):
            self.ui["btn_mute3"].checked = not self.ui["btn_mute3"].checked
        if pyxel.btnp(pyxel.KEY_4):
            self.ui["btn_mute4"].checked = not self.ui["btn_mute4"].checked
        
        if self.ui["btn_rawmml"].pressed:
            self.ui["btn_rawmml"].checked = True
            if self.ui["btn_rawmml"].checked:
                for i,m in enumerate(self.rawdata):
                    self.show_mml(i,m)                
                self.ui["btn_truemml"].checked = False
                
            self.ui["btn_rawmml"].pressed = False
        
        #---format buttons
        for b in ["btn_fmtf","btn_fmtm","btn_fmto"]:
            if self.ui[b].pressed:
                self.change_fmt_check(b)
                
                self.ui[b].pressed = False
                
        if self.ui["btn_truemml"].pressed:
            self.ui["btn_truemml"].checked = True
            if self.ui["btn_truemml"].checked:
                for i,m in enumerate(self.mmldata):
                    self.show_mml(i,m)
                self.ui["btn_rawmml"].checked = False
            
            self.ui["btn_truemml"].pressed = False
        
        #---repeat count
        if self.ui["btn_repmin"].pressed:
            inp = max(int(self.ui["txt_repcnt"].text) - 1, 1)
            self.ui["txt_repcnt"].set_text(f"{inp:>2}")
            self.ui["btn_repmin"].pressed = False
        if self.ui["btn_repmax"].pressed:
            inp = min(int(self.ui["txt_repcnt"].text) + 1, 10)
            self.ui["txt_repcnt"].set_text(f"{inp:>2}")
            self.ui["btn_repmax"].pressed = False
            
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for u in self.ui:
            self.ui[u].draw()
        
        self.dlg.draw()

App()