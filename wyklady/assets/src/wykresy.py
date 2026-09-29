"""Generuje wykresy do wykładów (SVG w wyklady/assets/).

Uruchomienie: python3 wyklady/assets/src/wykresy.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent
RED, BLUE, GRAY, GREEN = "#9d1c20", "#1f5f99", "#777777", "#2e7d32"

plt.rcParams.update({
    "font.size": 15, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "font.family": "sans-serif",
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, transparent=False, facecolor="white")
    plt.close(fig)
    print("zapisano", name)


def adc():
    t = np.linspace(0, 1, 1000)
    u = 1.4 + 1.2 * np.sin(2 * np.pi * t) + 0.4 * np.sin(6 * np.pi * t)
    vref, bits = 3.3, 3
    lsb = vref / 2**bits
    code = np.clip(np.floor(u / lsb), 0, 2**bits - 1)
    ts = np.linspace(0, 1, 25)
    us = 1.4 + 1.2 * np.sin(2 * np.pi * ts) + 0.4 * np.sin(6 * np.pi * ts)
    cs = np.clip(np.floor(us / lsb), 0, 2**bits - 1)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(t, u, color=GRAY, lw=2, label="sygnał analogowy")
    ax.step(ts, cs * lsb, where="post", color=RED, lw=2.5, label="po przetworniku (3 bity)")
    ax.plot(ts, us, "o", color=BLUE, ms=5, label="chwile próbkowania")
    for k in range(2**bits + 1):
        ax.axhline(k * lsb, color="#dddddd", lw=0.8, zorder=0)
    ax.set_xlabel("czas [s]")
    ax.set_ylabel("napięcie [V]")
    ax.set_ylim(-0.1, 3.4)
    ax.legend(loc="upper right", fontsize=12, frameon=False)
    save(fig, "w02-adc.svg")


def pwm():
    fig, axes = plt.subplots(3, 1, figsize=(9, 4.6), sharex=True)
    t = np.linspace(0, 3, 3000)
    for ax, d in zip(axes, [0.25, 0.5, 0.8]):
        s = ((t % 1) < d).astype(float) * 3.3
        ax.plot(t, s, color=RED, lw=2)
        ax.hlines(3.3 * d, 0, 3, color=BLUE, lw=2, ls="--")
        ax.text(3.1, 3.3 * d, f"średnio {3.3*d:.2f} V", color=BLUE, va="center", fontsize=13)
        ax.set_xlim(-0.05, 4.1)
        ax.set_xticks([0, 1, 2, 3])
        ax.set_ylabel(f"D={int(d*100)}%", rotation=0, labelpad=40, va="center")
        ax.set_yticks([0, 3.3])
        ax.set_ylim(-0.3, 3.8)
    axes[-1].set_xlabel("czas [okresy PWM]")
    save(fig, "w02-pwm.svg")


def debounce():
    t = np.linspace(0, 30, 3000)
    s = np.ones_like(t) * 3.3
    rng = np.random.default_rng(3)
    edges = [5, 5.4, 5.9, 6.2, 6.8, 7.1, 7.9, 8.2]
    state = 3.3
    for i, e in enumerate(edges):
        state = 0 if i % 2 == 0 else 3.3
        s[t >= e] = state
    s[t >= 9] = 0
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(t, s, color=RED, lw=2)
    ax.axvspan(5, 9, color="#f3d2d3", alpha=0.6)
    ax.text(7, 3.75, "drgania styków (ok. 1–10 ms)", ha="center", fontsize=13)
    ax.set_ylim(-0.3, 4.3)
    ax.set_xlabel("czas [ms]")
    ax.set_ylabel("PA0 [V]")
    ax.set_yticks([0, 3.3])
    ax.text(20, 0.3, "przycisk wciśnięty (pull-up, stan niski)", fontsize=12, color=GRAY)
    save(fig, "w02-drgania.svg")


def rc():
    t = np.linspace(0, 5, 500)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(t, 1 - np.exp(-t), color=RED, lw=2.5, label=r"$u_C(t)=U(1-e^{-t/\tau})$")
    ax.axvline(1, color=GRAY, ls="--")
    ax.text(1.05, 0.2, r"$\tau=RC$ (63%)", color=GRAY)
    ax.axvline(5, color=GRAY, ls=":")
    ax.text(4.1, 0.5, r"$5\tau$ (99%)", color=GRAY)
    ax.set_xlabel(r"czas [$\tau$]")
    ax.set_ylabel(r"$u_C/U$")
    ax.legend(frameon=False, loc="lower right")
    save(fig, "w02-rc.svg")


def pid():
    """Odpowiedź skokowa napędu (model 1. rzędu + integrator) z regulatorem P, PI, PID."""
    dt, T = 0.001, 3.0
    n = int(T / dt)
    tau, k = 0.15, 1.0
    fig, ax = plt.subplots(figsize=(9, 4))
    for (kp, ki, kd), col, lab in [
        ((4, 0, 0), GRAY, "P"),
        ((12, 0, 0.0), BLUE, "P (duże $K_p$)"),
        ((12, 0, 0.6), RED, "PD"),
    ]:
        x = v = integ = 0.0
        prev_e = 1.0
        xs = []
        for _ in range(n):
            e = 1.0 - x
            integ += e * dt
            u = kp * e + ki * integ + kd * (e - prev_e) / dt
            prev_e = e
            v += dt * (-v + k * u) / tau
            x += dt * v
            xs.append(x)
        ax.plot(np.arange(n) * dt, xs, color=col, lw=2.2, label=lab)
    ax.axhline(1, color="black", lw=1, ls="--")
    ax.set_xlabel("czas [s]")
    ax.set_ylabel("położenie [rad]")
    ax.legend(frameon=False)
    save(fig, "w10-pid.svg")


def przeuczenie():
    """Dopasowanie wielomianów różnego stopnia: niedouczenie, dobre dopasowanie, przeuczenie."""
    rng = np.random.default_rng(1)
    x = np.sort(rng.uniform(0, 1, 14))
    f = lambda z: np.sin(2 * np.pi * z)
    y = f(x) + rng.normal(0, 0.2, x.size)
    xx = np.linspace(0, 1, 400)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
    for ax, deg, tyt in zip(axes, [1, 4, 13], ["niedouczenie (st. 1)", "dobre dopasowanie (st. 4)", "przeuczenie (st. 13)"]):
        c = np.polynomial.polynomial.Polynomial.fit(x, y, deg)
        ax.plot(xx, f(xx), color=GRAY, lw=1.5, ls="--", label="prawdziwa zależność")
        ax.plot(xx, c(xx), color=RED, lw=2.2, label="model")
        ax.plot(x, y, "o", color=BLUE, ms=6, label="dane uczące")
        ax.set_title(tyt, fontsize=15)
        ax.set_ylim(-1.8, 1.8)
        ax.set_xlabel("x")
    axes[0].legend(frameon=False, fontsize=11, loc="lower left")
    save(fig, "w12-przeuczenie.svg")


if __name__ == "__main__":
    adc(); pwm(); debounce(); rc(); pid(); przeuczenie()
