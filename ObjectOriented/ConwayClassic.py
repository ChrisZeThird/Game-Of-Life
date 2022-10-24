# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:58:42 2022

@author: ChrisZeThird
"""

import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.widgets import Button
import matplotlib.animation as animation
import matplotlib.cm as cm

""" Classes """

## Initialize Figure
class initFig():
    
    def __init__(self,N):
        self.N = N
    
    def init(self):
        ## Initialize figure
        self.fig = plt.figure()
        self.ax = self.fig.subplots()
        plt.subplots_adjust(right = 0.25)
        # plt.subplots_adjust(bottom = 0.2)
        self.ax.axis('off')
        plt.tight_layout(pad=4)
        
        ## Draw a grid layout to see the cells more clearly
        for x in range(self.N + 1):
            self.ax.axhline(x, lw=2, color='w', zorder=5)
            self.ax.axvline(x, lw=2, color='w', zorder=5)
        
        
# Create board for 0 player mod
class Conway():
    
    """ Conway class setup the classic configuration of the game: 0 player game with initial input configurations. Only
        requirement is a size of board N (int). """
    
    def __init__(self,N):
        ## Initialize data set
        self.N = N
        self.data = np.zeros((self.N,self.N))
        
        ## Initialize figure (we call the initFig class to avoid repetition between gamemodes)
        init_figure = initFig(self.N)
        init_figure.init()
        self.fig = init_figure.fig
        self.ax = init_figure.ax
        
        ## Draw initial configuration
        self.img = self.ax.imshow(self.data, cmap='CMRmap', extent=[0, N, 0, N], vmin=0, vmax=1)
        
        ## Exit button placement
        self.axes_exit = plt.axes([0.755, 0.2, 0.1, 0.075])
        self.exit_button = Button(self.axes_exit, 'Exit',color='lightcoral', hovercolor='firebrick')

        ## Reset grid button placement
        self.axes_reset = plt.axes([0.7, 0.4, 0.1, 0.075])
        self.reset_button = Button(self.axes_reset, 'Reset',color='moccasin', hovercolor='gold')

        ## Random distribution button placement
        self.axes_random = plt.axes([0.81, 0.4, 0.1, 0.075])
        self.random_button = Button(self.axes_random, 'Randomize', color='lightblue', hovercolor='darkblue')

        ## Start animation button placement
        self.axes_start = plt.axes([0.7, 0.6, 0.1, 0.075])
        self.start_button = Button(self.axes_start, 'Start',color='palegreen', hovercolor='lime')

        ## Pause animation button placement
        self.axes_pause = plt.axes([0.81, 0.6, 0.1, 0.075])
        self.pause_button = Button(self.axes_pause, 'Pause',color='navajowhite', hovercolor='gold')
        
        ## Connect buttons to functions
        self.start_button.on_clicked(self.start_anim) # start the animation on click
        self.pause_button.on_clicked(self.pause_anim)

        self.reset_button.on_clicked(self.reset)
        self.random_button.on_clicked(self.random_distribution)

        self.exit_button.on_clicked(self.escape)

        ## Create interactivity to click on plot to turn on cells
        self.fig.canvas.mpl_connect('button_press_event', self.turn_on) # connect cells management to figure
        
    """ Rules of the Game of Life """
    
    def update(self,grid):
     
        ## Copy grid since we require 8 neighbors for calculation and we go cell by cell
        newGrid = grid.copy()
        N = self.N
        for i in range(N):
            for j in range(N):
                total = grid[i%N, (j-1)%N] + grid[i%N, (j+1)%N] + grid[(i-1)%N, j%N] + grid[(i+1)%N, j%N] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                
                ## Apply Conway's rules
                # total = np.count_nonzero((grid[(i-1)%N:(i+2)%N,(j-1)%N:(j+2)%N]) == 1)
                if grid[i, j]  == 1:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = 0
                else:
                    if total == 3:
                        newGrid[i, j] = 1
     
        ## Updated data
        self.data = newGrid
        ## Updated image
        self.img.set_data(self.data)
    
        
    """ Defining button press events """

    ## Allows the user to select cells to setup the initial configuration
    def turn_on(self,event):
        gx = event.xdata # x coordinate of the mouse
        gy = event.ydata # y coordinate of the mouse
        
        # mouse coordinate (x,y) correspond to array indexes [i,j] with i = N-1 - y and j = x
        i = self.N - 1 - int(gy) 
        j = int(gx) 
        if self.data[i,j] == 0:
            self.data[i,j] = 1 # on click, turns cell on
        else:
            self.data[i,j] = 0 # on click, turns cell off if it was on already
        
        self.img.set_data(self.data) # update the imshow 
        
        self.fig.canvas.draw_idle()
      
    ## Lets the user exit the figure
    def escape(self,event):
        plt.close()
        
    ## On click, reset the plot with all zeros array
    def reset(self,event):
        self.data = np.zeros((self.N,self.N)) # reset the array to all zeros
        
        self.img.set_data(self.data)
        self.fig.canvas.draw_idle()

    ## Starts the animation of the game
    def _update(self,frame):
        self.update(self.data)

    def start_anim(self,event):
        self.ani = animation.FuncAnimation(self.fig, self._update, interval=200, save_count=60)
        # ani.save('animation_random.gif') # Uncomment if you want to save the animation as a gif
    
    ## Pauses the animation on click
    def pause_anim(self,event):
        self.ani.pause()
    
    ## Generate random distribution of cells
    def random_distribution(self,event):
        self.data = np.random.randint(2, size=(self.N,self.N))

        self.img.set_data(self.data)
        self.fig.canvas.draw_idle()