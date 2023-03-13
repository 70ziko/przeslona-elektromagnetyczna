# Patryk Fidler
# indeks: 259468
# Elektromagnetyczne bezpieczeństwo systemów i sieci
# Projekt 1 - Przesłona
# Kształt otworu - trójkąt równoramienny

import numpy as np
import matplotlib.pyplot as plt

freq = 4680 # [MHz]
lambda_ = (300/freq)*100 # [cm] 6.41
bok_plyty = 50 # [cm]
pole_plyty = bok_plyty**2 # [cm^2]

min_skut_ekran = 15 # [dB]

a_otworu = lambda_/10 # [m]
b_otworu = lambda_/10 # [m]

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

def skut_ekranowania(a_otworu, b_otworu, lambda_):
    if b_otworu > a_otworu:
        a_otworu, b_otworu = b_otworu, a_otworu

    d = liczba_sasiadow(a_otworu, b_otworu, lambda_)

    S = 20*np.log10(lambda_/(2*a_otworu)) - 20*np.log10(d**0.5)
    return S


print(f'Skuteczność ekranowania dla jednego otworu: {skut_jednej_dziury(a_otworu, b_otworu, lambda_)}')
print(f'Skuteczność ekranowania: {skut_ekranowania(a_otworu, b_otworu, lambda_)}')