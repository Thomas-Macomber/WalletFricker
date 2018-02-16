import os
from LogTest import *

currentMenu = 0
previousMenu = 0

currentMenus = []
menus = ["Main Menu", "Help Menu", "Menu 3", "Menu 4"]
menusMain = ["Help", "Menu 3", "Menu 4", "Exit"]
menusHelp = ["HelpItem 1", "HelpItem 2", "Etc"]
menusMenu3 = ["SubMenu3a","SubMenu3b"]
menusMenu4 = ["SubMenu4a"]

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
        for i in range(0, len(menusMenu3[])):
            print ( menusMenu3[i] )
    elif menu == 3:
        for i in range(0, len(menusMenu4[])):
            print ( menusMenu4[i] )
