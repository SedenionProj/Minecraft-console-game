import os
from math import sin, cos,sqrt

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit

# init variables
width,height = os.get_terminal_size()
height-=1
pixelBuffer = [' ']*(width*height-width)
camPosX = 0
camPosY = 1
camPosZ = 0
camRotX = 0
camRotY = 0

lPosX = 0
lPosY = 0
lPosZ = 0


focalLengh = 1.5
color = ".'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# screen
def clear(char):
    for i in range(width*height-width):
        pixelBuffer[i] = char
def draw(*info):
    info = ''.join(info)
    info += ' '*(width - len(info))
    print(info+''.join(pixelBuffer),end='')

# math
def AddVec3(v1,v2):
    return v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]

def SubVec3(v1,v2):
    return v1[0]-v2[0],v1[1]-v2[1],v1[2]-v2[2]

def dot(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

def MultScal(l,v):
    return l*v[0],l*v[1],l*v[2]

def crossProd(v1,v2):
    return v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v1[0]*v2[2],v1[0]*v2[1]-v1[1]*v2[0]

def dist(v):
    return sqrt(v[0]**2+v[1]**2+v[2]**2)

def normalize(v):
    l = dist(v)
    return v[0]/l,v[1]/l,v[2]/l if l!=0 else 0.0

def eq(p,a,b):
    return (a[0]-p[0])*(b[1]-p[1])-(a[1]-p[1])*(b[0]-p[0])

def LinePlaneCollision(planeNormal, planePoint, p1, p2):
    u=SubVec3(p2,p1)
    dotp = dot(planeNormal,u)
    if abs(dotp) < 1e-5:
        return (0,0,0)
    
    w = SubVec3(p1, planePoint)
    si = -dot(planeNormal,w)/dotp
    u = MultScal(si,u)
    return AddVec3(p1,u)

def inZ(planeNormal, planePoint,tri):
    L = []
    vert1 = dot(SubVec3(planePoint,tri[0]),planeNormal)
    vert2 = dot(SubVec3(planePoint,tri[1]),planeNormal)
    vert3 = dot(SubVec3(planePoint,tri[2]),planeNormal)
    if vert1 > 0:
        L.append(tri[0]) 
    if vert2 > 0:
        L.append(tri[1]) 
    if vert3 > 0:
        L.append(tri[2]) 
    return L,vert1*vert3>0

# transform

def getChar(value):
    return color[round(value*68)] if value>=0 else "."

def clipping(tri):
    v = tri.copy()
    clip = []
    normal = (-sin(camRotY)*cos(camRotX),sin(camRotX),cos(camRotY)*cos(camRotX))
    camPos = (camPosX,camPosY,camPosZ)
    zNear = AddVec3(camPos,MultScal(0.1,normal))
    L,invert = inZ(normal,zNear,v)
    if len(L) == 0:
        return [v]
    elif len(L) == 3:
        return None
    elif len(L) == 1:
        v.remove(L[0])
        vi0 = LinePlaneCollision(normal,zNear,v[0],L[0])
        vi1 = LinePlaneCollision(normal,zNear,v[1],L[0])
        if invert:
            clip.append([v[0],vi0,v[1]])
            clip.append([v[1],vi0,vi1])
        else:
            clip.append([vi0,v[0],v[1]])
            clip.append([vi0,v[1],vi1])
    elif len(L) == 2:
        v.remove(L[0])
        v.remove(L[1])
        vi0 = LinePlaneCollision(normal,zNear,L[0],v[0])
        vi1 = LinePlaneCollision(normal,zNear,L[1],v[0])
        if invert:
            clip.append([vi1,vi0,v[0]])
        else:
            clip.append([vi0,vi1,v[0]])
    return clip

def projection(pos):
    nz = focalLengh*2*pos[2]/2
    px = (2*height/width)*pos[0]/nz
    py = -pos[1]/nz
    return round((px+1)*width/2),round((py+1)*height/2)

def rotationx(pos):
    y1=cos(camRotX)*pos[1]-sin(camRotX)*pos[2]
    z1=sin(camRotX)*pos[1]+cos(camRotX)*pos[2]
    return pos[0],y1,z1

def rotationy(pos):
    x1=cos(camRotY)*pos[0]+sin(camRotY)*pos[2]
    z1=-sin(camRotY)*pos[0]+cos(camRotY)*pos[2]
    return x1,pos[1],z1

# shapes

def putPixel(x,y,char):
    if 0<=x<width and 0<=y<height-1:
        pixelBuffer[round(y)*width+round(x)] = char

def triangle(pos,char):    
    xmin = min(pos[0][0],pos[1][0],pos[2][0])
    xmax = max(pos[0][0],pos[1][0],pos[2][0])+1
    ymin = min(pos[0][1],pos[1][1],pos[2][1])
    ymax = max(pos[0][1],pos[1][1],pos[2][1])+1
    for y in range(ymin,ymax):
        if 0<=y<height-1:
            for x in range(xmin,xmax):
                if 0<=x<width:
                    w0=eq((x,y),pos[2],pos[0])
                    w1=eq((x,y),pos[0],pos[1])
                    w2=eq((x,y),pos[1],pos[2])
                    if (w0 >= 0 and w1 >= 0 and w2 >= 0) or (-w0 >= 0 and -w1 >= 0 and -w2 >= 0):
                        putPixel(x,y,char)

def triangle3D(tri):
    clipped = clipping(tri)
    if clipped is None:
        return
    for tri2 in clipped:
        line1 = SubVec3(tri2[1],tri2[0])
        line2 = SubVec3(tri2[2],tri2[0])
        norm = normalize(crossProd(line1,line2))
        if dot(norm,SubVec3(tri2[0],[camPosX,camPosY,camPosZ])) < 0:
            lum = getChar(dot(norm,normalize((lPosX,lPosY,lPosZ))))
            v = [projection(rotationx(rotationy(SubVec3(i,(camPosX,camPosY,camPosZ))))) for i in tri2]
            triangle(v,lum)

def mesh(m):
    m.sort(key=lambda x:dist(SubVec3(MultScal(1/3,AddVec3(x[0],AddVec3(x[1],x[2]))),(camPosX,camPosY,camPosZ))),reverse=True)
    for tri in m:
        triangle3D(tri)

def drawTex(tx,ty,tex):
    x = tx
    y = ty
    for c in tex:
        if c == '°':
            y+=1
            x=tx
            continue
        putPixel(x,y,c)
        x+=1
# obj
def loadObj(name):
    f = open(name, "r")
    lines = [line.rstrip('\n').split(' ') for line in f.readlines() if line.rstrip('\n')]
    f.close()
    vert = [list(map(float,line[1:])) for line in lines if line[0] == 'v']
    order = [line[1:] for line in lines if line[0] == 'f']

    vertex = []
    for tri in order:
        if len(tri) == 4:
            vertex.append([vert[int(tri[0])-1],vert[int(tri[1])-1],vert[int(tri[2])-1]])
            vertex.append([vert[int(tri[2])-1],vert[int(tri[3])-1],vert[int(tri[0])-1]])
        if len(tri) == 3:
            vertex.append([vert[int(tri[0])-1],vert[int(tri[1])-1],vert[int(tri[2])-1]])
    return vertex

def translate(m,vec):
    mesh = []
    for tri in m:
        mesh.append([AddVec3(tri[0],vec),AddVec3(tri[1],vec),AddVec3(tri[2],vec)])
    return mesh

def scale(m,l):
    mesh = []
    for tri in m:
        mesh.append([MultScal(l,tri[0]),MultScal(l,tri[1]),MultScal(l,tri[2])])
    return mesh

def checkSameMesh(m1,m2):
    v1 = []
    v2 = []
    [v1.append(i) for sl in m1 for i in sl if i not in v1]
    [v2.append(i) for sl in m2 for i in sl if i not in v2]
    for v in v1:
        if not v in v2:
            return False
    return True

def removeFaces2(m):
    mesh = []
    for i in range(len(m)//2):
        face = [m[2*i],m[2*i+1]]
        check = True
        for j in range(len(m)//2):
            face1 = [m[2*j],m[2*j+1]]
            if checkSameMesh(face,face1) and i!=j:
                check =False
                break
        if check:
            mesh+=face
    return mesh

def removeFaces(m,cube):
    mesh = []
    for i in range(len(cube)//2):
        face = [cube[2*i],cube[2*i+1]]
        check = True
        for j in range(len(m)//2):
            face1 = [m[2*j],m[2*j+1]]
            if checkSameMesh(face,face1) and i!=j:
                check =False
                break
        if check:
            mesh+=face
    return mesh