import PySimpleGUI as sg

import numpy as np
import scipy.stats



def make_row(N, mu, sigma2):
    row = np.random.normal(size=int(N), loc=mu, scale=sigma2 ** .5)
    return row


def check_1(row, sigma2, alpha, mu_check):
    result = ""
    N = len(row)
    mean = np.mean(row)
    n_sqrt = np.sqrt(N)
    sigma = np.sqrt(sigma2)
    u = scipy.stats.norm.ppf(1 - alpha / 2)
    Z = np.abs((mean - mu_check) / (sigma / n_sqrt))
    result += "u = {:.2f}".format(u) + "\n"
    result += "Z = {:.2f}".format(Z) + "\n"
    return (Z <= u, result)


def check_2(row, alpha, mu_check):
    result = ""
    N = len(row)
    mean = np.mean(row)
    n_sqrt = np.sqrt(N)
    tau = scipy.stats.t.ppf(1 - alpha / 2, N - 1)
    s = np.sqrt(np.mean(np.square(row - mean)))
    Z = np.abs((mean - mu_check) / (s / n_sqrt))
    result += "tau = {:.2f}".format(tau) + "\n"
    result += "Z = {:.2f}".format(Z) + "\n"
    return (Z <= tau, result)


def check_3(row, alpha, dispersion_check):
    result = ""
    N = len(row)
    mean = np.mean(row)
    n_sqrt = np.sqrt(N)
    S = np.sqrt(np.mean(np.square(row - mean)))
    z1 = scipy.stats.poisson.ppf(1 - alpha / 2, N - 1)
    z2 = scipy.stats.poisson.ppf(alpha / 2, N - 1)
    Z = N * S ** 2 / dispersion_check ** 2
    result += "Z = {:.2f}".format(Z) + "\n"
    result += "z1 = {:.2f}".format(z1) + "\n"
    result += "z2 = {:.2f}".format(z2) + "\n"

    return (Z <= z1 and Z >= z2, result)

num_row = []


def check_all(sigma2, alpha, mu_check, dispersion_check):
    h0_comp = "Выполняется гипотеза H0"
    h1_comp = "Выполняется гипотеза H1"

    result = ""
    if (len(num_row) < 1):
        result += "Пожалуйста сначала сгенерируйте выборку" + "\n"
        return result
    result += "Гипотеза о математическом ожидании при известной дисперсии:" + "\n"
    temp = check_1(num_row, sigma2, alpha, mu_check)
    result += temp[1]
    if temp[0]:
        result += h0_comp + "\n"
    else:
        result += h1_comp + "\n"
    result += "\n"

    result += "Гипотеза о математическом ожидании при неизвестной дисперсии:" + "\n"
    temp = check_2(num_row, alpha, mu_check)
    result += temp[1]
    if temp[0]:
        result += h0_comp + "\n"
    else:
        result += h1_comp + "\n"
    result += "\n"

    result += "Гипотеза о дисперсии:" + "\n"
    temp = check_3(num_row, alpha, dispersion_check)
    result += temp[1]
    if temp[0]:
        result += h0_comp + "\n"
    else:
        result += h1_comp + "\n"

    return result


layout = [
    [sg.Text('Параметры распереления')],
    [sg.Text('N:'), sg.InputText('100', key='N')],
    [sg.Text('μ:'), sg.InputText('0', key='μ')],
    [sg.Text('σ²:'), sg.InputText('1', key='σ²')],
    [sg.Submit("Сгенерировать выборку")],
    [sg.Output(size=(48, 10), key='out_f')],
    [sg.Text('Данные для проверки')],
    [sg.Text('α:'), sg.InputText('0.05', key='α')],
    [sg.Text('Мат. ожидание:'), sg.InputText('0', key='mu')],
    [sg.Text('Дисперсия:'), sg.InputText('1', key='dispersion')],
    [sg.Submit("Проверить гипотезы")],
    [sg.Output(size=(48, 10), key='out_a')],
]

window = sg.Window('Lab 3', layout)

while True:                          
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Сгенерировать выборку':
        num_row = make_row(int(values["N"]), float(values["μ"]), float(values["σ²"]))
        window["out_f"].update("\n".join(list(map(str, num_row[:10]))))
    if event == 'Проверить гипотезы':
        window["out_a"].update(check_all(float(values["σ²"]), float(values["α"]), float(values["mu"]), float(values["dispersion"])))


window.close()
