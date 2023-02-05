import sources.engine as engine
import sources.menu as menu
import sources.minecraft as  minecraft
import sources.options as options
import time

last = 0

windowID = 0

while True:
    # main loop
    engine.clear(' ')
    current = time.time()
    dt = (current-last)*10
    last=current

    if windowID == 0:
        windowID = menu.main(dt)
    elif windowID == 1:
        windowID = minecraft.main(dt)
    elif windowID == 2:
        windowID = options.main(dt)

    if dt>0:
        fps = 10/dt

    engine.draw(" fps : ",str(round(fps)))

