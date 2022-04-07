import pyautogui, time, random, cv2, math, keyboard, os, numpy as np
from random import randint
from threading import Thread
from window_capture import WindowCapture
pyautogui.FAILSAFE = False
from config import configure_config

class Lost_bot():

    # propeties
    wincapture = WindowCapture("LOST ARK (64-bit, DX11) v.2.1.1.4")
    translate_pos = wincapture.get_screen_position
    global screenshot
    screenshot = wincapture.get_screenshot()
    IN_CITY = True
    MOVE = False
    CAST = False
    BOT_WORKING = False
    available_spells = []
    window_size = (wincapture.w, wincapture.h)
    print(wincapture)
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
    target_path = 'images\\pixel.png'
    # mini_boss_path = "boss2.png"
    # final_boss_path = "final_boss2.png"
    # enemy_path = "enemy.png"
    # portal_path = "portal2.png"
    spell_check = "images\\spell_check.png"
    result_path = "images\\result.png"
    matchmaking_path = "images\\matchmaking.png"
    ok2_button_path = "images\\ok.png"
    resurection_path = "images\\base_res.png"
    check_in_fight_path = "images\\check_in_fight.jpg"
    accept_path = "images\\ccept.jpg"



    def waitRandomizedTime(self, min, max):
        time.sleep(random.uniform(min, max))

    # load config
    text_file = open("config.txt", "r") ## load config files
    lines = text_file.read().split('\n')
    for row in lines:
        if "spells" in row:
            all_spells = row.replace("spells =","").replace(" ","")
        elif "spell/time" in row:
            duration = row[15:].split(" ")
        elif "song of escape" in row:
            song_of_escape = row[-1:]
        elif "repair" in row:
            repair = row.replace("repair:","").replace(" ","").lower()
    def focus_game_window(self):
        self.Lost_ark.minimize()
        self.Lost_ark.restore()
        self.Lost_ark.resizeTo(1920,1080)
        self.Lost_ark.moveTo(0,0)

    def check_available_spell(self, all_spells):  # check region what spells are available
        self.available_spells = []
        for spell in all_spells:
            path = ("images\\" + str(spell) + ".png")
            result = self.find_pos(path, 0.98, cv2.TM_CCORR_NORMED)
            if result != False:
                self.available_spells.append(spell)
        print("available spells: ", self.available_spells)
        return self.available_spells

    def find_pos(self, what_find_path, threshold, method):
        find_this = cv2.imread(what_find_path, cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(screenshot, find_this, method)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
        print(maxVal, what_find_path)
        if maxVal > threshold:
            return self.wincapture.get_screen_position(maxLoc)
        else:
            return False

    ## repair items if possible
    def repair_items(self):
        cropped_screen = screenshot[0:107,1430:1520]
        mask = cv2.imread("images\\mask.png", cv2.IMREAD_GRAYSCALE)
        mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        equipment = cv2.imread("images\\equipment.png", cv2.IMREAD_UNCHANGED)
        mask_x = cv2.bitwise_and(cropped_screen,cropped_screen,mask = mask)
        mask_y = cv2.bitwise_and(equipment,equipment,mask = mask)
        result = cv2.matchTemplate(mask_x , mask_y, self.method)
        _,max_val,_,_ = cv2.minMaxLoc(result)
        if max_val > 0.93:
            print("Repair start")
            pyautogui.hotkey("alt", "p")
            self.waitRandomizedTime(1,2)
            pos_repair = self.find_pos("images\\repair.png",0.98,self.method)
            pyautogui.moveTo(pos_repair[0] + randint(3,6), pos_repair[1] + randint(3,6))
            pyautogui.click()
            self.waitRandomizedTime(1,2)
            pos_repair = self.find_pos("images\\repair_button.png",0.98,self.method)
            pyautogui.moveTo(pos_repair[0] + randint(3,6), pos_repair[1] + randint(3,6))
            pyautogui.click()
            self.waitRandomizedTime(1,2)
            pyautogui.press("esc", 2, 2)

        ## first take screen of minimap and try to clear it, after that find target, calculate and follow him
    def find_pos_and_walk(self, minimap_path, target, method, game_window):
        im = screenshot
        cropped_image = im[40:295, 1593:1889]
        cv2.imwrite(minimap_path, cropped_image)
        im = cropped_image
        im_gray = cv2.imread(minimap_path, cv2.IMREAD_GRAYSCALE)

        ## clear a little our minimap to avoid some wrong matches
        thresh = cv2.threshold(im_gray,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = np.ones((12,12),np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        
        ## use our mask to minimap
        res = cv2.bitwise_and(im,im,mask = closing)
        friend = cv2.imread(target)

        ## resize to get vector
        im = cv2.resize(res, None, fx = 4, fy = 3)
        result = cv2.matchTemplate(im, friend, method)
        _,max_val,_, max_loc = cv2.minMaxLoc(result)
        _,map_w,map_h = im.shape[::-1]
        _,friend_w,friend_h = friend.shape[::-1]

        ## count distance how far we have to move our screenshot to place it on middle of screen
        distance_x = (game_window[0] - map_w) / 2
        distance_y = (game_window[1] - map_h) / 2
        
        ## count where is my character and friend character to get distance between them. If it is too big, just run to friend, dont cast spells. Also multiply 
        ## values to get further posx posy
        friend_position = (max_loc[0] + distance_x, max_loc[1] + distance_y)
        multiplier = 1
        friend_position_on_minimap = (max_loc[0] + (friend_w / 2),max_loc[1] + (friend_h / 2))
        my_position_on_minimap = (int((map_w / 2)), int((map_h) / 2))
        dist = math.dist(my_position_on_minimap,friend_position_on_minimap)
        if dist < 180:
            multiplier = 1.2
        if friend_position[0] < (game_window[0] / 2):
            posx = friend_position[0] * (2 - multiplier)
        else:
            posx = friend_position[0] * multiplier
        if friend_position[1] < (game_window[1] / 2):
            posy = friend_position[1] * (2 - multiplier)
        else:
            posy = friend_position[1] * multiplier
        if max_val > 0.98:
            self.wincapture.get_screen_position((posx,posy))
            return True, posx, posy
        else:
            return False, 0, 0

    def fight(self, target): ## start thread with moving to someone
        while not self.IN_CITY:
            pos = self.find_pos_and_walk(self.minimap_path, target, self.method, self.window_size)
            if pos[0] == True:
                pyautogui.moveTo(pos[1], pos[2])
                pyautogui.click(button= "SECONDARY", clicks = randint(1,3), interval = random.uniform(0.1,0.3))

    def cast_spell(self, spells):  ##check spells and cast first avalible
        hold_time = 0.2
        if self.available_spells == []:
            self.available_spells = self.check_available_spell(spells)
            for _ in range(0,randint(5,8)):
                pyautogui.click()
                self.waitRandomizedTime(0.2,0.3)
        else: 
            cast = self.available_spells[randint(0,len(self.available_spells)-1)]
            for i in self.duration:
                if cast in i:
                    hold_time = float(i.replace(cast, "").replace(",","."))
        
            pyautogui.keyDown(cast)
            self.waitRandomizedTime(hold_time*0.8,hold_time)
            pyautogui.keyUp(cast)
            self.available_spells.remove(cast)
            self.waitRandomizedTime(2,3)

    ## exit from dungeon if finish
    def exit(self, song_of_escape):
        if self.find_pos(self.result_path, 0.95, cv2.TM_CCORR_NORMED) != False:
            while True:
                time.sleep(randint(2,3))
                pyautogui.press(song_of_escape)
                time.sleep(randint(8,10))
                if self.find_pos(self.ok2_button_path, 0.99, cv2.TM_CCORR_NORMED) == False:
                    self.MOVE = False
                    return True
        else:
            return False
            
    def check_res(self): ## check if character is dead
        x = self.find_pos(self.resurection_path, 0.98, cv2.TM_CCORR_NORMED)
        if x != False:
            try:
                pyautogui.moveTo(x[0] + randint(5,25), x[1 + randint(5, 10)])
                self.waitRandomizedTime(1,2)
                pyautogui.click()
                self.z = 0
            except:
                pass

    def check_in_fight(self):  ##check if character is in city
        if self.find_pos(self.check_in_fight_path, 0.9, cv2.TM_CCORR_NORMED) != False:
            self.MOVE = False
            return False
        else:
            return True

    def check_accept(self):
        accept_pos = self.find_pos(self.accept_path, 0.945, cv2.TM_CCOEFF_NORMED)
        if accept_pos != False:
            pyautogui.moveTo(accept_pos[0] + randint(5,15), accept_pos[1] + randint(3,15))
            pyautogui.click()

    ## search for chaos dungeon when in city
    def search_chaos(self):
        self.wincapture.focus_window()
        while self.IN_CITY == True:
            print("in city: ", self.IN_CITY)
            self.z = 0
            if self.IN_CITY == True:
                self.IN_CITY = self.check_in_fight()
            if self.repair == "y":
                self.repair_items()

            if self.IN_CITY == True:
                pyautogui.press('g')
                self.waitRandomizedTime(1,2)
                matchmaking_pos = self.find_pos(self.matchmaking_path, 0.99, cv2.TM_CCOEFF_NORMED)
                if matchmaking_pos != False:
                    pyautogui.moveTo(matchmaking_pos[0] + randint(30,100), matchmaking_pos[1] + randint(3,40))
                    pyautogui.click()

            self.check_accept()

    ## do chaos dungeon after finding one
    def do_chaos(self):
        while self.IN_CITY == False:  
            if self.z == 0:                                
                pyautogui.press("z")
                self.z += 1
            if not self.MOVE:
                self.MOVE = True
                start_moving = Thread(target = self.fight, args = (self.target_path,))
                start_moving.start()
            self.cast_spell(self.all_spells)
            self.check_res()
            self.check_accept()
            self.IN_CITY = self.exit( self.song_of_escape)
            

def capture_screen():
    while True:
        global screenshot
        screenshot = Lost_bot.wincapture.get_screenshot()
        time.sleep(0.5)

def kill_bot():
    Thread(target = capture_screen, args = ()).start()
    while True:
        if keyboard.is_pressed("del"):
            os._exit(1)
        time.sleep(1)


def run_bot():
    configure = input("Do you want configure bot? Y/N\n").lower()
    if configure == "y":
        configure_config()
    Esc = True
    while True:
        bot = Lost_bot()
        if Esc:
            Thread(target = kill_bot, args = ()).start()
            Esc = False
        bot.search_chaos()
        bot.do_chaos()
        
if __name__ == '__main__':
    run_bot()