import argparse
from Player import Simulation

def main():
    #Divergent Examples
    ## Seed = 2, Num_players = 16, Gridsize = 10
    ####"FIXED" this by adding a 'bound' parameter to update_position,
    #### this prevents any player from exceeding the bounds by selecting the
    #### minimum of a calculated value and the bound N

    #Testing specific cases
    parser = argparse.ArgumentParser(description="Input simulation parameters")
    parser.add_argument("-N", "--grid_size",type=int, help="Size of NxN grid")
    parser.add_argument("-P", "--num_players", type=int, help="Number of points/players")
    parser.add_argument("-S", "--seed", type=int, help="Random seed")
    args = parser.parse_args()

    sim = Simulation(N=args.grid_size,num_players=args.num_players,seed=args.seed)
    sim.run_live_plot()
    '''
    sim = Simulation(N=10,num_players=8,seed=22)
    #sim.run_sim(plot=True)
    print(sim.adjacency)
    sim.run_live_plot()
    '''


main()