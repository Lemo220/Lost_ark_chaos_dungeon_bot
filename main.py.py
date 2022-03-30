import pyautogui
import time
import random
import cv2
from PIL import Image
from random import randint
from spells import check_avalible_spells
pyautogui.FAILSAFE = False
import pygetwindow as gw
from mss import mss


method = cv2.TM_SQDIFF
in_city = True
region_exit = (238,119,1873,926)
region_check_in_fight = (245,0,563,116)
region_check_res = (1050,0,1920,1080)
region_check_accept = (700,410,1260,700)

Lost_ark = gw.getWindowsWithTitle('Lost Ark') # focus on lost ark window
Lost_ark[0].activate()

def waitRandomizedTime(min, max):
    time.sleep(random.uniform(min, max))

def whirlwind(): ## special spell which has to be pushed
    print("krece sie")
    waitRandomizedTime(0.1,0.2)
    pyautogui.keyDown('d')
    move_to_someone(0)
    waitRandomizedTime(2,3)
    pyautogui.keyUp('d')



def move_to_someone(i): ## follow teammate found on minimap
    try:
        method = cv2.TM_SQDIFF
        path= 'images\\minimap.png'
        my_position = (150, 128)
        with mss() as sct:
            x = sct.grab((1593,40,1889,295))
            img = Image.frombytes("RGB", x.size, x.bgra, "raw", "BGRX")  # Convert to PIL.Image
            img.save('images\\minimap.png', 'PNG')
        friend = cv2.imread('images\\pixel.png')
        minimap = cv2.imread(path)
        result = cv2.matchTemplate(friend, minimap, method)
        friend_position = cv2.minMaxLoc(result)[2]
        print(my_position, "- my position")
        print(friend_position, "- friend position")

        x1 = 963 / my_position[0]
        y1 = 551 / my_position[1]
        
        x2 = x1 * friend_position[0]
        y2 = y1 * friend_position[1]
        if x2 <= 963:
            x2 = x2 * 0.7
        else:
            x2 = x2 * 1.3
        if y2 <= 551:
            y2 = y2 * 0.7
        else:
            y2 = y2 * 1.3
        while i < 1:
            pyautogui.moveTo(int(x2), int(y2))
            pyautogui.click(button = "SECONDARY")
            time.sleep(random.uniform(0.1, 0.25))
            i += 1
    except:
        pass

def cast_spell():  ##check spells and cast first avalible
    try:
        global spells
        if spells == []:
            spells = check_avalible_spells()
            
        print(spells)
        if spells != []:
            cast = spells[randint(0,len(spells)-1)]
            if cast == "d":
                whirlwind()
            else: 
                pyautogui.keyDown(cast)
                waitRandomizedTime(0.1,0.2)
                pyautogui.keyUp(cast)
            spells.remove(cast)
        else:
            for _ in range(0,10):
                pyautogui.click()
                waitRandomizedTime(0.2,0.3)
    except:
        pass




def exit(): ## exit from dungeon if finish
    if pyautogui.locateOnScreen('images\\results.png', confidence = 0.8, region = region_exit) != None:
        time.sleep(randint(2,3))
        pyautogui.press("8")
        time.sleep(randint(8,10))

        in_city == True
        return True
    else:
        return False
        
def check_res(): ## check if character is dead
    if pyautogui.locateOnScreen("images\\base_res.png", confidence = 0.8) != None:
        res_cords = pyautogui.locateOnScreen("images\\base_res.png", confidence = 0.8)
        pyautogui.moveTo(res_cords[0],res_cords[1])
        waitRandomizedTime(1,2)
        pyautogui.click()

def check_in_fight():  ##check if character is in city
    if pyautogui.locateOnScreen("images\\check_in_fight.png", confidence = 0.8, region = region_check_in_fight) != None:
        return False
    else:
        return True


while True:
    print("start")
    print("in city: ", in_city)
    z = 0
    if in_city == True:
        in_city = check_in_fight()
    spells = []

    if in_city == True:
        pyautogui.press('g')
        waitRandomizedTime(1,4)
        click_matchmaking = pyautogui.locateOnScreen("images\\matchmaking.png")
        try:
            pyautogui.moveTo(click_matchmaking[0] + randint(30,100), click_matchmaking[1] + randint(3,40))
            pyautogui.click()
        except:
            pass
        waitRandomizedTime(2,3)
        try:
            click_accept = pyautogui.locateOnScreen("images\\ccept.jpg", confidence = 0.8)
            pyautogui.moveTo(click_accept[0] + randint(2,10), click_accept[1] + randint(2,10))
            pyautogui.click()
        except:
            pass
    while in_city == False:
        if z == 0: # turn on buff at start every dungeon
            pyautogui.press("z")
            z += 1
        check_res()
        move_to_someone(0)
        cast_spell()
        move_to_someone(0)
        waitRandomizedTime(0.3,0.5)
        in_city = exit()
        if pyautogui.locateOnScreen("images\\ccept.jpg", confidence = 0.95, region = region_check_accept) != None:
            cords = pyautogui.locateOnScreen("images\\ccept.jpg", confidence = 0.95, region = region_check_accept)
            pyautogui.moveTo(cords[0] + randint(0,10), cords[1] + randint(0,10))
            waitRandomizedTime(1,2)
            pyautogui.click()