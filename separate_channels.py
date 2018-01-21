# !/usr/bin/env python
import cv2
import numpy as np


def convert_Image(img):
    B = np.array([])
    G = np.array([])
    R = np.array([])


    b = img[:,:,0]
    b = b.reshape(b.shape[0]*b.shape[1])
    g = img[:,:,1]
    g = g.reshape(g.shape[0]*g.shape[1])
    r = img[:,:,2]
    r = r.reshape(r.shape[0]*r.shape[1])
    B = np.append(B,b)
    G = np.append(G,g)
    R = np.append(R,r)
