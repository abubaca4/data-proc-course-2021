import PySimpleGUI as sg

import numpy as np


def generate_ints(n):
    result = np.sort(np.random.uniform(size=n))
    return (result, np.array2string(result))


def Dnp(x):
    return np.max([np.abs(i / len(x) - x[i - 1]) for i in range(1, len(x) + 1)])


def Dnm(x):
    return np.max([np.abs(x[i - 1] - (i - 1) / len(x)) for i in range(1, len(x) + 1)])


def Dn_alpha(n, alpha):
    return np.sqrt(1 / (2 * n) * np.log(2 / (1 - alpha)))


def Dn(x):
    dnp = Dnp(x)
    dnm = Dnm(x)
    text = ""
    text += "D_n^+ = " + str(dnp) + "\n"
    text += "D_n^- = " + str(dnm) + "\n"
    return (np.max([dnp, dnm]), text)


layout = [
    [sg.Text('N:'), sg.InputText('10', key='N')],
    [sg.Text('α:'), sg.InputText('0.05', key='α')],
    [sg.Submit("Сгенерировать и проверить")],
    [sg.Output(size=(48, 10), key='out')],
]

window = sg.Window('Lab 4', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать и проверить':
        text = ''
        num_row = generate_ints(int(values["N"]))
        dna = Dn_alpha(int(values["N"]), float(values["α"]))
        dn = Dn(num_row[0])
        text += dn[1]
        text += "D_n = " + str(dn[0]) + "\n"
        text += "D_n (α) = " + str(dna) + "\n"
        if dn[0] <= dna:
            text += "Выполняется гипотеза H0" + "\n"
        else:
            text += "Выполняется гипотеза H1" + "\n"
        text += "\n"
        text += num_row[1]
        window["out"].update(text)


window.close()
