import PySimpleGUI as sg

import numpy as np
import scipy.stats


def make_row(N, mu, sigma2):
    row = np.random.normal(size=int(N), loc=mu, scale=sigma2 ** .5)
    return row


def check_6(row, mu, sigma2, alpha, m):
    result = ""
    if m == 0:
        m = int(1 + np.floor(3.22 * np.log10(len(row))))
    min = np.min(row)
    max = np.max(row)
    h = (max - min) / m
    delta_sum = 0
    for i in range(m):
        n = np.sum((row >= min + h * i) & (row <= min + h * (i + 1)))
        p = scipy.stats.norm.cdf(
            min + h * (i + 1), mu, sigma2) - scipy.stats.norm.cdf(min + h * i, mu, sigma2)
        delta = (n - len(row) * p) ** 2 / (len(row) * p)
        delta_sum += delta

    tau = scipy.stats.poisson.ppf(1 - alpha / 2, m - 1)
    result += "δ = {:.2f}".format(delta_sum) + "\n"
    result += "tau = {:.2f}".format(tau) + "\n"
    return (np.abs(delta_sum) <= tau, result)


num_row = []

layout = [
    [sg.Text('Параметры распределения из которого будет генерироваться выборка')],
    [sg.Text('N:'), sg.InputText('100', key='N')],
    [sg.Text('μ:'), sg.InputText('0', key='μ')],
    [sg.Text('σ²:'), sg.InputText('1', key='σ²')],
    [sg.Submit("Сгенерировать выборку")],
    [sg.Output(size=(48, 10), key='out_0')],
    [sg.Text('Параметры распределения F1')],
    [sg.Text('μ:'), sg.InputText('0', key='μ_2')],
    [sg.Text('σ²:'), sg.InputText('1', key='σ²_2')],
    [sg.Text('Данные для проверки')],
    [sg.Text('α:'), sg.InputText('0.05', key='α')],
    [sg.Text('m(0 для подсчёта по формуле Стерджеса):'),
     sg.InputText('0', key='m')],
    [sg.Submit("Проверить гипотезы")],
    [sg.Output(size=(48, 10), key='out_1')],
]

window = sg.Window('Lab 3_3', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать выборку':
        num_row = make_row(int(values["N"]), float(
            values["μ"]), float(values["σ²"]))
        window["out_0"].update("\n".join(list(map(str, num_row[:10]))))
    if event == 'Проверить гипотезы':
        result = ""
        if len(num_row) < 1:
            result += "Пожалуйста сначала сгенерируйте выборку"
        else:
            result += 'Проверка по критерию Пирсона:' + "\n"
            temp = check_6(num_row, float(values['μ_2']), float(
                values['σ²_2']), float(values['α']), float(values['m']))
            result += temp[1]
            if temp[0]:
                result += "Выполняется гипотеза H0"
            else:
                result += "Выполняется гипотеза H1"
        window["out_1"].update(result)

window.close()
