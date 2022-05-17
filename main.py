from email.mime import image
import threading
from cv2 import threshold
import pyautogui, time, random, cv2, math, keyboard, os, numpy as np
from PIL import Image
from random import randint
from threading import Thread
from window_capture import WindowCapture

import multiprocessing
pyautogui.FAILSAFE = False
from config import configure_config

class Lost_bot():
    # properties
    wincapture = WindowCapture("LOST ARK (64-bit, DX11) v.2.2.4.1")
    translate_pos = wincapture.get_screen_position
    global screenshot
    screenshot = wincapture.get_screenshot()
    MINI_BOSS = False
    FINAL_BOSS = False
    IN_CITY = True
    MOVE = False
    CAST = False
    BOT_WORKING = False
    DIST = 0
    CAN_FIGHT = True
    available_spells = ['q','w','e', 'r', 'a', 's','d', 'f']
    all_spells =  ['q','w','e', 'r', 'a', 's','d', 'f']
    window_size = (wincapture.w, wincapture.h)
    NEXT_ROUND = False
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
    # target_path = 'images\\pixel.png'
    enemy_health_path = 'images\\enemy_health.png'
    mini_boss_path = "images\\mini_boss.png"
    big_boss = "images\\big_boss.png"
    # final_boss_path = "final_boss2.png"
    enemy_path = "images\\enemy.png"
    # portal_path = "portal2.png"
    empty_chaos = "images\\empty_chaos.png"
    spell_check = "images\\spell_check.png"
    result_path = "images\\result.png"
    matchmaking_path = "images\\matchmaking.png"
    enter_path = "images\\enter.png"
    ok2_button_path = "images\\ok.png"
    resurection_path = "images\\base_res.png"
    check_in_fight_path = "images\\check_in_fight.jpg"
    accept_path = "images\\ccept.jpg"
    #Large image of the next round
    next_path = "images\\next_path.png"
    mini_and_final_path = "images\\mini_and_final.png"
    chaos_portal_path = "images\\chaos_portal.png"
    ret_test_path = "images\\ret_test.png"
    char_and_ret_tes_path = "images\\char_and_ret_test.png"
    

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

        for spell in all_spells:
            path = ("images\\" + str(spell) + ".png")
            result = self.find_pos(path, 0.70, cv2.TM_CCORR_NORMED)
            #print('what is the resutl from the find_pos', result)
            if result and (result[0] != 0 or result[1] != 0):
                #print("Spell is now off cooldown")
                self.available_spells.append(spell)
        #print("available spells: ", self.available_spells)

        return self.available_spells

    def find_pos(self, what_find_path, threshold, method):
        #print('image:', what_find_path)

        find_this = cv2.imread(what_find_path, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(screenshot, find_this, method)

        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
        #print("maxVal",maxVal, "what_find_path", what_find_path)
        if maxVal > threshold:
            #print("this is the location of the screen we want", self.wincapture.get_screen_position(maxLoc))
            return self.wincapture.get_screen_position(maxLoc)
        else:
            return False
        
    def next_round(self):
        res = self.compare_two_img(self.chaos_portal_path)
        if not res:
            return

        #print('res is what dz', res)
        if res and res[1] != 0 and res[2] != 0:
            #print('NEXT_ROUND IS TRUE DZ', res)

            pyautogui.dragTo(res[1], res[2])
            pyautogui.press('space')
            pyautogui.click(clicks = randint(3,4))
            pyautogui.press('g')
            self.FINAL_BOSS = False
            self.MINI_BOSS = False

        return


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
            #print("Repair start")
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
    def compare_two_img(self, target_img):
        #print('compare to template:', target_img)
        minimap_path = self.minimap_path
        im = screenshot
        cropped_image = im[40:295, 1593:1889]
        im_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('im_gray', im_gray)
        # cv2.waitKey(0)

        cv2.imwrite(minimap_path, cropped_image)
        im = cropped_image
        
        target = cv2.imread(target_img, 0)
        # cv2.imshow('template', target)
        # cv2.waitKey(0)
        _,map_w, map_h = im.shape[::-1]
        target_w, target_h = target.shape[::-1]

        # cv2.imshow('img_resize', im)
        # cv2.waitKey(0)
        result = cv2.matchTemplate(im_gray, target, cv2.TM_CCOEFF_NORMED)
        max_val = 0
        loc = np.where(result>=.75)
        for pt in zip(*loc[::-1]):
            # #print('SOMETHING GREATER THAN THRESHOLD .7')
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print('target_img', target_img, 'max_val:', max_val)
            #print('max_val match to template', max_val)
            # color = (255,0,0)
            # img = cv2.rectangle(im, pt,(pt[0] + target_w , pt[1] + target_h), color, 2)
            # if target_img == self.big_boss:
            #     #print("WE ARE MATCHED WITH BOSSES DZ", target_img)
            #     cv2.imshow('TEMPLATE MATCHED', img)
            #     cv2.waitKey(0)
        
            ## count distance how far we have to move our screenshot to place it on middle of screen
            distance_x = (self.window_size[0] - map_w) / 2
            distance_y = (self.window_size[1] - map_h) / 2
            # #print('distance_x between us', distance_x, 'distance_y from us', distance_y)

            target_position = (max_loc[0] + distance_x, max_loc[1] + distance_y)
            # #print('target_pos', target_position)

            multiplier = 1
            target_position_on_minimap = (max_loc[0] + (target_w / 2),max_loc[1] + (target_h / 2))
            
            my_position_on_minimap = (int((map_w / 2)), int((map_h) / 2))
            # #print('Char position on map', my_position_on_minimap)
            dist = math.dist(my_position_on_minimap,target_position_on_minimap)
            # #print("Distance between targ & you" ,dist)
            # #print('what is my max_val', max_val)
            posx, posy = 0,0
            if dist < 100: 
                self.DIST = dist
            if dist < 1200:
                multiplier = 1.1
  
            if target_position[0] < ( self.window_size[0] / 2):
                posx = target_position[0] * (2 - multiplier)
            else:
                posx = target_position[0] * multiplier
            if target_position[1] < ( self.window_size[1] / 2):
                
                posy = target_position[1] * (2 - multiplier)
            else:
                posy = target_position[1] * multiplier
                
            if target_position[0] < ( self.window_size[0] / 2):
                posx = target_position[0] * (2 - multiplier)
            else:
                posx = target_position[0] * multiplier

            if target_position[1] < ( self.window_size[1] / 2):
                posy = target_position[1] * (2 - multiplier)
            else:
                posy = target_position[1] * multiplier
            
            #print('New Pos X and Pos Y', True, posx, posy)
            self.wincapture.get_screen_position((posx,posy))
            return True, posx, posy
        return False, 0,0
 
    def find_pos_and_walk(self, minimap_path, target, method, game_window):
            #print('Pos Walk of mini map to -->', target)
            # #print("IN RELATION TO ")
            im = screenshot
            cropped_image = im[40:295, 1593:1889]
            im_gray = cv2.imread(minimap_path, cv2.IMREAD_GRAYSCALE)
            
            # cv2.imshow('img', cropped_image)
            # cv2.waitKey(0)
            cv2.imwrite(minimap_path, cropped_image)
            im = cropped_image

            ## clear a little our minimap to avoid some wrong matches
            thresh = cv2.threshold(im_gray,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            kernel = np.ones((12,12),np.uint8)
            closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            kernel = np.ones((15,15),np.uint8)
            closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            

        
            ## use our mask to minimap
            res = cv2.bitwise_and(im,im,mask = closing)

            #Target can be mob, or anything
            target = cv2.imread(target)
        
            ## resize to get vector
            # im = cv2.resize(res, None, fx = 4, fy = 3)
            result = cv2.matchTemplate(im, target, method)
            min_val,max_val,min_loc, max_loc = cv2.minMaxLoc(result)
            _,map_w,map_h = im.shape[::-1]
            _,target_w,target_h = target.shape[::-1]

            ## count distance how far we have to move our screenshot to place it on middle of screen
            distance_x = (game_window[0] - map_w) / 2
            distance_y = (game_window[1] - map_h) / 2
            #print('distance_x between us', distance_x, 'distance_y from us', distance_y)

            ## count where is my character and target character to get distance between them. 
            # If it is too big, just run to target, dont cast spells. Also multiply 
            # values to get further posx posy
            target_position = (max_loc[0] + distance_x, max_loc[1] + distance_y)
            #print('target_pos', target_position)

            multiplier = 1
            target_position_on_minimap = (max_loc[0] + (target_w / 2),max_loc[1] + (target_h / 2))
            
            my_position_on_minimap = (int((map_w / 2)), int((map_h) / 2))
            #print('Char position on map', my_position_on_minimap)
            dist = math.dist(my_position_on_minimap,target_position_on_minimap)
            #print('Distance from:', target, "to YOU DZ:" ,dist)
            #print('what is my max_val', max_val)
            posx, posy = 0,0
            if dist < 100:
                multiplier = 1.1


            if dist < 180:
                multiplier = 1.2
            if target_position[0] < (game_window[0] / 2):
                posx = target_position[0] * (2 - multiplier)
            else:
                posx = target_position[0] * multiplier
            if target_position[1] < (game_window[1] / 2):
                posy = target_position[1] * (2 - multiplier)
            else:
                posy = target_position[1] * multiplier
            if max_val > 0.80 and target == self.next_path:
                self.wincapture.get_screen_position((posx,posy))
                #print('posx NEXT ROUND', posx, 'posy NEXT ROUND', posy)
                pyautogui.moveTo(posx,posy)
                pyautogui.press('space')
                pyautogui.click()
                pyautogui.press('g')
                return True, posx, posy

            elif max_val > 0.87 and target != self.next_path:
                self.wincapture.get_screen_position((posx,posy))
                #print("Meet threshhold for target DZ..")
                #print('posx', posx, 'posy', posy)
                return True, posx, posy
            else:
                return False, 0, 0


    def fight(self, target): 
        print('fighting function with target', target)
        
        #Find the position to the first target
        pyautogui.click(button='PRIMARY')
        if self.DIST > 160: #Need closer to cast skill
            return 
        pos = self.compare_two_img(target)
        #print('fight pos', pos)
        if pos[0] == False:
            #print('done fighting?',pos)
            return
        if pos[0] == True and target == self.big_boss:
            self.FINAL_BOSS = True
        if pos[0] == True and target == self.mini_boss_path:
            self.MINI_BOSS = True
        elif pos[0] == True:

            pyautogui.moveTo(pos[1], pos[2])
            pyautogui.press('z')
            
            if pos[1] and pos[2] == 0:
                #print('invalid resp')
                return

            if len(self.available_spells) == 0:
                self.available_spells = self.check_available_spell(self.all_spells)
                pyautogui.moveTo(pos[1], pos[2])
                pyautogui.click(button= "SECONDARY", clicks = randint(1,3), interval = random.uniform(0.1,0.3))
            if len(self.available_spells) != 0:
                #print('spells to use')
                self.cast_to_enemy(self.all_spells, pos[1], pos[2])

    


    def move_around(self):
        #print('moving around')
        pyautogui.click(randint(1000,1050),randint(1000,1050))
        return

    def cast_to_enemy(self, spells, pos_x,pos_y):  ##check spells and cast first avalible
        if pos_x <= 0 or pos_y <= 0:
            return
        # self.move_around()
        #print('x & y coord', pos_x, pos_y)
        #print('avail_spells entrance', self.available_spells)

        hold_time = 0.2
        if self.available_spells == []:
            self.available_spells = self.check_available_spell(spells)
            for _ in range(0,randint(5,8)):
                pyautogui.click(clicks=2)
                self.waitRandomizedTime(0.2,0.3)
        else: #available_spells != []
            cast = self.available_spells[randint(0,len(self.available_spells)-1)]
            for i in self.duration:
                if cast in i:
                    hold_time = float(i.replace(cast, "").replace(",","."))
            #print('using spell', cast)
            pyautogui.moveTo(pos_x, pos_y)
            pyautogui.click(clicks=2)
            pyautogui.keyDown(cast)
            self.waitRandomizedTime(hold_time*.8,hold_time)
            pyautogui.keyUp(cast)
            if cast in self.available_spells:
                #print('can remove spell')
                self.available_spells.remove(cast)

            self.waitRandomizedTime(0.15,0.25)
            
            #print('self.available_spells after usage', self.available_spells)

    ## exit from dungeon if finish
    def exit(self, song_of_escape):
        if self.find_pos(self.result_path, 0.95, cv2.TM_CCORR_NORMED) == True:
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
        res_check = self.find_pos(self.resurection_path, 0.90, cv2.TM_CCORR_NORMED)
        if res_check == False:
            #print('Alive')
            return
        #print('res_check dz', res_check)
        if res_check:
            #print('Dead')
            pyautogui.moveTo(res_check[0] + randint(1,10),  res_check[1] + randint(1,10))
            self.waitRandomizedTime(.5,1)
            pyautogui.click()
            self.z = 0

    ##check if character is in city
    def check_in_fight(self): 
        if self.find_pos(self.check_in_fight_path, 0.90, cv2.TM_CCORR_NORMED) != False:
            
            self.MOVE = False
            return False
        else:
            return True
        


    def check_accept(self):
        accept_pos = self.find_pos(self.accept_path, 0.90, cv2.TM_CCOEFF_NORMED)
        if accept_pos != False:
            pyautogui.moveTo(accept_pos[0] + randint(5,15), accept_pos[1] + randint(3,15))
            pyautogui.click()

    ## search for chaos dungeon when in city
    def search_chaos(self):
        self.wincapture.focus_window()
        while self.IN_CITY == True:
            #print("In the City")
            self.z = 0
            if self.IN_CITY == True:
                
                self.IN_CITY = self.check_in_fight()
                self.repair_items()
                

            if self.IN_CITY == True:
                #print('GOING INTO CHAOS DUNGEON')
                pyautogui.press('g')
                self.waitRandomizedTime(1,2)
                
               
                matchmaking_pos = self.find_pos(self.enter_path, 0.95, cv2.TM_CCOEFF_NORMED)
                
                if matchmaking_pos != False:
                    pyautogui.moveTo(matchmaking_pos[0] + randint(30,100), matchmaking_pos[1] + randint(3,40))
                    pyautogui.click()

            self.check_accept()

    def check_start(self):
        is_empty = self.find_pos(self.empty_chaos, .95, self.method)
        if is_empty:
            return True
        else: 
            return False
    def walk_around(self, is_empty):
        
        if is_empty:
 
            pyautogui.moveTo(668, 709)
            pyautogui.click(duration=3)
            pyautogui.moveTo(1245, 450)

            return True  
        else:
            return False

    ## do chaos dungeon g
    def do_chaos(self):
        #print('IN THE DO_CHAOS function')
        # next_rd = multiprocessing.Process(target=self.next_round())
        # next_rd.start()
        # next_thread = threading.Thread(target=self.next_round())
        # next_thread.start()
        if self.MINI_BOSS == False or self.FINAL_BOSS == False:
            self.next_round()
            self.fight(self.enemy_path)
            self.fight(self.mini_boss_path)
            self.fight(self.big_boss)
            self.check_res()
        elif self.MINI_BOSS == True and self.FINAL_BOSS != True:
            print("DZ DZ DZ we are at mini boss")
            self.next_round()
            self.fight(self.mini_boss_path)
            self.fight(self.big_boss)
            self.check_res()
        elif self.FINAL_BOSS == True:
            print("FINAL BOSS FIGHT ONLY DZZZ")
    
            self.next_round()
            self.fight(self.big_boss)
            self.check_res()

        # f1 = multiprocessing.Process(target=self.fight(self.enemy_path))
        # f1_thread = threading.Thread(target=self.fight(), args=self.enemy_path)
        # f1_thread.start()
        # f1.start()
        # self.fight(self.mini_boss_path)
        # self.fight(self.big_boss)

        # res_thread = threading.Thread(target=self.check_res())
        # res_thread.start()
        
        # next_thread.join()
        # f1_thread.join()
        # res_thread.join()
        # res_multi = multiprocessing.Process(target=self.check_res())
        # res_multi.start()

        # next_rd.join()
        # f1.join()
        # res_multi.join()


        # self.fight()
        # self.wincapture.focus_window()
        # while self.IN_CITY == False: 
        #     #print('Not in City')
        #     if self.z == 0:                              
        #         pyautogui.press("z")
        #         self.z += 1
            # if self.MOVE == False:
                # self.MOVE = True
            
            # self.fight(self.enemy_path)
            # self.fight_boss(self.mini_and_final_path)
           

            # self.IN_CITY = self.exit( self.song_of_escape)
            

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
    Esc = True
    bot = Lost_bot()
    bot.do_chaos()
    while True:

        if Esc:
            Thread(target = kill_bot, args = ()).start()
        Esc = False
        bot.search_chaos()
        bot.do_chaos()
    
    

        
if __name__ == '__main__':
    # run_bot()
    run_bot()
        
