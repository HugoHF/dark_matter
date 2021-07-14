import numpy as np
import matplotlib.pyplot as plt

def generate_data(num_points=100, mass=1, density=1, c=1, h_bar=1, mean=0, derivation=0.3, g_e=1, time_interval=10, use_noise=True):

    domain = np.array([i for i in range(num_points)]) / time_interval

    noise = np.random.normal(mean, derivation, num_points)

    if mass == 0:
        factor = np.sqrt(2*density / (c*c)) * h_bar / (c*c)
    else:
        factor = np.sqrt(2*density / (c*c)) * h_bar / (c*c* mass)

    phi = np.array([factor * np.cos(mass * c*c * t / h_bar) for t in domain])

    phi *= g_e

    if use_noise: phi += noise

    return(phi)


if __name__ == "__main__":
    phi = generate_data()
    print(phi)
