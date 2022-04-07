Lost ark bot to farm chaos dungeons.

Before first running the bot, run the config file to configure everything. You need to stay not in a big city (need to have available cast spells) to let bot get screens of your spells. After that, just run main.py and let the magic work! You need to have "Song of Escape" on your hotkeys to let the bot get out of the dungeon.

You have to stay near the column that let you enter to chaos dungeon, then just run the bot.

I used a lot of libraries like pyautogui to manage all actions and locate images on screen, cv2 to manipulate the screen of the minimap to find the right way to ally, scale it to normal size, and move. Mss to speed up screenshot function. Few more popular libraries like random, time, Image, etc. Bot use now threading that lets him get faster moves and doesn't look like a bot.

Bot work for every class in-game but first is needed to configure with config.py

If you have any questions or ideas on how to improve the bot, just write to me on GitHub in the Issues tab!
