#!/usr/bin/env python3
"""
============================================================
  Curva Padrão de Biomassa — Turbidimetria a 600 nm
  Saccharomyces cerevisiae (adaptável a outros cultivos)
============================================================
  Para usar em outro cultivo, edite APENAS o bloco
  "DADOS DE ENTRADA" abaixo. O restante do script
  calcula tudo automaticamente.
============================================================
  Dependências:
    pip install numpy scipy matplotlib pandas openpyxl
============================================================
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# ============================================================
#  DADOS DE ENTRADA — edite aqui para cada novo cultivo
# ============================================================

# --- Identificação do experimento ---
NOME_CULTIVO        = "Saccharomyces cerevisiae ATCC 7754"
MEIO_CULTURA        = "Meio YM"
TEMPERATURA_C       = 30        # °C
AGITACAO_RPM        = 100
TEMPO_CULTIVO_H     = 27
COMPRIMENTO_ONDA_NM = 600       # nm

# --- Gravimetria ---
# Uma tupla por tubo: (massa_tubo_g, massa_total_g, volume_L)
GRAVIMET = [
    (5.5054, 5.5341, 0.010),   # tubo 1
    (5.3165, 5.3420, 0.010),   # tubo 2
    (5.4825, 5.5095, 0.010),   # tubo 3
]

# --- Turbidimetria ---
# Uma tupla por diluição: (fator_diluicao, %T_suspensao, %T_sobrenadante)
TURBIDIA = [
    (  5,  18.12, 97.95),
    ( 10,  39.70, 98.85),
    ( 15,  59.55, 99.40),
    ( 25,  65.57, 99.20),
    ( 50,  81.95, 99.85),
    (100,  91.25, 99.95),
]

# ============================================================
#  FIM DOS DADOS DE ENTRADA
# ============================================================

SEP = "=" * 62

# ------------------------------------------------------------
#  1. GRAVIMETRIA
# ------------------------------------------------------------
print(SEP)
print(f"  CURVA PADRÃO DE BIOMASSA")
print(f"  Cultivo : {NOME_CULTIVO}")
print(f"  Meio    : {MEIO_CULTURA}  |  {TEMPERATURA_C} °C  |  {AGITACAO_RPM} rpm  |  {TEMPO_CULTIVO_H} h")
print(SEP)

tubos_ids, massas_biomassa, concentracoes = [], [], []

header = (f"{'Tubo':>5}  {'M. tubo (g)':>12}  {'M. total (g)':>13}  "
          f"{'Biomassa (g)':>13}  {'Vol (L)':>8}  {'Conc (g/L)':>11}")
print(f"\n[1] GRAVIMETRIA\n")
print(header)
print("-" * len(header))

for i, (m_tubo, m_total, vol) in enumerate(GRAVIMET, start=1):
    biomassa = round(float(m_total) - float(m_tubo), 4)
    conc     = round(biomassa / float(vol), 4)
    tubos_ids.append(i)
    massas_biomassa.append(biomassa)
    concentracoes.append(conc)
    print(f"{i:>5}  {m_tubo:>12.4f}  {m_total:>13.4f}  "
          f"{biomassa:>13.4f}  {vol:>8.3f}  {conc:>11.4f}")

conc_mae = round(float(np.mean(concentracoes)),          4)
desvio   = round(float(np.std(concentracoes, ddof=1)),   4)
cv       = round((desvio / conc_mae) * 100,              2)

print("-" * len(header))
w = len(header) - 13
print(f"{'Média':>{w}}  {conc_mae:>11.4f}")
print(f"{'Desvio padrão':>{w}}  {desvio:>11.4f}")
print(f"{'CV (%)':>{w}}  {cv:>11.2f}")
print(f"\n  → Concentração da solução mãe adotada: {conc_mae:.4f} g/L")


# ------------------------------------------------------------
#  2. TURBIDIMETRIA
# ------------------------------------------------------------
fds, abs_susp_list, abs_sob_list, abs_corr_list, conc_real_list = [], [], [], [], []

header2 = (f"{'FD':>5}  {'%T susp':>8}  {'Abs susp':>10}  "
           f"{'%T sobren':>10}  {'Abs sobren':>12}  {'Abs corrig':>11}  {'C real (g/L)':>13}")
print(f"\n[2] TURBIDIMETRIA\n")
print(header2)
print("-" * len(header2))

for fd, pct_T_susp, pct_T_sob in TURBIDIA:
    abs_susp = round(-np.log10(float(pct_T_susp) / 100.0), 4)
    abs_sob  = round(-np.log10(float(pct_T_sob)  / 100.0), 4)
    abs_corr = round(abs_susp - abs_sob, 4)
    c_real   = round(conc_mae / float(fd), 4)

    fds.append(int(fd))
    abs_susp_list.append(float(abs_susp))
    abs_sob_list.append(float(abs_sob))
    abs_corr_list.append(float(abs_corr))
    conc_real_list.append(float(c_real))

    print(f"{fd:>5}  {pct_T_susp:>8.2f}  {abs_susp:>10.4f}  "
          f"{pct_T_sob:>10.2f}  {abs_sob:>12.4e}  {abs_corr:>11.4f}  {c_real:>13.4f}")


# ------------------------------------------------------------
#  3. REGRESSÃO LINEAR
# ------------------------------------------------------------
x = np.array(abs_corr_list,  dtype=float)
y = np.array(conc_real_list, dtype=float)

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r2    = round(float(r_value**2), 4)
a     = round(float(slope),      4)
b     = round(float(intercept),  4)
sinal = "+" if b >= 0 else "−"
ab    = abs(b)

print(f"\n[3] REGRESSÃO LINEAR  (C = a·A{COMPRIMENTO_ONDA_NM} + b)\n")
print(f"  C = {a:.4f} · A{COMPRIMENTO_ONDA_NM} {sinal} {ab:.4f}")
print(f"  R²                       = {r2:.4f}  ({r2*100:.2f}% da variação explicada)")
print(f"  Erro padrão da regressão = {std_err:.6f}")
print(f"  p-valor (coef. angular)  = {p_value:.2e}")


# ------------------------------------------------------------
#  4. CONCENTRAÇÕES PREDITAS vs. REAIS
# ------------------------------------------------------------
header4 = (f"{'FD':>5}  {'Cálculo':>14}  {'C real (g/L)':>13}  "
           f"{'Abs corrig':>11}  {'C curva (g/L)':>14}  {'Erro abs.':>10}  {'Erro (%)':>9}")
print(f"\n[4] CONCENTRAÇÕES PREDITAS vs. REAIS\n")
print(header4)
print("-" * len(header4))

c_curva_list, erros_abs, erros_pct = [], [], []
for fd, abs_corr, c_real in zip(fds, abs_corr_list, conc_real_list):
    c_curva  = round(a * abs_corr + b, 4)
    erro_abs = round(abs(c_real - c_curva), 4)
    erro_pct = round((erro_abs / c_real) * 100, 2) if c_real != 0 else 0.0
    c_curva_list.append(float(c_curva))
    erros_abs.append(float(erro_abs))
    erros_pct.append(float(erro_pct))
    calc_str = f"{conc_mae:.4f} / {fd}"
    print(f"{fd:>5}  {calc_str:>14}  {c_real:>13.4f}  "
          f"{abs_corr:>11.4f}  {c_curva:>14.4f}  {erro_abs:>10.4f}  {erro_pct:>9.2f}")

print("-" * len(header4))
w4 = len(header4) - 12
print(f"{'Erro médio absoluto':>{w4}}  {float(np.mean(erros_abs)):>10.4f}")
print(f"{'Erro médio percentual':>{w4}}  {float(np.mean(erros_pct)):>9.2f}%")


# ------------------------------------------------------------
#  5. RESUMO
# ------------------------------------------------------------
print(f"\n[5] RESUMO\n")
print(f"  Solução mãe   : {conc_mae:.4f} g/L  (DP = {desvio:.4f}  |  CV = {cv:.2f}%)")
print(f"  Equação       : C = {a:.4f}·A{COMPRIMENTO_ONDA_NM} {sinal} {ab:.4f}")
print(f"  R²            : {r2:.4f}")
print(f"  Faixa linear  : Abs {float(min(x)):.4f} – {float(max(x)):.4f}"
      f"  |  Conc {float(min(y)):.4f} – {float(max(y)):.4f} g/L")


# ------------------------------------------------------------
#  6. GRÁFICO
# ------------------------------------------------------------
x_fit   = np.linspace(0, float(max(x)) * 1.08, 300)
y_fit   = a * x_fit + b
eq_lbl  = f"C = {a:.4f}·A$_{{600}}$ {sinal} {ab:.4f}\nR² = {r2:.4f}"

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(x, y, color="#000000", s=60, zorder=5, label="Pontos experimentais")
ax.plot(x_fit, y_fit, color="#000000", linewidth=1.6, label=eq_lbl)
ax.set_xlabel(f"Absorbância corrigida (A$_{{{COMPRIMENTO_ONDA_NM}}}$)", fontsize=11)
ax.set_ylabel("Concentração de biomassa (g/L)", fontsize=11)
ax.set_title(
    f"Curva padrão — {NOME_CULTIVO}\n"
    f"{MEIO_CULTURA}  |  {TEMPERATURA_C} °C  |  {TEMPO_CULTIVO_H} h",
    fontsize=10, pad=10,
)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(which="major", linestyle="--", linewidth=0.5, alpha=0.5)
ax.grid(which="minor", linestyle=":",  linewidth=0.3, alpha=0.3)
ax.legend(fontsize=10, framealpha=0.9)
plt.tight_layout()
fig.savefig("curva_padrao_biomassa.png", dpi=180, bbox_inches="tight")
print(f"\n  Gráfico salvo : curva_padrao_biomassa.png")


# ------------------------------------------------------------
#  7. EXPORTAR EXCEL (.xlsx) com 3 abas e formatação numérica
# ------------------------------------------------------------
# Aba 1 — Gravimetria
df_grav = pd.DataFrame({
    "Tubo":            tubos_ids,
    "Massa_tubo_g":    [float(g[0]) for g in GRAVIMET],
    "Massa_total_g":   [float(g[1]) for g in GRAVIMET],
    "Biomassa_g":      [float(v) for v in massas_biomassa],
    "Volume_L":        [float(g[2]) for g in GRAVIMET],
    "Concentracao_gL": [float(v) for v in concentracoes],
})
df_grav = pd.concat([df_grav, pd.DataFrame([
    {"Tubo": "Média",  "Massa_tubo_g": None, "Massa_total_g": None,
     "Biomassa_g": None, "Volume_L": None, "Concentracao_gL": float(conc_mae)},
    {"Tubo": "DP",     "Massa_tubo_g": None, "Massa_total_g": None,
     "Biomassa_g": None, "Volume_L": None, "Concentracao_gL": float(desvio)},
    {"Tubo": "CV (%)", "Massa_tubo_g": None, "Massa_total_g": None,
     "Biomassa_g": None, "Volume_L": None, "Concentracao_gL": float(cv)},
])], ignore_index=True)

# Aba 2 — Turbidimetria
df_turb = pd.DataFrame({
    "FD":                   [int(v)   for v in fds],
    "pct_T_suspensao":      [float(t[1]) for t in TURBIDIA],
    "Abs_suspensao":        [float(v) for v in abs_susp_list],
    "pct_T_sobrenadante":   [float(t[2]) for t in TURBIDIA],
    "Abs_sobrenadante":     [float(v) for v in abs_sob_list],
    "Abs_corrigida":        [float(v) for v in abs_corr_list],
    "C_real_gL":            [float(v) for v in conc_real_list],
})

# Aba 3 — Curva padrão
df_curva = pd.DataFrame({
    "FD":            [int(v)   for v in fds],
    "Abs_corrigida": [float(v) for v in abs_corr_list],
    "C_real_gL":     [float(v) for v in conc_real_list],
    "C_curva_gL":    [float(v) for v in c_curva_list],
    "Erro_abs_gL":   [float(v) for v in erros_abs],
    "Erro_pct":      [float(v) for v in erros_pct],
})
df_curva = pd.concat([df_curva, pd.DataFrame([
    {"FD": "Equação", "Abs_corrigida": None, "C_real_gL": None,
     "C_curva_gL": f"C={a:.4f}*A{COMPRIMENTO_ONDA_NM}{sinal}{ab:.4f}",
     "Erro_abs_gL": None, "Erro_pct": None},
    {"FD": "R²",      "Abs_corrigida": None, "C_real_gL": None,
     "C_curva_gL": float(r2),
     "Erro_abs_gL": None, "Erro_pct": None},
])], ignore_index=True)

FMT4   = "0.0000"
FMT2   = "0.00"
FMT_SC = "0.0000E+00"

COL_FMTS = {
    "Gravimetria": {
        "Massa_tubo_g": FMT4, "Massa_total_g": FMT4,
        "Biomassa_g":   FMT4, "Volume_L":      FMT4,
        "Concentracao_gL": FMT4,
    },
    "Turbidimetria": {
        "pct_T_suspensao":    FMT2,
        "Abs_suspensao":      FMT4,
        "pct_T_sobrenadante": FMT2,
        "Abs_sobrenadante":   FMT_SC,
        "Abs_corrigida":      FMT4,
        "C_real_gL":          FMT4,
    },
    "Curva_padrao": {
        "Abs_corrigida": FMT4,
        "C_real_gL":     FMT4,
        "C_curva_gL":    FMT4,
        "Erro_abs_gL":   FMT4,
        "Erro_pct":      FMT2,
    },
}

fname = "resultados_curva_padrao.xlsx"
with pd.ExcelWriter(fname, engine="openpyxl") as writer:
    df_grav.to_excel( writer, sheet_name="Gravimetria",   index=False)
    df_turb.to_excel( writer, sheet_name="Turbidimetria", index=False)
    df_curva.to_excel(writer, sheet_name="Curva_padrao",  index=False)

    for sheet_name, fmt_map in COL_FMTS.items():
        ws = writer.sheets[sheet_name]
        headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

        for col_name, num_fmt in fmt_map.items():
            if col_name not in headers:
                continue
            col_idx = headers.index(col_name) + 1
            for row in ws.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx):
                for cell in row:
                    if isinstance(cell.value, float):
                        cell.number_format = num_fmt

        for col in ws.columns:
            max_len = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in col
            )
            ws.column_dimensions[col[0].column_letter].width = max(max_len + 4, 16)

print(f"  Planilha salva: {fname}  (3 abas: Gravimetria | Turbidimetria | Curva_padrao)")
print(f"\n{SEP}")
