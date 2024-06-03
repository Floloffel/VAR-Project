'''
Script contains function to plot cube edges on a sphere. 
Plotted will be in 2D Plane with Azimuth [-1 to 1] and Elevation [-0.5 to 0.5]

Script can be imported or executed as stand alone.

Keyword arguments:
- aplha
- number of points per plotted edge

author:
f.ulbricht@campus.tu-berlin.de

date: 
03.06.2024
'''



import matplotlib.pyplot as plt
import numpy as np
from TS_TH_from_sphere_vector import y_bottom, y_top


def plot_square_to_cube(alpha=0.4, n_points=30):
    x_offsets_middle = np.array([-0.75, -0.25, 0.25])
    for x_offset in x_offsets_middle:
        x_array = np.linspace(x_offset, x_offset+0.5, n_points)

        plt.plot(x_array, (y_bottom(x_array, x_offset)), c='black', alpha=alpha)
        plt.plot(x_array, (y_top(x_array, x_offset)), c='black', alpha=alpha)


    x_back_west = np.linspace(-1, -0.75, int(n_points/2))
    x_back_east = np.linspace(0.75, 1, int(n_points/2))

    for x_array, x_offset in zip([x_back_west, x_back_east],[-1.25, 0.75]):
        plt.plot(x_array, (y_bottom(x_array, x_offset)), c='black', alpha=alpha)
        plt.plot(x_array, (y_top(x_array, x_offset)), c='black', alpha=alpha)


    verticals = np.array([-0.75, -0.25, 0.25, 0.75])

    for x_vertical in verticals:
        y_array = np.linspace(y_bottom(x_vertical, x_vertical), y_top(x_vertical, x_vertical), n_points)
        x_array = np.ones(y_array.shape) * x_vertical
        plt.plot(x_array, y_array, c='black', alpha=alpha)


if __name__ == "__main__":
    
    plt.figure()
    plot_square_to_cube()
    plt.axvline(0)
    plt.axhline(0)
    plt.xlim(-1, 1)
    plt.ylim(-0.5, 0.5)
    plt.title("Cube edges interpolated on sphere")
    plt.xlabel("Azimuth in rad")
    plt.ylabel("Elevation in rad")
    plt.show()

