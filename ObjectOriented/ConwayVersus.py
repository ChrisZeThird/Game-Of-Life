# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 16:44:28 2022

@author: ChrisZeThird
"""
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.widgets import Button
import matplotlib.animation as animation
from matplotlib.artist import Artist
import matplotlib.cm as cm

import ConwayClassic as cc

""" Classes """

class Versus():
    
    """ 1v1 gamemode adaptation of Conway's Game of Life. 2 players face each other, with two different colors. The game
        follows the same rules but instead of one type of cell we have two. The game ends when only one type of cell
        remains on the board. Again the only argument to pass is the size of the board"""
    
    def __init__(self,N,nbr):
        ## Initialize data set
        self.N = N
        self.data = np.zeros((self.N,self.N))
        
        ## Set the maximum number of cells a player can place
        self.nbr = nbr
        
        ## Initial count of player 1 and player 2 cells
        self.count_p1 = 0
        self.count_p2 = 0
        
        ## Defines the cmap to use to create two cell colours, 0 and 1 are still black and white
        self.cmap = 'CMRmap'
        self.p1 = 0.2 # player 1 colour 
        self.p2 = 0.5 # player 2 colour
        
        self.c1 = cm.CMRmap(self.p1) # retrieve actual color code from decimal value for player 1
        self.c2 = cm.CMRmap(self.p2) # retrieve actual color code from decimal value for player 2 
        
        ## Initialize figure (we call the initFig class to avoid repetition between gamemodes)
        init_figure = cc.initFig(self.N)
        init_figure.init()
        self.fig = init_figure.fig
        self.ax = init_figure.ax
        self.fig.suptitle(f'Each player has {self.nbr} cells to place', fontsize=20, fontname='Helvetica')
        
        self.textvar = self.fig.text(0,0,'') # useful for later, when displaying winner
        self.textvar.set_visible(False)
        
        ## Draw initial configuration
        self.img = self.ax.imshow(self.data, cmap='CMRmap', extent=[0, self.N, 0, self.N], vmin=0, vmax=1)
        
        ## Start animation button placement
        self.axes_start = plt.axes([0.7, 0.6, 0.1, 0.075])
        self.start_button = Button(self.axes_start, 'Start',color='palegreen', hovercolor='lime')
        
        ## Reset grid button placement
        self.axes_reset = plt.axes([0.81, 0.6, 0.1, 0.075])
        self.reset_button = Button(self.axes_reset, 'Reset',color='moccasin', hovercolor='gold')
        
        ## Player 1 selection button placement
        self.axes_p1 = plt.axes([0.7, 0.4, 0.1, 0.075])
        self.p1_button = Button(self.axes_p1, 'Player 1',color='royalblue', hovercolor=self.c1)
        
        ## Player 2 selection button placement
        self.axes_p2 = plt.axes([0.81, 0.4, 0.1, 0.075])
        self.p2_button = Button(self.axes_p2, 'Player 2',color='darksalmon', hovercolor=self.c2)
        
        ## Exit button placement
        self.axes_exit = plt.axes([0.755, 0.2, 0.1, 0.075])
        self.exit_button = Button(self.axes_exit, 'Exit',color='lightcoral', hovercolor='firebrick')
        
        ## Set the initial player to play
        self.current_player = 'P1'
        
        ## Connect buttons to functions
        self.start_button.on_clicked(self.start_game) # start the animation on click
        self.reset_button.on_clicked(self.reset)

        self.p1_button.on_clicked(self.select_p1)
        self.p2_button.on_clicked(self.select_p2)

        self.exit_button.on_clicked(self.escape)

        ## Create interactivity to click on plot to turn on cells
        self.fig.canvas.mpl_connect('button_press_event', self.turn_on) # connect cells management to figure
    
    """ Rules of the Game """
    def rule(self,p,q,total1,total2):
        """ We suppose p and q different. And we look at a cell with value p
            Returns the new value of the cell for fixed indexes.""" 
            
        if ((abs(total1 - total2) == 2) or (abs(total1 - total2) == 3)):
            return p
        
        # elif ((total1 == 3) and ((total1 < 2) or (total2 > 3))):
        #     return p
        
        # elif (((total1 > 3) or (total1 < 2)) and ((total2 > 3)) or (total2 < 2)):
        #     return 0
        
        # elif (((total1 > 3) or (total1 < 2)) and (total2 == 3)):
        #     return q
        
        elif ((abs(total1 - total2) == 1) and (total1 > 1)):
            return p
        
        else:
            return 0
            
    
    def get_neighbors(self, grid, i, j):
        
        N = self.N
        
        North = grid[(i-1), j] if (i > 0) else None
        S = grid[(i+1), j] if (i < N - 1) else None
        W = grid[i, (j-1)]  if ((j > 0)) else None
        E = grid[i, (j+1)] if (j < N - 1) else None
        
        NW = grid[(i-1), (j-1)] if (i > 0 and j > 0) else None
        NE = grid[(i-1), (j+1)] if (i > 0 and j < N - 1) else None
        SW = grid[(i+1), (j-1)] if (i < N - 1 and j > 0) else None
        SE = grid[(i+1), (j+1)] if (i < N - 1 and j < N - 1) else None
        
        neighbors = [North, S, W, E, NW, NE, SW, SE]
        
        return [x for x in neighbors if x is not None]
    
    def update(self,grid):
     
        ## Copy grid since we require 8 neighbors for calculation and we go cell by cell
        newGrid = grid.copy()
        N = self.N
        p1 = self.p1
        p2 = self.p2
        for i in range(N):
            for j in range(N):
                ## Apply adapated Conway's rules
                # total1 = np.count_nonzero((grid[(i-1)%N:(i+1)%N + 1,(j-1)%N:(j+1)%N + 1]) == p1) # doesn't work as intended
                # total2 = np.count_nonzero((grid[(i-1)%N:(i+1)%N + 1,(j-1)%N:(j+1)%N + 1]) == p2)
                
                #total = grid[i%N, (j-1)%N] + grid[i%N, (j+1)%N] + grid[(i-1)%N, j%N] + grid[(i+1)%N, j%N] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                # idea : list(np.argwhere(arr==p))
                
                neighbors = self.get_neighbors(grid,i,j)
                # print('neighbors: ', neighbors)
                total1 = sum((x==p1) for x in neighbors)
                total2 = sum((x==p2) for x in neighbors)
                
                if grid[i,j] != 0:
                    if grid[i,j] == p1:
                        newGrid[i,j] = self.rule(p1, p2, total1, total2)
                        
                    elif grid[i,j] == p2:
                        newGrid[i,j] = self.rule(p2, p1, total2, total1)
                    
                else:
                    if ((total1 == 3) and (total2 != 3)):
                        newGrid[i,j] = p1
                    
                    elif ((total1 != 3) and (total2 == 3)):
                        newGrid[i,j] = p2
                    
                    elif ((total1 == 3) and (total2 == 3)):
                        p = np.random.choice([self.p1,self.p2])
                        newGrid[i,j] = p
                    
        ## Updated data
        self.data = newGrid
        ## Updated image
        (self.img).set_data(self.data)
        # print('updated')
    
    """ Defining button press events """
    
    ## Allows the user to select cells to setup the initial configuration
    def turn_on(self,event):
        gx = event.xdata # x coordinate of the mouse
        gy = event.ydata # y coordinate of the mouse
        
        self.count_p1 = np.count_nonzero(self.data == self.p1)
        self.count_p2 = np.count_nonzero(self.data == self.p2)
        
        # mouse coordinate (x,y) correspond to array indexes [i,j] with i = N-1 - y and j = x
        i = self.N - 1 - int(gy) 
        j = int(gx) 
        if self.data[i,j] == 0:
            if (self.current_player == 'P1') and (self.count_p1 < (self.nbr + 1)): # checks if player 1 reaches max cell number
                self.data[i,j] = self.p1 # on click, turns cell on for player 1
            elif (self.current_player == 'P2') and (self.count_p2 < (self.nbr + 1)): # checks if player 2 reaches max cell number
                self.data[i,j] = self.p2 # on click, turns cell on for player 2
                
        else:
            if (self.current_player == 'P1') and (self.data[i,j] == self.p1) :
                self.data[i,j] = 0 # on click, turns cell off if it was on already, for player 1
                self.count_p1 -= 1 # substract cell from total cells count of player 1
            
            elif (self.current_player == 'P2') and (self.data[i,j] == self.p2):
                self.data[i,j] = 0 # on click, turns cell off if it was on already, for player 2
                self.count_p2 -= 1 # substract cell from total cells count of player 2
                
        self.img.set_data(self.data) # update the imshow 
        self.fig.canvas.draw_idle()
      
    ## Lets the user exit the figure
    def escape(self,event):
        plt.close()
        
    ## On click, reset the plot with all zeros array
    def reset(self,event):
        self.data = np.zeros((self.N,self.N)) # reset the array to all zeros
        
        (self.img).set_data(self.data)
        # self.ax_title_visible = False # useful for later, when displaying winner
        # self.fig.canvas.draw_idle()

        self.count_p1 = 0
        self.count_p2 = 0
        
        Artist.remove(self.textvar)
        
    ## Starts the animation of the game

    def start_game(self,event):
        self.ani = animation.FuncAnimation(self.fig, self._update, interval=100, save_count=60)
    
    def _update(self,frame):
        
        previous_count_p1 = np.count_nonzero(self.data == self.p1)
        previous_count_p2 = np.count_nonzero(self.data == self.p2)
        self.update(self.data)
        
        self.count_p1 = np.count_nonzero(self.data == self.p1)
        self.count_p2 = np.count_nonzero(self.data == self.p2)
        
        if (self.count_p1 == 0) and (self.count_p2 != 0):
            self.ani.event_source.stop()
            self.textvar = self.fig.text(0.5, 0.05, 'PLAYER 2 WINS!', color=self.c2, ha='center', fontsize=25, fontweight='bold')
        
        elif (self.count_p1 != 0) and (self.count_p2 == 0):
            self.ani.event_source.stop()
            self.textvar = self.fig.text(0.5, 0.05, 'PLAYER 1 WINS!', color=self.c1, ha='center', fontsize=25, fontweight='bold')
        
        elif (self.count_p1 == 0) and (self.count_p2 == 0):
            self.ani.event_source.stop()
            self.textvar.set_visible(True)
            self.textvar = self.fig.text(0.5, 0.05, 'DRAW!', color=cm.CMRmap(0.4), ha='center', fontsize=25, fontweight='bold')
        
        elif (self.count_p1 == previous_count_p1) and (self.count_p2 == previous_count_p2):
            self.ani.event_source.stop()
            self.textvar = self.fig.text(0.5, 0.05, 'DRAW!', color=cm.CMRmap(0.4), ha='center', fontsize=25, fontweight='bold')
        
    ## Select player turn to set cells
    def select_p1(self,event):
        self.current_player = 'P1'
    
    def select_p2(self,event):
        self.current_player = 'P2'