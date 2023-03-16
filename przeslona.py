# Patryk Fidler
# indeks: 259468
# Elektromagnetyczne bezpieczeństwo systemów i sieci
# Projekt 1 - Przesłona
# Kształt otworu - trójkąt równoramienny

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

freq = 4680 # [MHz]
lambda_ = (300/freq)*100 # [cm] 6.41
bok_plyty = 50 # [cm]

min_skut_ekran = 15 # [dB]

a_otworu = lambda_/2 # [m]
b_otworu = a_otworu/2 # [m]

odl_otworow = lambda_/10 # [m]

print(f'lambda: {lambda_}')

# Największa długość liniowa trójkąta rownoramiennego 
# jest równa długości najdłuższego boku

# Maksymalna długość liniowa otworu = lambda/2
# Minimalna odległość otworów = lambda/10

# Skuteczność ekranowania dla jednego otworu
print(lambda_/(2*a_otworu))

def skut_jednej_dziury(a_otworu, b_otworu, lambda_):
    if b_otworu > a_otworu:
        a_otworu, b_otworu = b_otworu, a_otworu
    S = 20*np.log10(lambda_/(2*a_otworu))
    return S

def liczba_sasiadow(a_otworu, b_otworu, lambda_):
    if b_otworu > a_otworu:
        a_otworu, b_otworu = b_otworu, a_otworu

    d = int(np.floor(((lambda_) + odl_otworow) / (a_otworu + odl_otworow)))
    return d

print(f'Liczba sąsiadujących otworów: {liczba_sasiadow(a_otworu, b_otworu, lambda_)}')

def skut_ekranowania(a_otworu, lambda_):

    n = liczba_sasiadow(a_otworu, b_otworu, lambda_)

    S = 20*np.log10(lambda_/(2*a_otworu)) - 20*np.log10(n**0.5)
    return S

a_otworu_range = [i for i in np.arange(0.01, lambda_/2, 0.01)]
# b_otworu_range = [i for i in np.arange(lambda_/2, 0.01, -0.01)]
odl_otworu_range = [i for i in np.arange(lambda_/10, lambda_/2, 0.01)]

def wys_otworu(a_otworu):
    h = np.sqrt(a_otworu**2 - (a_otworu/2)**2)
    return h
    
def pole_otworu(a_otworu=a_otworu):
    P = 0.5*(a_otworu/2)*wys_otworu(a_otworu)
    return P

print(f'a_otworu: {a_otworu}\nPole otworu: {pole_otworu(a_otworu)}')

def liczba_otworow_wiersz(bok_plyty, b_otworu, odl_otworu):
    n = int(np.floor((bok_plyty + odl_otworu) / (b_otworu + odl_otworu)))
    return n

def liczba_otworow_kolumn(bok_plyty, h, odl_otworu):
    n = int(np.floor((bok_plyty + odl_otworu) / (h + odl_otworu)))
    return n

def czesc_pola_plyty(bok_plyty, a_otworu, h, odl_otworu):
    P = ((liczba_otworow_wiersz(bok_plyty, a_otworu, odl_otworu)*liczba_otworow_kolumn(bok_plyty, h, odl_otworu)*pole_otworu(a_otworu))/(bok_plyty**2))*100
    return P

print(f'Liczba otworów w wierszu: {liczba_otworow_wiersz(bok_plyty, b_otworu, odl_otworow)}')
print(f'Liczba otworów w kolumnie: {liczba_otworow_kolumn(bok_plyty, wys_otworu(a_otworu), odl_otworow)}')
print(f'Część pola płytki zajmowana przez otwory: {czesc_pola_plyty(bok_plyty, a_otworu, wys_otworu(a_otworu), odl_otworow)}')

def maximize_czesc_pola_plyty(a_otworu_range, odl_otworu, min_skut_ekranu):
    results = []
    good_results = []
    max_pole = 0

    for idx, val in enumerate(a_otworu_range):
        results.append((val, skut_ekranowania(val, lambda_), czesc_pola_plyty(bok_plyty, val, wys_otworu(val), odl_otworu)))
        if results[idx][1] > min_skut_ekranu:
            good_results.append((val, skut_ekranowania(val, lambda_), czesc_pola_plyty(bok_plyty, val, wys_otworu(val), odl_otworu)))
            if results[idx][2] > max_pole:
                max_pole = results[idx][2]

    return good_results, max_pole

print(f'Wyniki: {maximize_czesc_pola_plyty(a_otworu_range, odl_otworow, min_skut_ekran)}')

def plot_skutecznosc_ekranowania(a_otworu_range, odl_otworu_range):
    a_otworu_vals = np.linspace(a_otworu_range[0], a_otworu_range[1], 50)
    odl_otworu_vals = np.linspace(odl_otworu_range[0], odl_otworu_range[1], 50)
    skutecznosc_ekranowania = np.zeros((len(a_otworu_vals), len(odl_otworu_vals)))

    for i, a_otworu in enumerate(a_otworu_vals):
        for j, odl_otworu in enumerate(odl_otworu_vals):
            b_otworu = a_otworu / 2
            h = np.sqrt(a_otworu**2 - (a_otworu/2)**2)
            skutecznosc_ekranowania[i,j] = skut_ekranowania(a_otworu, b_otworu, lambda_)

    plt.contourf(odl_otworu_vals, a_otworu_vals, skutecznosc_ekranowania, levels=20, cmap='coolwarm')
    plt.colorbar()
    plt.xlabel('odl_otworu')
    plt.ylabel('a_otworu')
    plt.title('Skutecznosc ekranowania')
    plt.show()

#     plt.scatter(results_arr[:, 0], results_arr[:, 1], c=results_arr[:, 2], cmap='viridis')
#     plt.colorbar(label='odl_otworu')
#     plt.xlabel('a_otworu')
#     plt.ylabel('b_otworu')
#     plt.title('Skutecznosc ekranowania')
#     plt.show()

# plot_skutecznosc_ekranowania(a_otworu_range, odl_otworu_range)

# optimal_params, optimal_S = optymalizacja(a_otworu_range, b_otworu_range, odl_otworu_range, pole_plyty, min_skut_ekran)

# print(f'Optymalne parametry: {optimal_params}\nOptymalna skuteczność ekranowania: {optimal_S}')
