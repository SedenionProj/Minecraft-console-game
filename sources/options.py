import sources.engine as engine
import sources.minecraft as minecraft
import keyboard
optionTex = " _____     _   _                   °|     |___| |_|_|___ ___ ___       °|  |  | . |  _| | . |   |_ -|_ _ _ °|_____|  _|_| |_|___|_|_|___|_|_|_|°      |_|   "

selectID = 0
hold = True
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
    elif keyboard.is_pressed("s"):
        keyboard.release("enter")
        val = input()
        try:
            if not hold:
                if selectID%5 == 0:
                    minecraft.sensitivityRot = float(val)
                if selectID%5 == 1:
                    engine.focalLengh = float(val)
        except:
            pass
        hold = True
    else:
        hold = False
    if keyboard.is_pressed("esc"):
        return 0
    

    engine.drawTex(10,1,optionTex)
    engine.drawTex(2,10,f"sensitivity : {minecraft.sensitivityRot}°focalLengh : {engine.focalLengh}°")
    engine.putPixel(20,10+selectID%5,"█")
    return 2