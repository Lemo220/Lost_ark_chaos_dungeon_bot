import pyautogui
from screen_search import *
from mss import mss
from PIL import Image
spells = ["a", "d", "f", "w", "q", "e"]

spells_region = (616,977,891,1070)

def findImageOnScreen(image_path):  
        x = pyautogui.locateOnScreen(image_path, region = spells_region, confidence = 0.9)
        if x == None:
            return False
        else:
            return True

def check_avalible_spells():  # check region what spells are available
    avalible_spells = []
    for spell in spells:
        if findImageOnScreen(('images\\' + spell + ".png")) == True:
            avalible_spells.append(spell)
    return avalible_spells