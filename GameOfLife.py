
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 10:50:50 2022

@author: ChrisZeThird

Special thanks to ConfusedReptile#6830 on discord for their help on the animation setup.
"""
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.widgets import Button
import matplotlib.animation as animation

""" Rules of the Game of Life """

def update(grid):
 
    # Copy grid since we require 8 neighbors for calculation and we go cell by cell
    newGrid = grid.copy()
    N,_ = np.shape(grid)
    for i in range(N):
        for j in range(N):
            total = grid[i%N, (j-1)%N] + grid[i%N, (j+1)%N] + grid[(i-1)%N, j%N] + grid[(i+1)%N, j%N] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
 
            # Applies Conway's rules
            if grid[i, j]  == 1:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 1
 
    # Updated data
    global data
    data = newGrid
    # Updated image
    global img
    img.set_data(data)

""" Setting initial distribution """

# Size of the grid
N = 30

# Make an empty data set
data = np.zeros((N, N)) 

""" Figure setup """

global fig
fig = plt.figure()
global ax
ax = fig.subplots()
plt.subplots_adjust(right = 0.25)

# Draw a grid layout to see the cell more clearly
for x in range(N + 1):
    ax.axhline(x, lw=2, color='w', zorder=5)
    ax.axvline(x, lw=2, color='w', zorder=5)
    
# Turn off the axis labels
ax.axis('off')
plt.tight_layout(pad=4)
 
# Plot the initial empty distribution
global img
img = ax.imshow(data, cmap='gray', extent=[0, N, 0, N], vmin=0, vmax=1)

""" Buttons positioning """

# Reset button placement
axes_exit = plt.axes([0.755, 0.2, 0.1, 0.075])
exit_button = Button(axes_exit, 'Exit',color='lightcoral', hovercolor='firebrick')

# Reset grid button placement
axes_reset = plt.axes([0.7, 0.4, 0.1, 0.075])
reset_button = Button(axes_reset, 'Reset',color='sandybrown', hovercolor='orangered')

# Random distribution button placement
axes_random = plt.axes([0.81, 0.4, 0.1, 0.075])
random_button = Button(axes_random, 'Randomize', color='lightblue', hovercolor='darkblue')

# Start animation button placement
axes_start = plt.axes([0.7, 0.6, 0.1, 0.075])
start_button = Button(axes_start, 'Start',color='palegreen', hovercolor='lime')

# Pause animation button placement
axes_pause = plt.axes([0.81, 0.6, 0.1, 0.075])
pause_button = Button(axes_pause, 'Pause',color='navajowhite', hovercolor='gold')

""" Defining button press events """

# Allow the user to select cells to setup the initial configuration
def turn_on(event):
    gx = event.xdata # x coordinate of the mouse
    gy = event.ydata # y coordinate of the mouse
    
    # mouse coordinate (x,y) correspond to array indexes [i,j] with i = N-1 - y and j = x
    i = N - 1 - int(gy) 
    j = int(gx) 
    if data[i,j] == 0:
        data[i,j] = 1 # on click, turns cell on
    else:
        data[i,j] = 0 # on click, turns cell off if it was on already
    global img
    img.set_data(data) # update the imshow 
    
    fig.canvas.draw_idle()
  
# Lets the user exit the figure
def escape(event):
    plt.close()
    
# On click, reset the plot with all zeros array
def reset(event):
    global data
    data = np.zeros((N,N)) # reset the array to all zeros
    
    global img
    img.set_data(data)
    fig.canvas.draw_idle()

# Start the animation of the game
def _update(frame):
    update(data)

def start_anim(event):
    global ani
    ani = animation.FuncAnimation(fig, _update, interval=200, save_count=50)
    # ani.save('animation3.gif')

def pause_anim(event):
    global ani
    ani.pause()
    
def random_distribution(event):
    global data
    data = np.random.randint(2, size=(N,N))
    
    global img
    img.set_data(data)
    fig.canvas.draw_idle()

""" Associate buttons with respective function """

# Connect buttons to functions
start_button.on_clicked(start_anim) # start the animation on click
pause_button.on_clicked(pause_anim)

reset_button.on_clicked(reset)
random_button.on_clicked(random_distribution)

exit_button.on_clicked(escape)

# Connect buttons to figure
fig.canvas.mpl_connect('button_press_event', turn_on) # connect cells management to figure
