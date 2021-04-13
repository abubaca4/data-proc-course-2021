import PySimpleGUI as sg

import numpy as np
import scipy.stats

def make_row(N, mu, sigma2):
    row = np.random.normal(size=int(N), loc=mu, scale=sigma2 ** .5)
    return row

def check_5(row1, row2, alpha):
    result = ""
    N = len(row1)
    M = len(row2)
    mean1 = np.mean(row1)
    mean2 = np.mean(row2)

    S1 = np.mean(np.square(row1 - mean1))
    S2 = np.mean(np.square(row2 - mean2))
    S = ((N - 1) * S1 + (M - 1) * S2) / (M + N + 2)
    s = np.sqrt(S)

    tau = scipy.stats.t.ppf(1- alpha / 2, N + M - 2)

    Z = np.abs(mean1 - mean2) / s * np.sqrt((M * N) / (M + N))
    result += "Z = {:.2f}".format(Z) + "\n"
    result += "tau = {:.2f}".format(tau) + "\n"
    return (Z <= tau, result)

num_row1 = []
num_row2 = []

