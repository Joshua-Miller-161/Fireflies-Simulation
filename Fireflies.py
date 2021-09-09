import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import random
import os
from IPython import display
#====================================================================
''' Create class from which we'll make the fireflies '''
class Firefly:
    def __init__(self, x_pos, y_pos, velocity, color, phase):
        self.x_pos = x_pos       # Array to store all x positions the firefly has been in
        self.y_pos = y_pos       # '' y '' ...
        self.velocity = velocity # Array of length 3 to track the firefly's speed and direction
        self.color = color       # Array of length 3 to store RGB values for the firefly's color
        self.phase = phase       # Phase for the flashing cycle
#====================================================================
''' Generate the x and y positions for one firesly over time '''
def GetPositions(num_timesteps, max_velo):
    X = np.empty(num_timesteps, dtype=float)
    Y = np.empty(num_timesteps, dtype=float)
    X[0], Y[0] = np.random.uniform(size=2)

    velocity = np.random.uniform(-max_velo, max_velo, size=2)
    for i in range(1, num_timesteps):
        # Check if the firefly would be outside of the screen on the next move
        if (X[i-1] + velocity[0] >= 1):
            velocity[0] *= -1
        elif (X[i-1] + velocity[0] <= 0):
            velocity[0] *= -1

        if (Y[i-1] + velocity[1] >= 1):
            velocity[1] *= -1
        elif (Y[i-1] + velocity[1] <= 0):
            velocity[1] *= -1

        X[i] = X[i-1] + velocity[0]
        Y[i] = Y[i-1] + velocity[1]        

    return X, Y
#====================================================================
''' Generate the colors for each firefly '''
def SetColors(num_timesteps, FireList, period, radius, attraction):
    for t in range(num_timesteps):
        for j in range(len(FireList)):
            if (np.sin(2 * np.pi * (1 / (2 * period)) * (t + FireList[j].phase)) > 0):
                FireList[j].color[t] = np.array([255, 255, 0]) / 255

            for k in range(len(FireList)):
                if not (j == k):
                    if (Distance(FireList[j], FireList[k], t) <= radius):
                        #print('POG: x1=', FireList[j].x_pos[t], 'x2=', FireList[k].x_pos[t], 'y1=', FireList[j].y_pos[t], 'y2=', FireList[k].y_pos[t], 't=', t)
                        #FireList[j].color[t] = np.array([255, 0, 0]) / 255
                        #FireList[k].color[t] = np.array([255, 0, 0]) / 255
                        FireList[j].phase = FireList[k].phase
                        '''
                        if (FireList[j].phase < FireList[k].phase):
                            FireList[j].phase += attraction
                        elif (FireList[j].phase > FireList[k].phase):
                            FireList[j].phase -= attraction
                        else:
                            FireList[j].phase = FireList[k].phase
                        '''
#====================================================================
''' Get distance between fireflies '''
def Distance(Fire1, Fire2, t):
    return np.sqrt((Fire1.x_pos[t] - Fire2.x_pos[t])**2 + (Fire1.y_pos[t] - Fire2.y_pos[t])**2)
#====================================================================
''' Parameters for simulation '''
num_timesteps = 1000
num_bugs = 100
max_velo = .01
period = 10
radius = .05
attraction = 1
phase_var = 4
#====================================================================
''' Perform the simulation '''
FireList = []

# Get position data for all of the fireflies
for i in range(num_bugs):
    X, Y = GetPositions(num_timesteps, max_velo)
    INITIAL_COLORS = np.zeros((num_timesteps, 3))
    FireList.append(Firefly(X, Y, [0,0], INITIAL_COLORS, np.random.randint(-phase_var, phase_var)))

# Determine flashing patterns
SetColors(num_timesteps, FireList, period, radius, attraction)

Xs = np.empty((len(FireList), num_timesteps), dtype=float)
Ys = np.empty((len(FireList), num_timesteps), dtype=float)
Cs = np.empty((len(FireList), num_timesteps, 3), dtype=float)

for j in range(len(FireList)):
    Xs[j] = FireList[j].x_pos
    Ys[j] = FireList[j].y_pos
    Cs[j] = FireList[j].color
#====================================================================
fig, ax = plt.subplots()
#====================================================================
''' Create one frame of the simulation '''
def buildscatterplot(i):
    ax.clear()
    p = ax.scatter(Xs[:, i], Ys[:, i], color=Cs[:, i, :])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(.90, .95, 't='+str(i))
#====================================================================
''' Animate '''
animation = ani.FuncAnimation(fig, buildscatterplot, interval=15, save_count=num_timesteps)
plt.show()
#====================================================================
''' Save the animation '''
filename = 'Fireflies.gif'
writergif = ani.PillowWriter(fps=60)
animation.save(filename, writer=writergif)