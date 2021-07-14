import numpy as np
import matplotlib.pyplot as plt
import argparse

def generate_data(total_time=1, time_interval=0.01, mass=1, density=1, c=1, h_bar=1, mean=0, derivation=0.3, g_e=1, use_noise=True):
    domain = np.arange(0, total_time, time_interval)
    num_points = len(domain)

    if mass == 0:
        factor = np.sqrt(2*density / (c*c)) * h_bar / (c*c)
    else:
        factor = np.sqrt(2*density / (c*c)) * h_bar / (c*c* mass)

    phi = np.array([factor * np.cos(mass * c*c * t / h_bar) for t in domain])
    phi *= g_e

    if use_noise:
        noise = np.random.normal(mean, derivation, num_points)
        phi += noise

    return(phi)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sample data.')
    parser.add_argument('-total_time', metavar='t', type=float, help='timespan of signal', default=100)
    parser.add_argument('-time_interval', metavar='dt', type=float, help='time interval between points, default: 0.1', default=0.1)
    parser.add_argument('-mass', metavar='m', type=float, help='mass of dark matter particles, default: 1 \n(make it 0 for no oscillation)', default=1)
    parser.add_argument('-density', metavar='rho', type=float, help='density of dark matter here, default: 1', default=1)
    parser.add_argument('-c', metavar='c', type=float, help='light speed, default: 1', default=1)
    parser.add_argument('-h_bar', metavar='h_bar', type=float, help='h_bar, default: 1', default=1)
    parser.add_argument('-mean', metavar='phi', type=float, help='mean of gaussian distribution for noise, default: 0', default=0)
    parser.add_argument('-derivation', metavar='sigma', type=float, help='derivation of gaussian distribution for noise, default: 0.3', default=0.3)
    parser.add_argument('-g_e', metavar='g_e', type=float, help='g_e in formula, default: 1', default=1)
    parser.add_argument('-no_noise', action='store_true', default=False, help='toggle noise')
    args = parser.parse_args()

    args.time_interval = 1/args.time_interval

    phi = generate_data(total_time=args.total_time, time_interval=args.time_interval, mass=args.mass, density=args.density, c=args.c, h_bar=args.h_bar, mean=args.mean, derivation=args.derivation, g_e=args.g_e, use_noise=(not args.no_noise))
    print(phi)
