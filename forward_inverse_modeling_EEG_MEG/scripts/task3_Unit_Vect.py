import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pathlib import Path


# -------------------------------------  Calculate Coordinates of Unit Vector ------------------------------------------

# Load the sensor coordinates from the previously saved file
data_dir = Path(__file__).resolve().parent.parent / "data"

data = np.load(data_dir / "sensor_coordinates.npz")
x = data['x']
y = data['y']
z = data['z']
radius = 0.09

# Initialize arrays for unit vector components
ex = np.zeros(33)
ey = np.zeros(33)
ez = np.zeros(33)
print(ex.shape)  # Should output (33,)

# Calculate unit vectors for each sensor
for i in range(33):
    # Calculate the magnitude of the position vector 
    mag = np.sqrt(x[i]**2 + y[i]**2 + z[i]**2)   
    # Normalize each component by dividing by the magnitude
    ex[i] = x[i] / mag
    ey[i] = y[i] / mag
    ez[i] = z[i] / mag

# Save the unit vector components to a file for later use
np.savez(data_dir / "Unit_Vect_coordinates.npz", ex=ex, ey=ey, ez=ez)


# -------------------------------------  Visiualize Unit Vector ---------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


def plot_hemisphere(ax, radius):
    # Plot a semi-transparent hemisphere on a 3D axis.

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi / 2, 100)

    x_h = radius * np.outer(np.cos(u), np.sin(v))
    y_h = radius * np.outer(np.sin(u), np.sin(v))
    z_h = radius * np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x_h, y_h, z_h, color='y', alpha=0.4)


def visualize_sensors_unit_vectors(x, y, z, ex, ey, ez, radius, ax=None):

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    ax.set_title('Visualize Unit Vector')

    # Configure 3D axes
    ax.set_box_aspect([1, 1, 1])

    for set_lim, set_ticks in [
        (ax.set_xlim, ax.set_xticks),
        (ax.set_ylim, ax.set_yticks),
        (ax.set_zlim, ax.set_zticks)
    ]:
        set_lim([-0.11, 0.11])
        set_ticks(np.arange(-0.1, 0.1, 0.04))

    # Plot sensor positions and labels
    ax.scatter(x, y, z, color='b')

    for i, (xi, yi, zi) in enumerate(zip(x, y, z)):
        ax.text(xi, yi, zi, str(i + 1), color='black', fontsize=8)

    # Plot unit vectors
    ax.quiver(
        x, y, z, ex, ey, ez,
        color='r',
        length=0.015,
        normalize=True,
        arrow_length_ratio=0.5
    )

    # Plot hemisphere
    plot_hemisphere(ax, radius)

    # Axis labels
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    return ax
