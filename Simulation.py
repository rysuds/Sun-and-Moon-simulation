import random as rand
import numpy as np
import matplotlib.pyplot as plt
from Player import Player

class Simulation():
    '''
        This class creates the simualtion in which the players' positions
        evolve with respect to each other
    '''
    def __init__(self,N=5,num_players=5,seed=20,players={}):
        self.N = N
        self.num_players = num_players
        self.players = players
        self.adjacency = {}
        self.step = N*0.1 #movement increment of player
        self.history = [] #list of list of coords, corresponds to timesteps
        self.centers = [] #center at every step
        rand.seed(seed)

        #initialize all players/partners
        self.generate_players()
        self.add_all_partners()

    def get_iterations(self):
        return len(self.history)

    def generate_players(self):
        N = self.N
        if len(self.players) > 0:
            self.players = {}

        for i in range(self.num_players):
            #modularize this to customize player placement, currently only supports random placement
            x_coord, y_coord = round(rand.uniform(-N,N),2), round(rand.uniform(-N,N),2)
            self.players[i] = Player(x=x_coord,y=y_coord)

    def add_all_partners(self):
        if len(self.players) < self.num_players:
            self.generate_players()
        #print(self.players)
        for key,player in self.players.items():
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
            self.adjacency[key] = player.partners

    def get_tups(self,array=True):
        tups = []
        for player in self.players.values():
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
            old = new
            for player in self.players.values():
                player.update_position(player_dict = self.players, bound=self.N)

            self.history.append(self.get_tups(array=False))
            self.centers.append(self.get_center)

            new = self.get_tups()
            convergence = self.get_step_diffs(old,new)

        #print(f'Number of Iterations:{len(self.history)}')
        if plot:
            self.plotter()

    def run_live_plot(self,lim = 0.1):
        #Plots the graphs step by step, rather than from a list of snapshots
        self.generate_players()
        self.add_all_partners()
        old, new = np.zeros((self.num_players,2)), self.get_tups()
        convergence = self.get_step_diffs(old,new)

        fig, ax = plt.subplots()
        x_0, y_0 = zip(*self.get_tups(array=False))
        c1, c2 = self.get_center()
        points, = ax.plot(x_0,y_0,marker = 'o',linestyle = 'None')
        centers, = ax.plot(c1,c2,marker = 'o',linestyle = 'None',color='r')
        i = 0
        while convergence > lim:
            i +=1
            old = new
            for player in self.players.values():
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