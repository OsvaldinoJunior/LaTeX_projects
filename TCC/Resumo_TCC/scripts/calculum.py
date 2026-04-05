import matplotlib
matplotlib.use("Agg")  # deve vir antes do pyplot

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

conc_mae = 2.71
TURBIDIA = [
    (  5,  18.12, 97.95),
    ( 10,  39.70, 98.85),
    ( 15,  59.55, 99.40),
    ( 25,  65.57, 99.20),
    ( 50,  81.95, 99.85),
    (100,  91.25, 99.95),
]

abs_corr_list, conc_real_list = [], []
for fd, pct_T_susp, pct_T_sob in TURBIDIA:
    abs_susp = round(-np.log10(pct_T_susp / 100), 4)
    abs_sob  = round(-np.log10(pct_T_sob  / 100), 4)
    abs_corr = round(abs_susp - abs_sob, 4)
    c_real   = round(conc_mae / fd, 4)
    abs_corr_list.append(abs_corr)
    conc_real_list.append(c_real)

x = np.array(conc_real_list, dtype=float)
y = np.array(abs_corr_list,  dtype=float)

slope, intercept, r_value, *_ = stats.linregress(x, y)
r2 = round(r_value**2, 4)
a  = round(slope,      4)
b  = round(intercept,  4)

x_fit = np.linspace(0, max(x) * 1.08, 300)
y_fit = a * x_fit + b

def br(v, d=4):
    return f"{v:.{d}f}".replace(".", ",")

eq_str = f"$A = {br(a)} \\cdot C - {br(abs(b))}$"
r2_str = f"$R^2 = {br(r2)}$"

fig, ax = plt.subplots(figsize=(7, 5))

ax.scatter(x, y, color="black", s=60, zorder=5, label="Dados experimentais")
ax.plot(x_fit, y_fit, color="black", linewidth=1.5, label=f"{eq_str}\n{r2_str}")

ax.set_xlabel("Concentração de biomassa (g/L)", fontsize=12)
ax.set_ylabel("Absorbância (600 nm)", fontsize=12)

ax.grid(False)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.tick_params(which='both', direction='in', top=True, right=True)

ax.set_xlim(left=-max(x) * 0.045, right=max(x) * 1.14)
ax.set_ylim(bottom=-max(y) * 0.045, top=max(y) * 1.14)

ax.legend(fontsize=10, framealpha=1, edgecolor="#cccccc",
          handlelength=1.5, handletextpad=0.6)

plt.tight_layout()
fig.savefig("curva_padrao.png", dpi=300, bbox_inches="tight")
print("Salvo: curva_padrao.png")
