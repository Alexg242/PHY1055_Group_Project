# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 03:46:00 2026

@author: alexg
"""


import matplotlib.pyplot as plt
import numpy as np
from G3_modifications import *

tau = 1#infection rate
b = 1 #birth rate
d = 1.5 #natural death rate
delta = 1.5 #death rat of infected indiviudlas

def main(n):
    n = str(n)
    n = "$S_" +n + "$"
    plt.close('all')
    coords = np.linspace(-3, 10, 101)
    H, I= np.meshgrid(coords, coords)
    dx = (b-d)*H-delta*I
    dy = tau*I*(H-I)-(delta+d)*I
    
    skip = 5
    x_skipped, y_skipped = H[::skip, ::skip], I[::skip, ::skip]  # note the indexing [start:end:skip]
    dx_skipped, dy_skipped = dx.T[::skip, ::skip], dy.T[::skip, ::skip]  # note the .T transpose method
    
    plt.figure(figsize=(6,6))
    plt.gca().set_aspect('equal', adjustable='box')  # Make plot box square
    plt.xlabel('Heatlthy Pop (H)')
    plt.ylabel('Infected Pop (I)')
    plt.title("2D Vector field of population of Healthy (H) vs Infedcted (I) rabbits"
              "\n"
              "Using Eq 1 and Eq 2 Showing "+n)
    plt.quiver(x_skipped, y_skipped, dx_skipped, dy_skipped)
    plt.streamplot(x_skipped, y_skipped, dx_skipped, dy_skipped)

    """
    plt.quiver(H, I, dx, dy)  # plot field as quiver"""
    #plt.streamplot(H, I, dx, dy, density=[0.5, 0.5])
    plt.show()


# if this is the module called directly, then execute the main function, otherwise only define it
if __name__ == '__main__':
    main(1)

#%%
tau = 0.75#infection rate
b = 1.2 #birth rate
d = 1 #natural death rate
delta = 2 #death rat of infected indiviudlas

if __name__ == '__main__':
    main(2)

#%%

tau = 1#infection rate
b = 3 #birth rate
d = 1 #natural death rate
delta = 1.5 #death rat of infected indiviudlas

if __name__ == '__main__':
    main(3)
