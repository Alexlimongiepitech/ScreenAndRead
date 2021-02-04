import pytesseract
import pyautogui
import os
import sys

def firstStart():
    try:
        configFile = open("Config.txt", "x")
        configFile.close()
        os.mkdir("screenshot/")
    except OSError:
        pass
    

def config():
    """
        Functions for config the who start the picture and it's size
    """
    input("put where is the top-right and press enter")
    x, y = pyautogui.position()
    # print(x, y)
    input("put where is the bottom-left and press enter")
    rectx, recty = pyautogui.position()
    # print(rectx - x, recty - y)
    configFile = open("Config.txt", "w")
    configFile.write(str(x) + ", " + str(y) + ", " + str(rectx - x) + ", " + str(recty - y))
    screenRegion = (x, y, rectx - x, recty - y)
    return screenRegion

def getconfig():
    """    
        Functions for getting the Config.txt
    """
    configFile = open("Config.txt", "r")
    splited = configFile.read().split(', ')
    try:
        screenRegion = (splited[0], splited[1], splited[2], splited[3])
    except IndexError:
        screenRegion = config()
    return screenRegion
    

def main():
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe" # path for tesseract.exe
    # tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"' # path to tessdata, if you have an error on the language, uncomment this line
    cmd = ""
    screenNumber = 0
    screenRegion = ()
    path = ""
    name_of_your_project = ""
    
    try:
        firstStart()
        if (sys.argv[1] == "config"):
            screenRegion = config()
        elif (sys.argv[1] == "getconfig"):
            print(getconfig())
        else:
            name_of_your_project = sys.argv[1]
            path = "screenshot/" + name_of_your_project
            screenRegion = getconfig()
    except IndexError:
        name_of_your_project = input("give me the name of project :\n")
        path = "screenshot/" + name_of_your_project
        screenRegion = getconfig()

    try:
        os.mkdir(path)
    except OSError:
        pass
    else:
        print("Successfully created the directory")
        txt = open(path + "/save.txt", "x")
        txt.close()
    
    while (cmd != "exit"):
        cmd = input("press enter for screenshot -> ")
        if (cmd != "exit"):
            screenPath = str(path + "/screenshot_" + str(screenNumber) + ".png")
            while (os.path.exists(screenPath)):
                screenNumber = screenNumber + 1
                screenPath = str(path + "/screenshot_" + str(screenNumber) + ".png")
            screen = pyautogui.screenshot(screenPath, region=screenRegion) # comment if tessdata_dir_config is disable
            # screenText = pytesseract.image_to_string(screen, lang='eng', config=tessdata_dir_config) # un-comment if tessdata_dir_config is active
            screenText = pytesseract.image_to_string(screen, lang='eng')
            print(screenText)
            txt = open(path + "/save.txt", "a")
            txt.write("screenshot_" + str(screenNumber) + ".png\nstart:\n")
            txt.write(screenText)
            txt.write(":end\n")
            txt.close()
            
if __name__== "__main__":
   main()