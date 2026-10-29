from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

mu = 4 * math.pi * pow(10, -7)

#  -------------------------------------  Sort points based on distance from z-axis  ------------------------------------------

def sort_point(x, y, z):
    # Calculate distance from z-axis for each point
    distances = np.sqrt(x**2 + y**2)
    sorted_indices = np.argsort(distances)
    x_sorted = x[sorted_indices]
    y_sorted = y[sorted_indices]
    z_sorted = z[sorted_indices]
    return x_sorted, y_sorted, z_sorted

#  ------------------------------- Convert spherical coordinates to Cartesian coordinates -------------------------------------
def Conv_coordinates(phi, theta, radius):

    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)
    return x, y, z

#  --------------------------------- Convert Cartesian coordinates to Polar coordinates ---------------------------------------

def cartesian_to_polar(x, y, z):
    r = np.sqrt(pow(x,2) + pow(y,2) + pow(z,2))
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    return r, theta, phi


#  ------------------------------------------ Calculate MEG Lead-Field Matrix -------------------------------------------------
def Calc_G(er, r, rq):

    numerator = np.cross(er, rq)
    denominator = np.linalg.norm(r - rq)**3

    a_ij = (mu / (4 * np.pi)) * numerator / denominator

    return a_ij

#  ------------------------------------------ Calculate EEG Lead-Field Matrix -------------------------------------------------
def d_n(n, xi, f1, f2):
    return (((n + 1) * xi + n) * (n * xi / (n + 1) + 1)
            + (1 - xi) * ((n + 1) * xi + n) * (f1 ** (2 * n + 1) - f2 ** (2 * n + 1))
            - n * (1 - xi) ** 2 * (f1 / f2) ** (2 * n + 1))


def Calc_L(theta_sensor, phi_sensor, r_dipole, theta_dipole, phi_dipole,
           R3, sg1, sg2, R1, R2, sigma):
    b = r_dipole / R3
    xi = sg2 / sg1
    f1 = R1 / R3
    f2 = R2 / R3

    # --- local frame with the dipole on the z-axis (replaces the angle subtraction) ---
    st, ct = np.sin(theta_dipole), np.cos(theta_dipole)
    sp, cp = np.sin(phi_dipole), np.cos(phi_dipole)
    zh = np.array([st * cp, st * sp, ct])        # radial direction of the dipole
    xh = np.array([ct * cp, ct * sp, -st])       # theta-hat at the dipole
    yh = np.array([-sp, cp, 0.0])                # phi-hat at the dipole
    s = np.array([np.sin(theta_sensor) * np.cos(phi_sensor),
                  np.sin(theta_sensor) * np.sin(phi_sensor),
                  np.cos(theta_sensor)])

    cos_theta = np.clip(s @ zh, -1.0, 1.0)       # true angle between dipole and sensor
    sin_theta = np.sqrt(1.0 - cos_theta ** 2)
    phi_local = np.arctan2(s @ yh, s @ xh)
    cos_phi, sin_phi = np.cos(phi_local), np.sin(phi_local)

    sum_x = sum_y = sum_z = 0.0
    for nn in range(1, 20):
        leg = np.polynomial.legendre.Legendre.basis(nn)
        Pn = leg(cos_theta)
        Pn_1 = sin_theta * leg.deriv()(cos_theta)   # P_n^1(cos θ), no Condon-Shortley phase

        dnn = d_n(nn, xi, f1, f2)
        C = (1 / (4 * np.pi * sigma * R3 ** 2)) * ((2*nn + 1) / nn) * b ** (nn - 1) \
            * ((xi * (2*nn + 1) ** 2) / (dnn * (nn + 1)))

        sum_x += C * Pn_1 * cos_phi
        sum_y += C * Pn_1 * sin_phi
        sum_z += C * nn * Pn

    # rotate the local (x', y', z') coefficients back to global x, y, z
    return sum_x * xh + sum_y * yh + sum_z * zh