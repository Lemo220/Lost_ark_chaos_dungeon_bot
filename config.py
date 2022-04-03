from mss import mss
from PIL import Image

spells_regions = {"q" : (685,982,715,1013), 
                    "w" : (735, 982, 765,1013), 
                    "e" : (785, 982, 815, 1013),
                     "r" : (835, 982, 865, 1013), 
                     "a" : (707, 1030, 742, 1060), 
                     "s" : (757, 1030, 792, 1060), 
                     "d" : (807, 1030, 842, 1060), 
                     "f" : (857, 1030, 892, 1060),
                     "z" : (947, 1013,969, 1036)
                     },


def configure_config():
    hold_spells = []
    print()
    print("Hey, thank you for downloading and enjoy!\nRemember, bot use mouse and keyboard so you can't do anything on computer when it's working.\nIf you want to stop him just hold 'ESC' for 1-2 seconds.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("!!!! IMPORTANT !!!!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("You must stay in place where spells are available to configure everything correctly! (You can't be in big city, spells can't be on cooldown, anything can't cover up spells etc.)")
    print("If you are berserker with mayhem and you want use 'Z' as regular spell, turn on mayhem and then configure.")
    print("Let me know on GitHub if you have any problems or you have some ideas how to improve him :)")
    print()
    spells_input = input("""What spells do you want to use? (example: qwesd) \nAvailable spells: qwerasdf\n""")
    hold_spells_input = input("""Which of these spells has to be hold?\n""")
    for spell_duration_hold in hold_spells_input:
        duration = input("""How long hold spell """ + spell_duration_hold + "? (in seconds, must be integer)\n")
        hold_spells.append(spell_duration_hold + duration)

    song_of_escape = input("At which slot (5-9) do you have song of escape? (Need it to leave dungeon)\n")
    f = open("config.txt", "w")
    line1 = "spells = " + spells_input
    line2 = " ".join(map(str,hold_spells))
    line3 = "song of escape: " + song_of_escape
    f.write(line1 + "\n" + "spell/time(s): "+ line2 + "\n" + line3)


    for spell in spells_input:
        print(spell)
        x = mss().grab((spells_regions[0][spell]))
        img = Image.frombytes("RGB", x.size, x.bgra, "raw", "BGRX")
        img.save("images\\" + spell + ".png")
if __name__ == '__main__':
    configure_config()