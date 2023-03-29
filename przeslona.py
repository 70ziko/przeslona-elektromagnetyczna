# Patryk Fidler
# indeks: 259468
# Elektromagnetyczne bezpieczeństwo systemów i sieci
# Projekt 1 - Przesłona
# Kształt otworu - trójkąt równoramienny

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def liczba_sasiadow(podst, odl,  lambda_):
    h = podst
    d = int(np.floor((lambda_ + odl) / (h + odl))) # sąsiedzi w pionie
    n = int(np.floor((lambda_ + odl) / (podst/2 + odl))) # sąsiedzi w poziomie
    pair = lambda n: n - 1 if n%2 != 0 else n - 2 # zwraca parzystą liczbę
    if n >= d:
        return pair(n)
    else:
        return pair(d)
    

def skut_ekranowania(podst, lambda_, odl):

    b = ((5**0.5)/2) * podst
    n = liczba_sasiadow(podst, odl, lambda_)

    if n == 0:
        S = 20*np.log10(lambda_/(2*b))
    else:
        S = 20*np.log10(lambda_/(2*b)) - 20*np.log10(n**0.5)
    return S
    
def pole_otworu(podst):
    h = podst
    P = (podst/2)*h
    return P

def otwory_wiersz(bok_plyty, podst, odl):
    n = int(np.floor((bok_plyty + odl) / (podst/2 + odl)))
    return n

def otwory_kolumn(bok_plyty, h, odl):
    n = int(np.floor((bok_plyty + odl) / (h + odl)))
    return n

def czesc_pola_plyty(bok_plyty, podst, odl):
    P = ((otwory_wiersz(bok_plyty, podst, odl)*otwory_kolumn(bok_plyty, podst, odl)*pole_otworu(podst))/(bok_plyty**2))*100
    return P


def maximize_czesc_pola_plyty(podst_range, odl_range, min_skut_ekranu, lambda_, bok_plyty):
    results = []
    good_results = []
    max_pole = 0
    max = []

    for pod in podst_range:
        for odl in odl_range:
            results.append((pod, odl, \
            skut_ekranowania(pod, lambda_, odl), \
            czesc_pola_plyty(bok_plyty, pod, odl), \
            liczba_sasiadow(pod, odl, lambda_)))

    for i in results:
        if i[2] >= min_skut_ekranu:
            good_results.append(i)
            if i[3] >= max_pole:
                max = i
                max_pole = i[3]

    print(f'max pole posiada: {max[-1]} z polem: {max_pole}')

    return max, good_results

def plot_skutecznosc_ekranowania(results):
    # set up the figure and axes
    x = [row[0] for row in results]
    y = [row[1] for row in results]
    z = [row[2] for row in results]
    pole = [row[3] for row in results]

    fig = plt.figure(1)
 

    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')
    
    ax.scatter3D(x, y, z)
    ax.set_title('Skuteczność ekranowania')

    plt.xlabel('podstawa [cm]')
    plt.ylabel('odległość [cm]')


    plot_pole = plt.figure(2)
    plt.scatter(pole, z)
    plt.xlabel('Część pola przesłony [%]')
    plt.ylabel('Skuteczność ekranowania [dB]')
    plt.title('Część pola przesłony w zależności od skuteczności ekranowania')
    plt.show()


def main():
    freq = 4680 # [MHz]
    lambda_ = (300/freq)*100 # [cm] = ~6.41cm
    bok_plyty = 50 # [cm]
    min_skut_ekran = 15 # [dB] 

    podst_range = [i for i in np.arange(0.01, lambda_/2, 0.01)]
    odl_range = [i for i in np.arange(lambda_/10, lambda_/2, 0.1)]

    max, res = maximize_czesc_pola_plyty(podst_range, odl_range, min_skut_ekran, lambda_, bok_plyty)
    print('Wyniki: ')
    for i in res:
        if i[2] >= min_skut_ekran:
            print(i)

    print(f'Wynik: {max}')

    plot_skutecznosc_ekranowania(res)


if __name__ == '__main__':
    main()


