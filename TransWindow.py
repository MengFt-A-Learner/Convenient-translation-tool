# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:51:29 2022

@author: MengFt
"""

from transTool import transTool
import PySimpleGUI as sg
from PIL import Image,ImageGrab
import time
#窗口布局
class transWindow(object):
    def __init__(self):
        print("创建一个翻译窗口，可进行汉译英和英译汉")    
        self.transLayoutVertical =[
            [sg.Button("百度翻译",key="BDtranslate"),
             sg.Button("清空翻译",key="clearTranslation"),
             sg.Button("转为纵向",key="turn2Horizontal"),
             sg.Radio('英译汉', "transTypeRadio", default=True, size=(10,1),key="E2C"),
             sg.Radio('汉译英', "transTypeRadio", default=True, size=(10,1), key='C2E'),],
            [sg.Text('原文',font='Times 10',size=(20,1)),sg.Text('译文',font='Times 10',size=(20,1)),],
            [sg.Multiline(size=(15,30),font='Times 16', expand_x=True, expand_y=True,key="textBeforeTranslate",enable_events=True),
             sg.Multiline(size=(15,30),font='Times 16', expand_x=True, expand_y=True,key="textAfterTranslate",enable_events=True),],
            ]
        
        self.transLayoutHorizontal =[
            [sg.Button("百度翻译",key="BDtranslate"),
             sg.Button("清空翻译",key="clearTranslation"),
             sg.Button("转为横向",key="turn2Vertical"),
             sg.Radio('英译汉', "transTypeRadio", default=True, size=(10,1),key="E2C"),
             sg.Radio('汉译英', "transTypeRadio", default=True, size=(10,1), key='C2E'),],
            [sg.Text('原文',font='Times 10',size=(20,1)),
             sg.Multiline(size=(15,30),font='Times 16', expand_x=True, expand_y=True,key="textBeforeTranslate",enable_events=True),],
            [sg.Text('译文',font='Times 10',size=(20,1)),
             sg.Multiline(size=(15,30),font='Times 16', expand_x=True, expand_y=True,key="textAfterTranslate",enable_events=True),],
            ]
        self.windowDirect=0    #0默认横向
        self.transType=0    #0默认英译汉
        self.BDTransTool=transTool()

    def getScreenSize(self):
        image = ImageGrab.grab()

        height=image.height
        width=image.width
        return (width,height)

    def currentTime(self):
        currentTime=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime( int(time.time())))
        return currentTime
    
    def getTransType(self):
        if self.window['E2C'].get()==True:
            self.transType=0
        elif self.window['C2E'].get()==True:
            self.transType=1
        return self.transType
        
        
    def windowInit(self):
        #选取窗口类型
        if self.windowDirect==0:
            #横向布置窗口
            #tempLayout=self.transLayoutVertical
            tempLayout=[
                [sg.Button("百度翻译",key="BDtranslate",font='Times 15'),
                 sg.Button("清空翻译",key="clearTranslation",font='Times 15'),
                 sg.Button("转为纵向",key="turn2Horizontal",font='Times 15'),
                 sg.Radio('英译汉', "transTypeRadio", default=True, size=(10,1),key="E2C",font='Times 15'),
                 sg.Radio('汉译英', "transTypeRadio", default=True, size=(10,1), key='C2E',font='Times 15'),],
                [sg.Text('原文',font='Times 15',size=(110,1)),sg.Text('译文',font='Times 15',size=(20,1)),],
                [sg.Multiline(size=(15,5),font='Times 16', expand_x=True, expand_y=True,key="textBeforeTranslate",enable_events=True),
                 sg.Multiline(size=(15,5),font='Times 16', expand_x=True, expand_y=True,key="textAfterTranslate",enable_events=True),],
                ]
            windowSize=self.getScreenSize()
            transWindowSize=(windowSize[0]-100,400)
            transWindowLocation=(0,windowSize[1]-transWindowSize[1]-50)        

        else:
            #tempLayout=self.transLayoutHorizontal
            tempLayout=[
                [sg.Button("百度翻译",key="BDtranslate",font='Times 15'),
                 sg.Button("清空翻译",key="clearTranslation",font='Times 15'),
                 sg.Button("转为横向",key="turn2Vertical",font='Times 15'),],
                 [sg.Radio('英译汉', "transTypeRadio", default=True, size=(10,1),key="E2C",font='Times 15'),
                 sg.Radio('汉译英', "transTypeRadio", default=True, size=(10,1), key='C2E',font='Times 15'),],
                [sg.Text('原文',font='Times 15',size=(4,1)),
                 sg.Multiline(size=(10,20),font='Times 16', expand_x=True, expand_y=True,key="textBeforeTranslate",enable_events=True),],
                [sg.Text('译文',font='Times 15',size=(4,1)),
                 sg.Multiline(size=(10,20),font='Times 16', expand_x=True, expand_y=True,key="textAfterTranslate",enable_events=True),],
                ]
            windowSize=self.getScreenSize()
            transWindowSize=(400,windowSize[1]-100)
            transWindowLocation=(windowSize[0]-transWindowSize[0]-50,0)        
        
        #tempLayout[-1].append(sg.Sizegrip())        

        self.window=sg.Window("翻译准确，写作顺畅！！",
                                    tempLayout,
                                    resizable=True, 
                                    grab_anywhere=True,
                                    keep_on_top=True,
                                    finalize=True, 
                                    location=(transWindowLocation),
                                    margins=(0,0), 
                                    )
        self.window.set_min_size(transWindowSize)

        #初始化后台翻译工具
        while True:
            event,values=self.window.read(timeout=1000)       
        
            if not event in (None,"__TIMEOUT__"):    
                print("当前时间为：{}，子窗口1激活事件{}".format(self.currentTime(),event))
            if event in (sg.WIN_CLOSED,'关闭'):
                self.window.close()
                break
            if event in ('BDtranslate'):
                print('开启翻译')
                stringBeforeTrans=self.window['textBeforeTranslate'].get()
                if stringBeforeTrans in ("",None):
                    print("无翻译内容")
                    sg.popup_auto_close("翻译内容为空",auto_close_duration=1,keep_on_top=True,font='Times 15')
                    continue
                else:
                    
                    self.BDTransTool.inputString(stringBeforeTrans,transType=self.getTransType(),deleteWrap=True)
                    stringAfterTrans=self.BDTransTool.getTrans()
                    stringBeforeTrans=self.BDTransTool.inputWords
                    self.window["textBeforeTranslate"].update(stringBeforeTrans)
                    self.window["textAfterTranslate"].update(stringAfterTrans)
                    
            if event in ('clearTranslation'):
                print('清空翻译')
                self.window["textBeforeTranslate"].update("")
                self.window["textAfterTranslate"].update("")

            if event in ('turn2Horizontal'):
                self.windowDirect=1
                print('转为纵向')
                self.window.close()
                self.windowInit()
            if event in ('turn2Vertical'):
                self.windowDirect=0
                print('转为纵向')
                self.window.close()
                self.windowInit()

            #如果关闭子窗口，自动重新打开主窗口                

#页面操作

if __name__ == "__main__":
    window1=transWindow()
    window1.windowInit()

    













