import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

A12 = 1.946
A21 = 1.61
T_FAIXA = (67.0, 80.1)
P = 101.325
T_CTE = 0.5 * (T_FAIXA[0] + T_FAIXA[1])
T_K = T_CTE + 273.15
R = 8.314462618
ANT1 = (16.8958, 3795.17, 230.918)
ANT2 = (13.7819, 2726.81, 217.572)
TEB_LIT = {"Etanol": 78.3, "Benzeno": 80.1}
AZ_LIT = {"T": 67.8, "x1": 0.44}
TITULO = "Etanol (1) + Benzeno (2) — Van Laar"


def psat(T, ant):
    A, B, C = ant
    return np.exp(A - B / (T + C))


def ln_gammas(x1):
    x1 = np.clip(np.asarray(x1, dtype=float), 1e-9, 1 - 1e-9)
    x2 = 1.0 - x1
    den = A12 * x1 + A21 * x2
    return A12 * (A21 * x2 / den) ** 2, A21 * (A12 * x1 / den) ** 2


def gE_RT(x1):
    x1 = np.clip(np.asarray(x1, dtype=float), 1e-9, 1 - 1e-9)
    x2 = 1.0 - x1
    return x1 * x2 * A12 * A21 / (A12 * x1 + A21 * x2)


def gE(x1):
    return R * T_K * gE_RT(x1)


def T_bolha(x1):
    g1, g2 = [float(g) for g in np.exp(ln_gammas(x1))]
    f = lambda T: x1 * g1 * psat(T, ANT1) + (1 - x1) * g2 * psat(T, ANT2) - P
    return brentq(f, 20.0, 150.0)


def y1_bolha(x1, T):
    g1 = float(np.exp(ln_gammas(x1)[0]))
    return x1 * g1 * psat(T, ANT1) / P


def T_ebulicao(ant):
    return brentq(lambda T: psat(T, ant) - P, 20.0, 150.0)


x1 = np.linspace(0.001, 0.999, 999)
lng1, lng2 = ln_gammas(x1)
T1_eb, T2_eb = T_ebulicao(ANT1), T_ebulicao(ANT2)
x_arr = np.linspace(0.001, 0.999, 300)
T_bub = np.array([T_bolha(x) for x in x_arr])
y_arr = np.array([y1_bolha(x, T) for x, T in zip(x_arr, T_bub)])


def dif_K(x):
    return y1_bolha(x, T_bolha(x)) - x


d = np.array([dif_K(x) for x in x_arr])
mud = np.where(np.diff(np.sign(d)) != 0)[0]
az = None
if len(mud) > 0:
    i = mud[0]
    x_az = brentq(dif_K, x_arr[i], x_arr[i + 1])
    T_az = T_bolha(x_az)
    az = (x_az, T_az)

fig1, ax = plt.subplots(figsize=(7, 5))
ax.plot(x1, lng1, label="ln γ₁ (etanol)")
ax.plot(x1, lng2, label="ln γ₂ (benzeno)")
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel("ln γ")
ax.set_title(f"ln γ × x₁ a T constante = {T_CTE:.2f} °C ({T_K:.2f} K)\n{TITULO}")
ax.legend()
fig1.tight_layout()
fig1.savefig("1_ln_gamma.png", dpi=150)

fig2, ax = plt.subplots(figsize=(7, 5))
ax.plot(x1, gE(x1), color="red")
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel("Gᴱ (J/mol)")
ax.set_title(f"Gᴱ × x₁ a T constante = {T_CTE:.2f} °C ({T_K:.2f} K)\n{TITULO}")
fig2.tight_layout()
fig2.savefig("2_GE.png", dpi=150)

fig3, ax = plt.subplots(figsize=(7, 6))
ax.plot(x_arr, T_bub, color="royalblue", lw=1.8, label="Líquido saturado (x₁)")
ax.plot(y_arr, T_bub, color="tomato", lw=1.8, ls="--", label="Vapor saturado (y₁)")
ax.scatter([0, 1], [T2_eb, T1_eb], color="black", zorder=5, s=35)
ax.annotate(f"Benzeno\n{T2_eb:.1f} °C", (0, T2_eb), textcoords="offset points", xytext=(8, -22), fontsize=8)
ax.annotate(f"Etanol\n{T1_eb:.1f} °C", (1, T1_eb), textcoords="offset points", xytext=(-45, -22), fontsize=8)
if az:
    ax.scatter([az[0]], [az[1]], color="green", zorder=6, s=45)
    ax.annotate(f"Azeótropo\nx₁={az[0]:.3f}; {az[1]:.1f} °C", az,
                textcoords="offset points", xytext=(12, 10), fontsize=8, color="green")
ax.set_xlabel("x₁, y₁ (etanol)")
ax.set_ylabel("T (°C)")
ax.set_title(f"Diagrama T-x-y a 1 atm\n{TITULO}")
ax.legend(loc="upper center")
fig3.tight_layout()
fig3.savefig("3_Txy.png", dpi=150)

fig4, ax = plt.subplots(figsize=(6, 6))
ax.plot(x_arr, y_arr, color="purple", lw=1.8, label="Equilíbrio")
ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="y = x")
if az:
    ax.scatter([az[0]], [az[0]], color="green", zorder=6, s=45, label="Azeótropo")
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel("y₁ (etanol)")
ax.set_title(f"Diagrama x-y a 1 atm\n{TITULO}")
ax.legend()
fig4.tight_layout()
fig4.savefig("4_xy.png", dpi=150)

print(f"T constante: {T_CTE:.2f} °C ({T_K:.2f} K)")
print(f"Pontos de ebulição: etanol {T1_eb:.2f} °C; benzeno {T2_eb:.2f} °C")
if az:
    print(f"Azeótropo: x₁ = y₁ = {az[0]:.4f}; T = {az[1]:.2f} °C")
print(f"Gᴱ máximo: {np.max(gE(x1)):.1f} J/mol em x₁ = {x1[np.argmax(gE(x1))]:.3f}")
print("Figuras salvas: 1_ln_gamma.png, 2_GE.png, 3_Txy.png, 4_xy.png")
plt.show()