import math
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from Vector import Vector

#TODO: relate # of iterations till convergence to largest Eigenvalue of Laplacian
#TODO: use NetworkX to plot directed edges and scow actal connections to neighbors
#TODO: make command line runnable
#TODO: write functions to customize placement, ie create a square configuration with specific partners etc

class Player(Vector):
    '''
        This class defines all of the properties of the "player" or the node
        in our dynamic graph. In this model, each player has two partners, with
        some randomly generated distance (weighted edge) between them
    '''
    def __init__(self,x=0.0, y=0.0):
        self.x, self.y = x,y
        self.partners = []

    def add_partner(self,partner):
        #Store key of partners
        self.partners.append(partner)

    def update_position(self,player_dict,bound=None,step=None):
        #Bound Parameter fixes the max x,y coord value to a specified value
        p1i,p2i = self.partners[0], self.partners[1]
        p1,p2 = player_dict[p1i], player_dict[p2i]

        midpoint_vector = p1.mid(p2)
        #find closest partner
        if self.dist(p1) <= self.dist(p2):
            closest = p1
        else:
            closest = p2
        #Vector from closest to midpoint
        CM = midpoint_vector - closest
        #Vector from closest to player
        CP = self - closest
        ProjCPCM = CP.proj(CM)
        movement_vector = CM - ProjCPCM
        if step: #limit movement to step defined by simulation
            scaled = movement_vector.unitVector().scale(step)
            new_self = self + scaled
        else:
            new_self = self + movement_vector

        if bound: #limit upper bound
            self.x, self.y = min(new_self.x,bound),min(new_self.y,bound)
        else:
            self.x, self.y = new_self.x, new_self.y



