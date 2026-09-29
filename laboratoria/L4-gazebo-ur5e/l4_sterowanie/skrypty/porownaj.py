"""Porównanie przebiegów z rejestratora dla różnych sposobów sterowania.

Użycie: python3 porownaj.py wprost.csv wprost_interp.csv trajektoria.csv ik.csv
Wynik: tabela (czas ruchu, maks. prędkość, maks. przyspieszenie) i wykresy porownanie.png.
"""
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def wczytaj(sciezka):
    dane = np.genfromtxt(sciezka, delimiter=',', names=True)
    t = dane['t']
    q = np.column_stack([dane[f'q{i+1}'] for i in range(6)])
    v = np.column_stack([dane[f'v{i+1}'] for i in range(6)])
    rosnacy = np.concatenate([[True], np.diff(t) > 1e-6])   # usuń powtórzone znaczniki czasu
    return t[rosnacy], q[rosnacy], v[rosnacy]


def main(pliki):
    fig, osie = plt.subplots(len(pliki), 2, figsize=(12, 3 * len(pliki)), squeeze=False)
    print(f'{"plik":28s} {"czas ruchu [s]":>15s} {"max |v| [rad/s]":>16s} {"max |a| [rad/s²]":>17s}')
    for wiersz, sciezka in zip(osie, pliki):
        t, q, v = wczytaj(sciezka)                # v: prędkości zmierzone w symulatorze
        okno = 25                                   # średnia ruchoma: prędkość z symulatora jest zaszumiona
        v_gl = np.apply_along_axis(lambda x: np.convolve(x, np.ones(okno) / okno, mode='same'), 0, v)
        a = np.gradient(v_gl, t, axis=0)
        w_ruchu = np.abs(v).max(axis=1) > 0.01
        czas_ruchu = t[w_ruchu][-1] - t[w_ruchu][0] if w_ruchu.any() else 0.0
        print(f'{sciezka:28s} {czas_ruchu:15.2f} {np.abs(v).max():16.3f} {np.abs(a).max():17.2f}')
        wiersz[0].plot(t, q); wiersz[0].set_title(f'{sciezka}: q(t)'); wiersz[0].set_xlabel('t [s]')
        wiersz[1].plot(t, v); wiersz[1].set_title('prędkość przegubów [rad/s]'); wiersz[1].set_xlabel('t [s]')
    plt.tight_layout()
    plt.savefig('porownanie.png', dpi=120)
    print('Zapisano porownanie.png')


if __name__ == '__main__':
    main(sys.argv[1:])
