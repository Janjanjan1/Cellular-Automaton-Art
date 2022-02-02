import numpy as np
from numba import njit
from PIL import Image, ImageShow, ImagePalette
from tqdm import tqdm
@njit()
def nebor2(popn,i,j,a, size):
    d = 1
    start1 = i - d
    end1 = i + d
    start2 = j - d
    end2 = j + d
    if start1 < 0:
        start1 = 0
    if start2 < 0:
        start2 = 0
    if end1 > size -1 :
        end1 = size - 2
    if end2 > size - 1:
        end2 = size -2

    ne = popn[start1:end1+1,start2:end2+1].flatten()
    return np.count_nonzero(ne == a) > 1
#A = 3 for non symmetric spirals and A = 4 for symmetric
@njit()
def loop(popn,new, size):
    for i in range(0,size):
        for j in range(0,size):
            a = popn[i,j] + 1
            if a == 4:
                a = 0
            if nebor2(popn,i,j,a, size) == True:
                new[i,j] = a
            else:
                new[i,j] = popn[i,j]
    return new

def main():
    ssize = 500
    popn = np.random.choice(a = [0,1,2,3],size = (ssize,ssize))
    palette = []
    for i in range(256):    
        palette.extend((np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)))
    im = []
    gen = 100
    with tqdm(total=gen) as pbar:   
        for gen in range(0,gen):
            # print(gen)
            new = np.zeros_like(popn)
            popn = loop(popn,new, ssize)
            im.append(Image.fromarray(popn).convert('P'))
            pbar.update(1)
    im[0].save('z.gif', save_all=True, append_images=im[1:],
           optimize=False, duration=3, loop=True, palette = palette)
    return 

main()