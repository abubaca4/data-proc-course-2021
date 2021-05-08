import PySimpleGUI as sg

import numpy as np
import scipy.stats


def generate_ints(n):
    result = np.sort(np.random.uniform(size=n))
    return (result, np.array2string(result))


def pirson(row, alpha, m):
    if m == 0:
        m = int(1 + np.floor(3.22 * np.log10(len(row))))
    min = np.min(row)
    max = np.max(row)
    h = (max - min) / m
    delta_sum = 0
    for i in range(m):
        n = np.sum((row >= min + h * i) & (row <= min + h * (i + 1)))
        p = scipy.stats.uniform.cdf(
            min + h * (i + 1)) - scipy.stats.uniform.cdf(min + h * i)
        delta = (n - len(row) * p) ** 2 / (len(row) * p)
        delta_sum += delta

    text = ''
    tau = scipy.stats.poisson.ppf(1 - alpha / 2, m - 1)
    text += "δ = {:.2f}".format(delta_sum) + "\n"
    text += "τ = {:.2f}".format(tau) + "\n"
    return (np.abs(delta_sum) <= tau, text)


def Dnp(x):
    return np.max([np.abs(i / len(x) - x[i - 1]) for i in range(1, len(x) + 1)])


def Dnm(x):
    return np.max([np.abs(x[i - 1] - (i - 1) / len(x)) for i in range(1, len(x) + 1)])


def Dn(x):
    dnp = Dnp(x)
    dnm = Dnm(x)
    return np.max([dnp, dnm])


def Dn_alpha(n, alpha):
    return np.sqrt(1 / (2 * n) * np.log(2 / (1 - alpha)))


def kolmogorov(row, alpha, m):
    dna = Dn_alpha(m, alpha)
    dn = Dn(row)
    text = ''
    text += "D_n = " + str(dn) + "\n"
    text += "D_n (α) = " + str(dna) + "\n"
    return (dn <= dna, text)


layout = [
    [sg.Text('N:'), sg.InputText('10', key='N')],
    [sg.Text('α:'), sg.InputText('0.05', key='α')],
    [sg.Submit("Сгенерировать и проверить")],
    [sg.Output(size=(48, 10), key='out')],
]

window = sg.Window('Сравнение критериев Пирсона и Колмогорова', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать и проверить':
        text = ''
        num_row = generate_ints(int(values["N"]))
        p = pirson(num_row[0], float(values["α"]), int(values["N"]))
        k = kolmogorov(num_row[0], float(values["α"]), int(values["N"]))
        text += p[1]
        text += k[1]
        text += "Пирсон: " + ("H0" if p[0] else "H1") + "\n"
        text += "Колмогоров: " + ("H0" if k[0] else "H1") + "\n"
        text += "\n"
        text += num_row[1]
        window["out"].update(text)

window.close()
