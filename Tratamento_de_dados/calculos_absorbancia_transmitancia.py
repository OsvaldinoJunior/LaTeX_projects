"""
=============================================================
  CURVA PADRÃO DE BIOMASSA — SCRIPT REUTILIZÁVEL
=============================================================
  Realiza todos os cálculos do relatório:
    1. Biomassa seca por gravimetria (triplicata)
    2. Absorbância a partir de transmitância (%T)
    3. Absorbância corrigida (suspensão − sobrenadante)
    4. Concentração por fator de diluição
    5. Regressão linear e R²
    6. Geração do gráfico da curva padrão

  Como usar:
    - Edite apenas a seção "DADOS DE ENTRADA" abaixo
    - Execute:  python curva_padrao_biomassa.py
    - Gera:     resultados.txt  e  curva_padrao.png
=============================================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# ============================================================
#  DADOS DE ENTRADA — edite esta seção para novo experimento
# ============================================================

MICROORGANISMO = "Saccharomyces cerevisiae ATCC 7754"
COMPRIMENTO_ONDA = 600   # nm
VOLUME_ALIQUOTA  = 0.010 # L (alíquota usada para massa seca)

# --- Tubos para biomassa seca ---
# Cada tupla: (massa_tubo_g, massa_total_g)
TUBOS = [
    (5.5053, 5.5341),  # Tubo 1
    (5.3147, 5.3420),  # Tubo 2
    (5.4825, 5.5095),  # Tubo 3
]

# --- Diluições e leituras de transmitância (%T) ---
# Cada tupla: (fator_diluicao, %T_suspensao, %T_sobrenadante)
DILUICOES = [
    (  5, 18.12, 97.95),
    ( 10, 39.70, 98.85),
    ( 15, 59.55, 99.40),
    ( 25, 65.57, 99.20),
    ( 50, 81.95, 99.85),
    (100, 91.25, 99.95),
]

# ============================================================
#  FUNÇÕES DE CÁLCULO
# ============================================================

def transmitancia_para_absorbancia(pct_T):
    """Converte %T em absorbância: A = 2 - log(%T)"""
    if pct_T <= 0 or pct_T >= 100:
        raise ValueError(f"%T={pct_T} fora do intervalo válido (0, 100)")
    return 2 - math.log10(pct_T)


def calcular_biomassa_seca(tubos, volume_L):
    """
    Calcula biomassa seca e concentração para cada tubo.
    Retorna lista de dicts e a concentração média (g/L).
    """
    resultados = []
    for i, (m_tubo, m_total) in enumerate(tubos, start=1):
        biomassa = round(m_total - m_tubo, 4)
        concentracao = round(biomassa / volume_L, 4)
        resultados.append({
            "tubo":        i,
            "m_tubo_g":    m_tubo,
            "m_total_g":   m_total,
            "biomassa_g":  biomassa,
            "volume_L":    volume_L,
            "conc_gL":     concentracao,
        })
    media = round(sum(r["conc_gL"] for r in resultados) / len(resultados), 4)
    return resultados, media


def calcular_absorbancia(diluicoes, conc_media_gL):
    """
    Para cada diluição calcula:
      - Absorbância da suspensão
      - Absorbância do sobrenadante
      - Absorbância corrigida
      - Concentração diluída (g/L)
    """
    resultados = []
    for fd, pct_T_susp, pct_T_sobre in diluicoes:
        A_susp  = round(transmitancia_para_absorbancia(pct_T_susp),  4)
        A_sobre = round(transmitancia_para_absorbancia(pct_T_sobre), 6)
        A_corr  = round(A_susp - A_sobre, 4)
        conc    = round(conc_media_gL / fd, 4)
        resultados.append({
            "fd":           fd,
            "pct_T_susp":   pct_T_susp,
            "A_susp":       A_susp,
            "pct_T_sobre":  pct_T_sobre,
            "A_sobre":      A_sobre,
            "A_corrigida":  A_corr,
            "conc_gL":      conc,
        })
    return resultados


def regressao_linear(x_vals, y_vals):
    """
    Regressão linear y = a*x + b.
    Retorna coeficientes (a, b) e R².
    """
    x = np.array(x_vals)
    y = np.array(y_vals)
    a, b = np.polyfit(x, y, 1)
    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    R2 = 1 - ss_res / ss_tot
    return round(a, 4), round(b, 4), round(R2, 4)


def gerar_grafico(abs_vals, conc_vals, a, b, R2, microorganismo, comprimento_onda,
                  arquivo_saida="curva_padrao.png"):
    """Gera e salva o gráfico da curva padrão."""
    A_fit = np.linspace(0, max(abs_vals) * 1.1, 300)
    C_fit = a * A_fit + b

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(abs_vals, conc_vals, color="black", zorder=5, s=55,
               label="Dados experimentais")
    equacao = f"$C = {a}\\cdot A_{{{comprimento_onda}}} + ({b})$\n$R^2 = {R2}$"
    ax.plot(A_fit, C_fit, color="black", linewidth=1.3, label=equacao)

    ax.set_xlabel(f"Absorbância ({comprimento_onda} nm)", fontsize=11)
    ax.set_ylabel("Concentração de biomassa (g/L)", fontsize=11)
    ax.set_title(f"Curva Padrão — {microorganismo}", fontsize=10, style="italic")
    ax.legend(fontsize=10, frameon=True)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=180, bbox_inches="tight")
    plt.close()
    return arquivo_saida


def formatar_sci(valor):
    """Formata número em notação científica legível."""
    if valor == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(valor))))
    mant = valor / (10 ** exp)
    return f"{mant:.2f}×10^{exp}"


# ============================================================
#  EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    linhas = []
    sep = "=" * 62

    linhas.append(sep)
    linhas.append("  CURVA PADRÃO DE BIOMASSA — RESULTADOS")
    linhas.append(f"  Microrganismo : {MICROORGANISMO}")
    linhas.append(f"  Data          : {date.today().strftime('%d/%m/%Y')}")
    linhas.append(sep)

    # ── 1. Biomassa seca ───────────────────────────────────
    linhas.append("\n[ 1 ] BIOMASSA SECA (MÉTODO GRAVIMÉTRICO)\n")
    linhas.append(
        f"  {'Tubo':<6} {'m_tubo(g)':<12} {'m_total(g)':<12} "
        f"{'Biomassa(g)':<13} {'Volume(L)':<11} {'Conc.(g/L)'}"
    )
    linhas.append("  " + "-" * 58)

    res_tubos, conc_media = calcular_biomassa_seca(TUBOS, VOLUME_ALIQUOTA)
    for r in res_tubos:
        linhas.append(
            f"  {r['tubo']:<6} {r['m_tubo_g']:<12.4f} {r['m_total_g']:<12.4f} "
            f"{r['biomassa_g']:<13.4f} {r['volume_L']:<11.3f} {r['conc_gL']:.4f}"
        )
    linhas.append("  " + "-" * 58)
    linhas.append(f"  {'Média':>54}  {conc_media:.4f} g/L")

    # ── 2. Absorbâncias ────────────────────────────────────
    linhas.append("\n[ 2 ] ABSORBÂNCIAS E ABSORBÂNCIA CORRIGIDA\n")
    linhas.append(
        f"  {'FD':<6} {'%T susp':<10} {'A susp':<10} "
        f"{'%T sobre':<11} {'A sobre':<14} {'A corrig':<10} {'Conc.(g/L)'}"
    )
    linhas.append("  " + "-" * 72)

    res_abs = calcular_absorbancia(DILUICOES, conc_media)
    for r in res_abs:
        linhas.append(
            f"  {r['fd']:<6} {r['pct_T_susp']:<10.2f} {r['A_susp']:<10.4f} "
            f"{r['pct_T_sobre']:<11.2f} {formatar_sci(r['A_sobre']):<14} "
            f"{r['A_corrigida']:<10.4f} {r['conc_gL']:.4f}"
        )

    # ── 3. Regressão linear ────────────────────────────────
    abs_corr = [r["A_corrigida"] for r in res_abs]
    concs    = [r["conc_gL"]     for r in res_abs]

    a, b, R2 = regressao_linear(abs_corr, concs)
    sinal_b = "+" if b >= 0 else "-"

    linhas.append("\n[ 3 ] REGRESSÃO LINEAR\n")
    linhas.append(f"  Equação : C = {a} · A_{COMPRIMENTO_ONDA} {sinal_b} {abs(b)}")
    linhas.append(f"  R²      : {R2}")

    qualidade = (
        "Excelente (R² ≥ 0,99)" if R2 >= 0.99 else
        "Bom (0,95 ≤ R² < 0,99)" if R2 >= 0.95 else
        "Aceitável (0,90 ≤ R² < 0,95)" if R2 >= 0.90 else
        "Ruim (R² < 0,90) — revisar dados"
    )
    linhas.append(f"  Qualidade: {qualidade}")

    # ── 4. Gráfico ─────────────────────────────────────────
    arquivo_png = gerar_grafico(
        abs_corr, concs, a, b, R2,
        MICROORGANISMO, COMPRIMENTO_ONDA
    )
    linhas.append(f"\n[ 4 ] GRÁFICO\n")
    linhas.append(f"  Salvo em: {arquivo_png}")

    linhas.append("\n" + sep)

    # ── Exibe e salva ──────────────────────────────────────
    saida = "\n".join(linhas)
    print(saida)

    with open("resultados.txt", "w", encoding="utf-8") as f:
        f.write(saida)
    print("\n  Resultados também salvos em: resultados.txt")


if __name__ == "__main__":
    main()
