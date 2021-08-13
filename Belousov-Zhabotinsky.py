import numpy as np
import time
from PIL import Image, ImageShow, ImagePalette



def nebor2(population1, i, j, d):
    start1 = i - d
    end1 = i + d
    start2 = j - d
    end2 = j + d
    if start1 < 0:
        start1 = 0
    if start2 < 0:
        start2 = 0
    if end1 > 199:
        end1 = 199
    if end2 > 199:
        end2 = 198

    ne = population1[start1:end1 + 1,start2:end2 + 1]
    if np.count_nonzero((0<ne) & (ne<7)) >=2 :
        return True
    else:
        return False

def popn_gen():
    return np.random.choice(a = [0,1,2,3,4,5,6,7], p =[0.7,0.3,0,0,0,0,0,0], size = (200,200))

def update(popn):
    new = np.zeros_like(popn)
    x,y = popn.shape
    for i in range(0,x):
        for j in range(0,y):
            a = popn[i,j]
            if a == 0:
                if nebor2(popn,i,j,1):
                    new[i,j] = 1
            elif a == 1 or a == 2 or a== 3 or a == 4 or a == 5 or a == 6:
                new[i,j] = a + 1
            elif a == 7:
                new[i,j] = 0
    return new

def cond(popn,new,down,up,left,right,d_l,d_r,u_l,u_r):
    if popn == 0:
        temp = np.array([down,up,left,right,d_l,d_r,u_l,u_r])
        if np.count_nonzero((0 < temp) & (temp<= 3)) >= 2 :
            new = 1
    elif popn == 1 or popn==2 or popn == 3:
        new = popn + 1
    elif popn == 4:
        new = 0
    return new


def main():
    im = []
    popn = popn_gen()
    for i in range(0,50):
        print(i)
        popn = update(popn)
        im.append(Image.fromarray(popn).convert('P'))
    return im

def main2():
    im = []
    popn = popn_gen()
    vcond = np.vectorize(cond)
    for i in range(0,100):
        print(i)
        new = np.zeros_like(popn)
        down = np.roll(popn, 1, axis=0)
        up = np.roll(popn, -1, axis=0)
        left = np.roll(popn, -1, axis=1)
        right = np.roll(popn, 1, axis=1)
        d_l = np.roll(down,-1,axis = 1)
        d_r = np.roll(down,1,axis = 1)
        u_l = np.roll(up,-1,axis = 1)
        u_r = np.roll(up,1,axis = 1)
        popn = vcond(popn,new,down,up,left,right,d_l,d_r,u_l,u_r)
        im.append(Image.fromarray(popn).convert('P'))
    return im


palette = []
for i in range(256):
    palette.extend((np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)))
assert len(palette) == 768    

im = main()


im[0].save('z.gif', save_all=True, append_images=im[1:],
           optimize=True, duration=5, loop=True, palette = palette)