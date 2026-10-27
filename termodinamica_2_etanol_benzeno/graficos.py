import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# Uma identidade visual comum, com rótulos legíveis na projeção dos slides.
NAVY = "#19314B"
TEAL = "#00777E"
GOLD = "#DC9D2D"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.labelcolor": NAVY,
    "axes.edgecolor": "#8D9CA9",
    "axes.linewidth": 0.8,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "legend.fontsize": 14,
    "text.color": NAVY,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "lines.linewidth": 2.8,
    "mathtext.fontset": "dejavusans",
})


def eixos_apresentacao():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(color="#DCE5EA", linewidth=0.65, alpha=0.6)
    ax.tick_params(length=3, width=0.8, pad=5)
    ax.set_xlim(0, 1)
    ax.set_xticks(np.linspace(0, 1, 6))
    return fig, ax


def salvar_figura(fig, arquivo):
    fig.tight_layout(pad=0.75)
    fig.savefig(arquivo, dpi=220)

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

fig1, ax = eixos_apresentacao()
ax.plot(x1, lng1, color=TEAL, label="Etanol (1)")
ax.plot(x1, lng2, color=NAVY, linestyle="--", label="Benzeno (2)")
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel("ln γ")
ax.set_ylim(0, 2.1)
ax.set_yticks(np.arange(0, 2.1, 0.5))
ax.legend(loc="upper center", frameon=False, handlelength=2.2)
salvar_figura(fig1, "1_ln_gamma.png")

fig2, ax = eixos_apresentacao()
ax.plot(x1, gE(x1), color=TEAL)
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel(r"$G^E$ (J/mol)")
ax.set_ylim(0, 1400)
ax.set_yticks([0, 400, 800, 1200])
salvar_figura(fig2, "2_GE.png")

fig3, ax = eixos_apresentacao()
ax.plot(x_arr, T_bub, color=TEAL, label="Líquido (x₁)")
ax.plot(y_arr, T_bub, color=NAVY, linestyle="--", label="Vapor (y₁)")
ax.scatter([0, 1], [T2_eb, T1_eb], color=NAVY, zorder=5, s=32, clip_on=False)
ax.annotate(f"Benzeno\n{T2_eb:.1f} °C", (0, T2_eb), textcoords="offset points",
            xytext=(8, 9), va="bottom", fontsize=13)
ax.annotate(f"Etanol\n{T1_eb:.1f} °C", (1, T1_eb), textcoords="offset points",
            xytext=(-8, 9), ha="right", va="bottom", fontsize=13)
if az:
    ax.scatter([az[0]], [az[1]], color=GOLD, edgecolor=NAVY, linewidth=0.5,
               zorder=6, s=68)
    ax.annotate("Azeótropo", az, textcoords="data", xytext=(0.5, 73.2),
                ha="center", fontsize=14,
                arrowprops={"arrowstyle": "-", "color": NAVY, "lw": 0.8})
ax.set_xlabel("x₁, y₁ (etanol)")
ax.set_ylabel("T (°C)")
ax.set_ylim(66, 83)
ax.set_yticks([68, 72, 76, 80])
ax.legend(loc="upper center", frameon=False, handlelength=2.2)
salvar_figura(fig3, "3_Txy.png")

fig4, ax = eixos_apresentacao()
ax.plot(x_arr, y_arr, color=TEAL, label="Equilíbrio")
ax.plot([0, 1], [0, 1], color=NAVY, linestyle="--", linewidth=1.6, label="y₁ = x₁")
if az:
    ax.scatter([az[0]], [az[0]], color=GOLD, edgecolor=NAVY, linewidth=0.5,
               zorder=6, s=68, label="Azeótropo")
ax.set_xlabel("x₁ (etanol)")
ax.set_ylabel("y₁ (etanol)")
ax.set_ylim(0, 1)
ax.set_yticks(np.linspace(0, 1, 6))
ax.legend(loc="upper left", frameon=False, handlelength=2.2)
salvar_figura(fig4, "4_xy.png")

print(f"T constante: {T_CTE:.2f} °C ({T_K:.2f} K)")
print(f"Pontos de ebulição: etanol {T1_eb:.2f} °C; benzeno {T2_eb:.2f} °C")
if az:
    print(f"Azeótropo: x₁ = y₁ = {az[0]:.4f}; T = {az[1]:.2f} °C")
print(f"Gᴱ máximo: {np.max(gE(x1)):.1f} J/mol em x₁ = {x1[np.argmax(gE(x1))]:.3f}")
print("Figuras salvas: 1_ln_gamma.png, 2_GE.png, 3_Txy.png, 4_xy.png")
plt.show()
