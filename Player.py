import math
import numpy as np
from vec import Vector
from copy import deepcopy
import random as rand
import matplotlib.pyplot as plt

class Player(Vector):
    def __init__(self,x=0.0, y=0.0):
        self.x, self.y = x,y
        self.partners = []

    def add_partner(self,partner):
        #Store key of partners
        self.partners.append(partner)

    def update_position(self,player_dict,bound=None):
        #Bound Parameter fixes the max x,y coord value to a specified value
        p1i,p2i = self.partners
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
        new_self = self + movement_vector
        if bound:
            sign = lambda a: (a>0) - (a<0)
            #lower, upper = -bound, bound
            #pairx = (self.x,new_self.x)
            #pairy = (self.y,new_self.y)

            #if abs(new_self.x)>=bound:
            #    self.x = sign(new_self.x)*bound
            #if abs(new_self.y)>=bound:
            #    self.y = sign(new_self.y)*bound

            #Upper Positive bound check
            self.x, self.y = min(new_self.x,bound),min(new_self.y,bound)

            #for pair in (pairx,pairy):
            #    s,n = pair
            #    if n <=lower:
            #        s = lower
            #    elif n >= upper:
            #        s = upper
            #    else:
            #        pass
            #self.x, self.y = new_self.x, new_self.y
        else:
            self.x, self.y = new_self.x, new_self.y

class Simulation():
    def __init__(self,N=5,num_players=5,seed=20,players={}):
        self.N = N
        self.num_players = num_players
        self.players = players
        self.history = [] #list of list of coords, corresponds to timesteps
        self.centers = [] #center at every step
        rand.seed(seed)

    def get_iterations(self):
        return len(self.history)

    def generate_players(self):
        N = self.N
        if len(self.players) > 0:
            self.players = {}

        for i in range(self.num_players):
            #modularize this to customize player placement
            x_coord, y_coord = round(rand.uniform(-N,N),2), round(rand.uniform(-N,N),2)
            self.players[i] = Player(x=x_coord,y=y_coord)
        print(self.players)

    def add_all_partners(self):
        if len(self.players) < self.num_players:
            self.generate_players()
        #print(self.players)
        for key,player in self.players.items():
            #tmp = deepcopy(self.players)
            #prevent self selection
            keys = list(self.players.keys())
            keys.remove(key)

            p1 = rand.choice(keys)
            #player.add_partner(self.players[p1])
            player.add_partner(p1)

            #prevent re-selection
            keys.remove(p1)
            p2 = rand.choice(keys)
            #player.add_partner(self.players[p2])
            player.add_partner(p2)


    def get_tups(self,array=True):
        tups = []
        for key,player in self.players.items():
            tups.append(player.get_coord())
        if array:
            return np.array(tups)
        else:
            return tups

    def get_center(self):
        tups = self.get_tups(array=False)
        center = tuple([sum(x)/len(tups) for x in zip(*tups)])
        return center

    def plotter(self):
        fig, ax = plt.subplots()
        hist = self.history
        x_0, y_0 = zip(*hist[0])
        points, = ax.plot(x_0,y_0,marker = 'o',linestyle = 'None')
        for i,slice in enumerate(hist[1:]):
            plt.title(f'Iteration: {i}')
            x_i, y_i = zip(*slice)
            points.set_data(x_i,y_i)
            ax.set_xlim(-self.N+1,self.N+1)
            ax.set_ylim(-self.N+1,self.N+1)
            plt.pause(0.15)
        plt.show()

    def get_step_diffs(self,old,new):
        #return average difference between coordinates of players
        #used for convergance comndition
        diff = new - old
        distances = []
        for tup in diff:
            distances.append(np.sqrt(tup[0]**2 + tup[1]**2))
        return sum(distances)/len(distances)

    def run_sim(self,lim = 0.01,plot=False):
        #create players and their partners
        self.generate_players()
        self.add_all_partners()
        old, new = np.zeros((self.num_players,2)), self.get_tups()
        convergence = self.get_step_diffs(old,new)

        self.history.append(self.get_tups(array=False))
        self.centers.append(self.get_center())
        #iter = 0
        while convergence > lim:
            #iter+=1
            #print(iter)
            old = new
            for key,player in self.players.items():
                player.update_position(player_dict = self.players, bound=self.N)

            self.history.append(self.get_tups(array=False))
            self.centers.append(self.get_center)

            new = self.get_tups()
            convergence = self.get_step_diffs(old,new)

        #print(f'Number of Iterations:{len(self.history)}')
        if plot:
            self.plotter()

    def run_live_plot(self,lim = 0.1):
        #create players and their partners
        self.generate_players()
        self.add_all_partners()
        old, new = np.zeros((self.num_players,2)), self.get_tups()
        convergence = self.get_step_diffs(old,new)

        #self.history.append(self.get_tups(array=False))
        #iter = 0

        fig, ax = plt.subplots()
        x_0, y_0 = zip(*self.get_tups(array=False))
        c1, c2 = self.get_center()
        points, = ax.plot(x_0,y_0,marker = 'o',linestyle = 'None')
        centers, = ax.plot(c1,c2,marker = 'o',linestyle = 'None',color='r')
        i = 0
        while convergence > lim:
            i +=1
            old = new
            for key, player in self.players.items():
                player.update_position(player_dict = self.players,bound=self.N)

            new = self.get_tups()
            convergence = self.get_step_diffs(old,new)

            plt.title(f'Iteration: {i}')
            x_i, y_i = zip(*self.get_tups(array=False))
            points.set_data(x_i,y_i)
            c1, c2 = self.get_center()
            centers.set_data(c1,c2)

            ax.set_xlim(-self.N+1,self.N+1)
            ax.set_ylim(-self.N+1,self.N+1)
            plt.pause(0.05)
            fig.canvas.draw()
            print(f'Iteration: {i}')
        plt.close()


def main():
    #can loop through random seeds to get different data points
    #TODO for a given seed, plot iter vs num_players
    # see if center of mass is a useful variable
    #TODO plot actual network of graph! edges correspond to neighbor, use arrows
    #for DAG, change color if both directions

    #Divergent Examples
    ## Seed = 2, Num_players = 16, Gridsize = 10
    ####"FIXED" this by adding a 'bound' parameter to update_position,
    #### this prevents any player from exceeding the bounds by selecting the
    #### minimum of a calculated value and the bound N

    '''
    range_players = range(3,300)
    seed = 2
    grid = 100
    num_players, num_iter, avg_center = [],[],[]
    for n in range_players:
        sim = Simulation(N=grid,num_players=n,seed = seed)
        sim.run_sim(plot=False)
        print(f'Num Players: {n} | Num Iterations: {len(sim.history)}')
        num_players.append(n)
        num_iter.append(len(sim.history))

    plt.figure()
    plt.title(f'Seed: {seed}')
    plt.xlabel('# Players')
    plt.ylabel('Iteration')
    #plt.xticks(rotation=45, ha='right')
    plt.plot(num_players,num_iter, color = 'b')
#plt.legend()
    plt.show()
    '''


    #Testing specific cases
    sim = Simulation(N=10,num_players=6,seed = 2)
    #sim.run_sim(plot=True)
    sim.run_live_plot()


main()
