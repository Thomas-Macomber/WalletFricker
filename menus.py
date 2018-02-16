import os
from LogTest import *

currentMenu = 0
previousMenu = 0

currentMenus = []
menus = ["Main Menu", "Help Menu", "Curriency Log"]
menusMain = ["Help", "Log"]
menusHelp = ["Log"]

def printMenu( menu ):
    os.system('cls')
    header()
    print( menus[menu] )
    if menu == 0:
        for i in range(0, len(menusMain[])):
            print ( menusMain[i] )
    elif menu == 1:
        for i in range(0, len(menusHelp[])):
            print ( menusHelp[i] )
    elif menu == 2:
        startBot()        
