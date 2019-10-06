import math
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
'''
Credit for base code: https://stackoverflow.com/questions/30329252/calculate-a-point-along-a-line-segment-one-unit-from-a-end-of-the-seg

'''

class Vector():
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        #self.tup = (x,y)
        #self.z = z

    def __add__(self, other):
        tmpx, tmpy = self.x, self.y
        tmpx += other.x
        tmpy += other.y
        #self.z += other.z
        return Vector(tmpx,tmpy)

    def __sub__(self, other):
        tmpx, tmpy = self.x, self.y
        tmpx -= other.x
        tmpy -= other.y
        #self.z -= other.z
        return Vector(tmpx,tmpy)

    def get_coord(self):
        return (self.x,self.y)

    def scale(self,s):
        return Vector(self.x*s,self.y*s)

    def dot(self, other):
        return float(self.x*other.x + self.y*other.y)

    def cross(self, other):
        tempX = self.y*other.z - self.z*other.y
        tempY = self.z*other.x - solf.x*other.z
        tempZ = self.x*other.y - self.y*other.x
        return Vector(tempX, tempY, tempZ)

    def dist(self, other):
        return np.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def mid(self,other):
        return Vector((self.x+other.x)/2.,(self.y+other.y)/2.)

    def unitVector(self):
        mag = self.dist(Vector())
        if mag != 0.0:
            return Vector(self.x * 1.0/mag, self.y * 1.0/mag)
        else:
            return Vector()

    def proj(self,other): #projects 'self' onto other
        #get scalars
        top = self.dot(other)
        bottom = other.dot(other)

        #scale vector down to fraction, equivalent to multiplying dot product to unit vector
        s = top/bottom
        tmp = other.scale(s)
        #tmp2 = other.unitVector().scale(top)
        return Vector(tmp.x,tmp.y)

    #def __repr__(self):
        #return str([self.x, self.y])
