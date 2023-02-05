import sources.engine as engine
import keyboard
import sources.minecraft as minecraft
logoTex = "███╗   ███╗██╗███╗   ██╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗°████╗ ████║██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝°██╔████╔██║██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║   °██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║   °██║ ╚═╝ ██║██║██║ ╚████║███████╗╚██████╗██║  ██║██║  ██║██║        ██║   °╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   "
singpTex = " _____ _         _         _                 °|   __|_|___ ___| |___ ___| |___ _ _ ___ ___ °|__   | |   | . | | -_| . | | .'| | | -_|  _|°|_____|_|_|_|_  |_|___|  _|_|__,|_  |___|_|  °            |___|     |_|       |___|        "
optionTex = " _____     _   _                   °|     |___| |_|_|___ ___ ___       °|  |  | . |  _| | . |   |_ -|_ _ _ °|_____|  _|_| |_|___|_|_|___|_|_|_|°      |_|   "
multiTex = " _____     _ _   _     _                 °|     |_ _| | |_|_|___| |___ _ _ ___ ___ °| | | | | | |  _| | . | | .'| | | -_|  _|°|_|_|_|___|_|_| |_|  _|_|__,|_  |___|_|  °                  |_|       |___|        "
selectTex = "   █°  ██° ███°████° ███°  ██°   █"


selectID = 0
hold = False
def main(dt):
    global hold
    global selectID
    if keyboard.is_pressed("up arrow"):
        if not hold:
            selectID -= 1
        hold = True
    elif keyboard.is_pressed("down arrow"):
        if not hold:
            selectID += 1
        hold = True
    else:
        hold = False

    if keyboard.is_pressed("enter"):
        if selectID%3 == 0:
            minecraft.init()
            return 1
        elif selectID%3 == 1:
            return 2
        elif selectID%3 == 2:
            return 3

    engine.drawTex(10,5,logoTex)
    engine.drawTex(10,20,singpTex)
    engine.drawTex(10,30,optionTex)
    engine.drawTex(10,40,multiTex)
    engine.drawTex(60,[20,30,40][selectID%3],selectTex)
    return 0