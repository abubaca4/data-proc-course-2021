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

    tau = scipy.stats.t.ppf(1 - alpha / 2, N + M - 2)

    Z = np.abs(mean1 - mean2) / s * np.sqrt((M * N) / (M + N))
    result += "Z = {:.2f}".format(Z) + "\n"
    result += "tau = {:.2f}".format(tau) + "\n"
    return (Z <= tau, result)


num_row1 = []
num_row2 = []

layout = [
    [sg.Text('N:'), sg.InputText('100', key='N'),
     sg.Text('N:'), sg.InputText('100', key='N_2')],
    [sg.Text('μ:'), sg.InputText('0', key='μ'),
     sg.Text('μ:'), sg.InputText('0', key='μ_2')],
    [sg.Text('σ²:'), sg.InputText('1', key='σ²')],
    [sg.Submit("Сгенерировать выборку 1"),
     sg.Submit("Сгенерировать выборку 2")],
    [sg.Text('Параметры распределения 1'),
     sg.Text('Параметры распределения 2')],
    [sg.Output(size=(48, 10), key='out_0'),
     sg.Output(size=(48, 10), key='out_1')],
    [sg.Text('Данные для проверки')],
    [sg.Text('α:'), sg.InputText('0.05', key='α')],
    [sg.Submit("Проверить гипотезы")],
    [sg.Output(size=(48, 10), key='out_2')],
]

window = sg.Window('Lab 3_2', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать выборку 1':
        num_row1 = make_row(int(values["N"]), float(
            values["μ"]), float(values["σ²"]))
        window["out_0"].update("\n".join(list(map(str, num_row1[:10]))))
    if event == 'Сгенерировать выборку 2':
        num_row2 = make_row(int(values["N_2"]), float(
            values["μ_2"]), float(values["σ²"]))
        window["out_1"].update("\n".join(list(map(str, num_row2[:10]))))
    if event == 'Проверить гипотезы':
        result = ""
        if (len(num_row1) < 1 or len(num_row2) < 1):
            result = 'Пожалуйста сначала сгенерируйте выборки'
        else:
            result += 'Гипотеза о равенстве математических ожиданий при неизвестных дисперсиях:' + '\n'
            temp = check_5(num_row1, num_row2, float(values['α']))
            result += temp[1] + '\n'
            if temp[0]:
                result += "Выполняется гипотеза H0"
            else:
                result += "Выполняется гипотеза H1"
        window["out_2"].update(result)


window.close()
