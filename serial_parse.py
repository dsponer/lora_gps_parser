import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ruh_m = plt.imread('map.png')
BBox = (131.8797, 131.9089, 43.0373, 43.0227)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title('Plotting Spatial Data on Riyadh Map')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(ruh_m, zorder=0, extent=BBox, aspect='equal')
plt.show()
