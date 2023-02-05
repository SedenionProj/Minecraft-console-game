import pip
from math import sin, cos
from random import randint
try:
    import keyboard
except:
    print('Installing keybord module...')
    pip.main(['install', "keyboard"])
    try:
        import keyboard
    except:
        print('Failed to install "keyboard" module,\ncheck your internet connection, make sure you have admin privilege\nor try : pip install keybord')
        input()
        exit()
import sources.engine as engine
sensitivityRot = 0.3
sensitivityMov = 0.5

# main
cube = [[[0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]], [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5]], [[0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5]], [[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5]], [[-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5]], [[0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5]], [[-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5]], [[-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5], 
[-0.5, -0.5, 0.5]], [[0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5]], [[-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5]], [[0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5]], [[-0.5, -0.5, 0.5], [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5]]]

vertexBuffer = []
chatHistory = ""

def chat():
    global chatHistory
    def openChat():
        x=0
        y=0
        for c in chatHistory:
            if c == "°":
                y+=1
                x=0
                continue
            engine.putPixel(x,y,c)
            x+=1
    while True:
        engine.mesh(vertexBuffer)
        openChat()
        engine.draw("CHAT OPENED")
        m = input()
        msg= m.split()
        if len(msg) == 0:
            return        
        if msg[0][0] == "/":
            msg[0] = msg[0][1:]
            if msg[0] == "help":
                chatHistory += f"[to execute a command write '/' followed by the name of one of the commands :]°"
                chatHistory += f"'help' - show help menu°"
                chatHistory += f"'tp x y z' - teleport to x y z°"
                chatHistory += f"'clear' - clear the chat°"
                chatHistory += f"'getLive' - get a variable from the°"
            elif msg[0] == "tp":
                engine.camPosX = int(msg[1])
                engine.camPosY = int(msg[2])
                engine.camPosZ = int(msg[3])
                chatHistory += f"[teleported to {msg[1]} {msg[2]} {msg[3]}]°"
            elif msg[0] == "clear":
                chatHistory = ""
            elif msg[0] == "getLive":
                try:
                    chatHistory += f"[value of '{msg[1]}' is {globals()[msg[1]]}]°"
                except:
                    chatHistory += f"['{msg[1]}' was not found.]°"
            else:
                chatHistory += f"['{m}' is not a valid command.]°"
        else:
            chatHistory += m+'°'

def placeBlock(vb,chunk,x,y,z):
    def isNotFilled(x,y,z):
        if x < 0 or x > 15 or y < 0 or y > 15 or z < 0 or z > 15:
            return True
        if chunk[x][y][z]==1:
            return False
        return True    
    if isNotFilled(x,y,z+1):
        vb += engine.translate(cube[0:2],(x,y,z))
    if isNotFilled(x+1,y,z):
        vb += engine.translate(cube[2:4],(x,y,z))
    if isNotFilled(x,y,z-1):
        vb += engine.translate(cube[4:6],(x,y,z))
    if isNotFilled(x-1,y,z):
        vb += engine.translate(cube[6:8],(x,y,z))
    if isNotFilled(x,y+1,z):
        vb += engine.translate(cube[8:10],(x,y,z))
    if isNotFilled(x,y-1,z):
        vb += engine.translate(cube[10:12],(x,y,z))
    if isNotFilled(x,y,z):
        chunk[x][y][z]=1
    
    
    
chunk = [[[0 for _ in range(16)] for _ in range(16)] for _ in range(16)]

def generation(vb):
    
    for x in range(16):
        for z in range(16):
            chunk[x][randint(0,0)][z] = 1

    for x in range(16):
        for y in range(16):
            for z in range(16):
                if chunk[x][y][z] == 1:
                    placeBlock(vb,chunk,x,y,z)
    return vb

t = 0.5

def init():
    print("loading chunk...")
    generation(vertexBuffer)

def main(dt):
    global t
    t+=dt/100

    if keyboard.is_pressed("down arrow"):
        if engine.camRotX>-1.57:
            engine.camRotX-=dt*sensitivityRot
    if keyboard.is_pressed("up arrow"):
        if engine.camRotX<1.57:
            engine.camRotX+=dt*sensitivityRot
    if keyboard.is_pressed("left arrow"):
        engine.camRotY+=dt*sensitivityRot
    if keyboard.is_pressed("right arrow"):
        engine.camRotY-=dt*sensitivityRot
    if keyboard.is_pressed("s"):
        engine.camPosX-=-sin(engine.camRotY)*dt*sensitivityMov
        engine.camPosZ-=cos(engine.camRotY)*dt*sensitivityMov
    if keyboard.is_pressed("z"):
        engine.camPosX+=-sin(engine.camRotY)*dt*sensitivityMov
        engine.camPosZ+=cos(engine.camRotY)*dt*sensitivityMov
    if keyboard.is_pressed("d"):
        engine.camPosX+=cos(engine.camRotY)*dt*sensitivityMov
        engine.camPosZ+=sin(engine.camRotY)*dt*sensitivityMov
    if keyboard.is_pressed("q"):
        engine.camPosX-=cos(engine.camRotY)*dt*sensitivityMov
        engine.camPosZ-=sin(engine.camRotY)*dt*sensitivityMov
    if keyboard.is_pressed("shift"):
        engine.camPosY-=dt*sensitivityMov
    if keyboard.is_pressed("space"):
        engine.camPosY+=dt*sensitivityMov
    if keyboard.is_pressed("t"):
        chat()
    if keyboard.is_pressed("esc"):
        return 0
    if keyboard.is_pressed("o"):
        placeBlock(vertexBuffer,chunk,round(engine.camPosX),round(engine.camPosY),round(engine.camPosZ))
    
    engine.lPosX=50*cos(t)
    engine.lPosY=50*sin(t)
    engine.mesh(vertexBuffer)
    return 1