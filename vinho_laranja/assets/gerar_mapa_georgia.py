"""Desenha o mapa factual da Geórgia com limites públicos do Natural Earth.

Execute com Python, NumPy e Matplotlib: python assets/gerar_mapa_georgia.py
Os dados locais permitem regenerar a figura sem acesso à rede.
O globo usa projeção ortográfica; o detalhe usa latitude/longitude, com a
proporção corrigida para a latitude média de 42 graus norte.
"""

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/vinho-laranja-matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch
from matplotlib.path import Path as PlotPath
import numpy as np


ASSETS = Path(__file__).resolve().parent
DATA = json.loads((ASSETS / "mapa_georgia_dados.json").read_text())
INK = "#362722"
AMBER = "#ac4c16"
HONEY = "#e3a740"
LAND = "#ece6da"
WATER = "#e2edf0"
COAST = "#aba697"
SEA_TEXT = "#536f7b"


def globe_projection(lon, lat):
    """Orthographic projection, central longitude 20E and latitude 20N."""
    lon = np.deg2rad(lon) - np.deg2rad(20)
    lat = np.deg2rad(lat)
    lat0 = np.deg2rad(20)
    x = np.cos(lat) * np.sin(lon)
    y = np.cos(lat0) * np.sin(lat) - np.sin(lat0) * np.cos(lat) * np.cos(lon)
    visible = np.sin(lat0) * np.sin(lat) + np.cos(lat0) * np.cos(lat) * np.cos(lon) >= 0
    return x, y, visible


def globe_image(resolution=500):
    # Inverse-project each visible pixel; avoids incorrectly closing polygons
    # across the horizon of the globe.
    grid = np.linspace(-1, 1, resolution)
    x, y = np.meshgrid(grid, grid)
    radius = np.hypot(x, y)
    visible = radius <= 1
    x, y, radius = x[visible], y[visible], radius[visible]
    c = np.arcsin(radius)
    lat0 = np.deg2rad(20)
    lat = np.arcsin(np.cos(c) * np.sin(lat0) + y * np.sin(c) * np.cos(lat0) / radius)
    lon = np.deg2rad(20) + np.arctan2(
        x * np.sin(c), radius * np.cos(lat0) * np.cos(c) - y * np.sin(lat0) * np.sin(c)
    )
    points = np.column_stack(((np.rad2deg(lon) + 180) % 360 - 180, np.rad2deg(lat)))
    land = np.zeros(len(points), dtype=bool)
    for country in DATA["world"]:
        for polygon in country["polygons"]:
            exterior = np.asarray(polygon[0])
            lo, hi = exterior.min(axis=0), exterior.max(axis=0)
            candidate = np.all((points >= lo) & (points <= hi), axis=1)
            indices = np.flatnonzero(candidate)
            if not len(indices):
                continue
            inside = PlotPath(exterior).contains_points(points[indices])
            for hole in polygon[1:]:
                inside &= ~PlotPath(hole).contains_points(points[indices])
            land[indices[inside]] = True
    rgba = np.zeros((resolution, resolution, 4))
    pixels = np.tile(matplotlib.colors.to_rgba(WATER), (len(points), 1))
    pixels[land] = matplotlib.colors.to_rgba("#b8b8a4")
    rgba[visible] = pixels
    return rgba


def country_path(polygon):
    # Natural Earth supplies opposite winding for interiors and exterior rings.
    vertices, codes = [], []
    for ring in polygon:
        vertices.extend(ring)
        codes.extend([PlotPath.MOVETO] + [PlotPath.LINETO] * (len(ring) - 2) + [PlotPath.CLOSEPOLY])
    return PlotPath(vertices, codes)


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    fig = plt.figure(figsize=(7.2 / 2.54, 4.8 / 2.54), dpi=320, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(WATER)
    for country in DATA["region"]:
        georgia = country["iso"] == "GEO"
        for polygon in country["polygons"]:
            ax.add_patch(PathPatch(
                country_path(polygon), facecolor=HONEY if georgia else LAND,
                edgecolor=AMBER if georgia else COAST,
                linewidth=0.85 if georgia else 0.42, zorder=3 if georgia else 1,
            ))
    ax.set_xlim(32.5, 54.5)
    ax.set_ylim(36.5, 47.35)
    ax.set_aspect(1 / np.cos(np.deg2rad(42)))
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    def label(lon, lat, text, size=7.1, **kwargs):
        ax.text(lon, lat, text, ha="center", va="center", fontsize=size,
                color=kwargs.pop("color", INK), zorder=5, **kwargs)

    label(44.0, 43.7, "GEÓRGIA", 10.5, weight="bold", color=AMBER)
    label(47.7, 45.4, "RÚSSIA", 7.6)
    label(38.3, 39.0, "TURQUIA", 7.6)
    label(43.9, 39.5, "ARMÊNIA", 7)
    label(49.5, 40.7, "AZERBAIJÃO", 6.6)
    label(48.5, 37.4, "IRÃ", 7.2)
    label(35.8, 42.25, "Mar\nNegro", 8.7, color=SEA_TEXT, style="italic")
    label(52.4, 43.2, "Mar\nCáspio", 8, color=SEA_TEXT, style="italic")
    # Capital coordinates: Tbilisi, 41.7151 N / 44.8271 E.
    ax.plot(44.8271, 41.7151, "o", ms=2.5, color=INK, zorder=6)
    ax.annotate("Tbilisi", (44.8271, 41.7151), xytext=(4, -7),
                textcoords="offset points", fontsize=6.5, color=INK, zorder=6)
    ax.annotate("N", xy=(53.55, 46.1), xytext=(53.55, 45.25), ha="center",
                fontsize=6.6, color=SEA_TEXT,
                arrowprops={"arrowstyle": "-|>", "lw": 0.6, "color": SEA_TEXT})

    # Small global locator in a white inset, clear of Georgia and its neighbors.
    panel = FancyBboxPatch((0.012, 0.635), 0.270, 0.361,
                          boxstyle="round,pad=0.008,rounding_size=0.018",
                          transform=fig.transFigure, facecolor="white",
                          edgecolor="none", zorder=8)
    fig.add_artist(panel)
    globe = fig.add_axes([0.026, 0.695, 0.239, 0.286], zorder=9)
    globe.imshow(globe_image(), extent=(-1, 1, -1, 1), origin="lower")
    sphere = Circle((0, 0), 1, fill=False, edgecolor="#8fa3a7", lw=0.5)
    globe.add_patch(sphere)
    for longitude in range(-180, 181, 30):
        xx, yy, front = globe_projection(longitude, np.linspace(-90, 90, 361))
        globe.plot(np.where(front, xx, np.nan), np.where(front, yy, np.nan),
                   color="white", alpha=0.45, lw=0.3)
    for latitude in range(-60, 91, 30):
        xx, yy, front = globe_projection(np.linspace(-180, 180, 721), latitude)
        globe.plot(np.where(front, xx, np.nan), np.where(front, yy, np.nan),
                   color="white", alpha=0.45, lw=0.3)
    gx, gy, _ = globe_projection(43.5, 42.2)
    globe.plot(gx, gy, "o", ms=6.5, color="white", zorder=11)
    globe.plot(gx, gy, "o", ms=4.2, color=AMBER, zorder=12)
    globe.set_xlim(-1.04, 1.04)
    globe.set_ylim(-1.04, 1.04)
    globe.set_axis_off()
    fig.text(0.145, 0.659, "Visão global", ha="center", va="center",
             fontsize=6.7, color=SEA_TEXT, zorder=10)
    destination = ASSETS / "mapa_georgia.png"
    fig.savefig(destination, dpi=320, facecolor="white")
    plt.close(fig)
    print(destination)


if __name__ == "__main__":
    main()
