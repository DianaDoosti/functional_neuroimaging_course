import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from .utility_functions import Conv_coordinates
from pathlib import Path

# -------------------------------------  Calculate Coordinates of MEG sensors ------------------------------------------

# number of MEG sensors = 33

# Define theta angles for all sensors (zenith angle)
# First sensor at zenith (0°), then 4 sensors at each of the 8 longitudinal strips

theta_degrees = [0.0]  
for i in range(8):        
    for j in range(1, 5): 
        theta_degrees.append(22.5 * j)
        
# Define phi angles for all sensors (azimuthal angle)

phi_degrees = [0.0]  # φ is arbitrary at zenith
for i in range(8):
    for j in range(1, 5):
        phi_degrees.append(45.0 * i)

       
# Convert degrees to radians for calculations
theta = np.radians(theta_degrees)
phi = np.radians(phi_degrees)

# Convert spherical coordinates to Cartesian coordinates
radius = 0.09
x, y, z = Conv_coordinates(phi, theta, radius)

print(theta_degrees)
print(phi_degrees)

# Save the calculated sensor coordinates to a file for later use

data_dir = Path(__file__).resolve().parent.parent / "data"

np.savez(data_dir / "sensor_coordinates.npz", x=x, y=y, z=z)



