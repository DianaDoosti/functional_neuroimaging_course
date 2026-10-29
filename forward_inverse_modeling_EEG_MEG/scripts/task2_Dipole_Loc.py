import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math 
import random
from pathlib import Path

try:
    from .utility_functions import sort_point, Conv_coordinates
except ImportError:
    from utility_functions import sort_point, Conv_coordinates

# -------------------------------------  Calculate Coordinates of Diapole  ------------------------------------------
# Define the number of dipole sources to generate
num_points = 104

# Initialize a random number generator with the default algorithm
rng = random.Random() 

# Generate random theta values (polar angle) between 0 and π
theta = [rng.uniform(0, math.pi) for _ in range(num_points)]

# Generate random phi values (azimuthal angle) between 0 and 2π
phi = [rng.uniform(0, 2*math.pi) for _ in range(num_points)]

radius = 0.07  # radius of the sphere in meters

# Convert spherical coordinates to Cartesian coordinates using utility_functions
x, y, z = Conv_coordinates(phi, theta, radius)

# Sort the dipole coordinates based on distance from z-axis
x_sorted, y_sorted, z_sorted = sort_point(x, y, z)

# Concatenate the coordinates into a single array
rq = np.stack((x_sorted, y_sorted, z_sorted), axis=1)

# Define the new dipole 
theta = np.radians(45)
phi = np.radians(45)

x_0, y_0, z_0 = Conv_coordinates(phi, theta, radius)
rq_0 = np.array([x_0, y_0, z_0])

q_0 = np.array([0, 0, 1]) # Define the orientation vector for the new dipole

# Append the new dipole position to the existing coordinates
rq = np.vstack((rq, rq_0)) 

# Save the dipole coordinates to a file for later use
data_dir = Path(__file__).resolve().parent.parent / "data"

np.savez(data_dir / "Dipole_coordinates.npz", x=rq[:,0], y=rq[:,1], z=rq[:,2], rq=rq)

# -------------------------------------  Visiualize Diapole  ------------------------------------------

def plot_sphere(ax, radius):
    # Plot a semi-transparent sphere on a 3D axis.
    
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x_s = radius * np.outer(np.cos(u), np.sin(v))
    y_s = radius * np.outer(np.sin(u), np.sin(v))
    z_s = radius * np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x_s, y_s, z_s, color='r', alpha=0.3)


def visualize_dipole(x, y, z, q_0, radius,  ax=None):
    # Visualize dipoles inside the sphere.
    
    # Create a new figure only if no axis is provided
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
    ax.set_title('Random Generated Dipole')

    # Configure 3D axes
    ax.set_box_aspect([1, 1, 1])

    for set_lim, set_ticks in [
        (ax.set_xlim, ax.set_xticks),
        (ax.set_ylim, ax.set_yticks),
        (ax.set_zlim, ax.set_zticks)
    ]:
        set_lim([-0.08, 0.08])
        set_ticks(np.arange(-0.08, 0.08, 0.04))

    # Plot sensor positions and labels
    ax.scatter(x, y, z, color='b')

    for i, (xi, yi, zi) in enumerate(zip(x, y, z)):
        ax.text(xi, yi, zi, str(i + 1), color='black', fontsize=9)
        

    ax.quiver(x[104], y[104], z[104], q_0[0], q_0[1], q_0[2], color='r', length=0.03,
          normalize=True, arrow_length_ratio=0.5)

    # Plot sphere
    plot_sphere(ax, radius)

    # Axis labels
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    return ax
