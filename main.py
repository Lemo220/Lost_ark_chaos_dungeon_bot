import pyautogui, time, random, cv2, math, keyboard, os, pygetwindow as gw, numpy as np
from PIL import Image
from random import randint
from config import spells_regions
import mss
from threading import Thread
pyautogui.FAILSAFE = False


class Lost_bot():

    # propeties
    IN_CITY = True
    IN_CHAOS = True
    MOVE = False
    CAST = False
    BOT_WORKING = False
    TOO_FAR = False
    available_spells = []
    Lost_ark = gw.getWindowsWithTitle('Lost Ark')[0]
    method = cv2.TM_CCORR_NORMED
    z = 0
    global regions
    regions =   {"region_results" : (238,119,1873,926), 
                "region_check_in_fight" : (245,0,563,116),
                "region_check_accept" : (700,410,1260,700),
                "region_check_ok" : (570,725,1400,1065),
                "region_minimap" : (1593,40,1889,295),
                }
    minimap_path = 'images\\minimap.png'
    target_path = 'images\\enemy.png'
    mini_boss_path = "boss2.png"
    final_boss_path = "final_boss2.png"
    enemy_path = "enemy.png"
    portal_path = "portal2.png"



    def waitRandomizedTime(self, min, max):
        time.sleep(random.uniform(min, max))

    # load config
    text_file = open("config.txt", "r") ## load config files
    lines = text_file.read().split('\n')
    for row in lines:
        if "spells" in row:
            all_spells = row.replace("spells =","").replace(" ","")
        if "spell/time" in row:
            duration = row[15:].split(" ")
        if "song of escape" in row:
            song_of_escape = row[-1:]
    # set window
    Lost_ark.activate()
    Lost_ark.resizeTo(1920,1080)
    Lost_ark.moveTo(0,0)


    def check_available_spell(self, all_spells):  # check region what spells are available
        self.available_spells = []
        for spell in all_spells:
            with mss.mss() as sct:
                x = sct.grab((spells_regions[0][spell]))
                img = list(Image.Image.getdata(Image.frombytes("RGB", x.size, x.bgra, "raw", "BGRX")))
                if img == list(Image.Image.getdata(Image.open("images\\" + str(spell) + ".png"))):
                    self.available_spells.append(spell)
        print("available spells", self.available_spells)
        return self.available_spells

    def find_pos(self, minimap_path, target, method, game_window):
        with mss.mss() as sct:
                    x = sct.grab(regions["region_minimap"])
                    img = Image.frombytes("RGB", x.size, x.bgra, "raw", "BGRX")  # Convert to PIL.Image
                    img.save(minimap_path, 'PNG')
        map = cv2.imread(minimap_path)
        map2 = cv2.imread(minimap_path, cv2.IMREAD_GRAYSCALE)
        
        ## clear a little our minimap to avoid some wrong matches
        thresh = cv2.threshold(map2,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = np.ones((12,12),np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        
        ## use our mask to minimap
        res = cv2.bitwise_and(map,map,mask = closing)
        friend = cv2.imread(target)

        ## resize to get vector
        map = cv2.resize(res, None, fx = 4, fy = 3)
        result = cv2.matchTemplate(map, friend, method)
        _,max_val,_, max_loc = cv2.minMaxLoc(result)
        _,map_w,map_h = map.shape[::-1]
        _,friend_w,friend_h = friend.shape[::-1]
        ## count distance how far we have to move our screenshot to place it on middle of screen
        distance_x = (game_window.size[0] - map_w) / 2
        distance_y = (game_window.size[1] - map_h) / 2
        

        ## count where is my character and friend character to get distance between them. If it is too big, just run to friend, dont cast spells. Also multiply 
        ## values to get further posx posy
        friend_position = (max_loc[0] + distance_x, max_loc[1] + distance_y)
        multiplier = 1
        friend_position_on_minimap = (max_loc[0] + (friend_w / 2),max_loc[1] + (friend_h / 2))
        my_position_on_minimap = (int((map_w / 2)), int((map_h) / 2))
        dist = math.dist(my_position_on_minimap,friend_position_on_minimap)
        if dist > 150:
            self.TOO_FAR = True
        else:
            self.TOO_FAR = False
        if dist < 180:
            multiplier = 1.2
        if friend_position[0] < (game_window.size[0] / 2):
            posx = friend_position[0] * (2 - multiplier)
        else:
            posx = friend_position[0] * multiplier
        if friend_position[1] < (game_window.size[1] / 2):
            posy = friend_position[1] * (2 - multiplier)
        else:
            posy = friend_position[1] * multiplier
        if max_val > 0.86:
            return True, posx, posy
        else:
            return False, 0, 0
        
    def move_to_someone(self, posx, posy):
        pyautogui.moveTo((posx,posy))
        pyautogui.click(button= "SECONDARY", clicks = randint(1,3), interval = random.uniform(0.1,0.3))

    def fight(self, target): ## start thread with moving to someone
        while not self.IN_CITY:
            pos = self.find_pos(self.minimap_path, target, self.method, self.Lost_ark)
            if pos[0] == True:
                self.move_to_someone(pos[1], pos[2])


    def cast_spell(self, spells):  ##check spells and cast first avalible
        hold_time = 0.2
        if self.TOO_FAR != True:
            if self.available_spells == []:
                self.available_spells = self.check_available_spell(spells)
                for _ in range(0,10):
                    pyautogui.click()
                    self.waitRandomizedTime(0.2,0.3)
            elif self.available_spells != []:
                cast = self.available_spells[randint(0,len(self.available_spells)-1)]
                for i in self.duration:
                    if cast in i:
                        hold_time = int(i.replace(cast, ""))
                pyautogui.keyDown(cast)
                self.waitRandomizedTime(hold_time*0.8,hold_time)
                pyautogui.keyUp(cast)
                self.available_spells.remove(cast)


        self.CAST = False

    def exit(self, region_result,region_check_if_ok, song_of_escape): ## exit from dungeon if finish
        if pyautogui.locateOnScreen('images\\results.png', confidence = 0.8, region = region_result) != None:
            while True:
                time.sleep(randint(2,3))
                pyautogui.press(song_of_escape)
                time.sleep(randint(8,10))
                if pyautogui.locateOnScreen("images\\ok2.png", confidence = 0.9, region = region_check_if_ok) == None:
                    self.MOVE = False
                    break
            return True
        else:
            return False
            
    def check_res(self): ## check if character is dead
        if pyautogui.locateOnScreen("images\\base_res.png", confidence = 0.99) != None:
            try:
                res_cords = pyautogui.locateOnScreen("images\\base_res.png", confidence = 0.99)
                pyautogui.moveTo(res_cords[0],res_cords[1])
                self.waitRandomizedTime(1,2)
                pyautogui.click()
            except:
                pass

    def check_in_fight(self, region_check_in_fight):  ##check if character is in city
        if pyautogui.locateOnScreen("images\\check_in_fight.png", confidence = 0.8, region = region_check_in_fight) != None:
            self.MOVE = False
            return False
        else:
            return True

    def click_accept(self, region_check_accept):
        click_accept = pyautogui.locateOnScreen("images\\ccept.jpg", confidence = 0.8, region = region_check_accept)
        pyautogui.moveTo(click_accept[0] + randint(2,10), click_accept[1] + randint(2,10))
        pyautogui.click()

    ## search for chaos dungeon when in city
    def search_chaos(self):
        while self.IN_CITY == True:
            print("in city: ", self.IN_CITY)
            self.z = 0
            if self.IN_CITY == True:
                self.IN_CITY = self.check_in_fight(regions["region_check_in_fight"])

            if self.IN_CITY == True:
                pyautogui.press('g')
                self.waitRandomizedTime(1,2)
                click_matchmaking = pyautogui.locateOnScreen("images\\matchmaking.png")
                try:
                    pyautogui.moveTo(click_matchmaking[0] + randint(30,100), click_matchmaking[1] + randint(3,40))
                    pyautogui.click()
                except:
                    pass
                self.waitRandomizedTime(2,3)
                try:
                    self.click_accept(regions["region_check_accept"])
                except:
                    pass
        return False

    ## do chaos dungeon after finding one
    def do_chaos(self):
        while self.IN_CITY == False:  
            if self.z == 0: # turn on buff at start every dungeon - only for berserker mayhem i guess
                pyautogui.press("z")
                self.z += 1
            if not self.MOVE:
                self.MOVE = True
                start_moving = Thread(target = self.fight, args = (self.target_path,))
                start_moving.start()
            self.cast_spell(self.all_spells)
            self.check_res()
            self.IN_CITY = self.exit(regions["region_results"], regions["region_check_ok"],  self.song_of_escape)
            if pyautogui.locateOnScreen("images\\ccept.jpg", confidence = 0.95, region = regions["region_check_accept"]) != None:
                
                self.click_accept(regions["region_check_accept"])

def kill_bot():
    while True:
        if keyboard.is_pressed("Esc"):
            os._exit(1)
        time.sleep(1)
Esc = True
if __name__ == "__main__":
    while True:
        bot = Lost_bot()
        if Esc:
            Thread(target = kill_bot, args = ()).start()
            Esc = False
        bot.search_chaos()
        bot.do_chaos()
        
