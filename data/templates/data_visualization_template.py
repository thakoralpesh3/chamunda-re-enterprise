#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matplotlib Autonomous Chart Generator for Aradhya
Produces publication-quality charts for dealership metrics, finance & system performance.
"""
import sys
from pathlib import Path

def generate_bar_chart(categories: list, values: list, title: str, xlabel: str, ylabel: str, output_png: Path):
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend safe for background execution
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    bars = ax.bar(categories, values, color=colors[:len(categories)], edgecolor="black", linewidth=0.8)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=8)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png)
    plt.close()
    return str(output_png)

if __name__ == "__main__":
    cats = ["J-Series 350", "650 Twins", "Sherpa 450", "UCE 350", "Cast Iron"]
    vals = [42, 18, 14, 25, 9]
    out = Path("/home/alpesh/chamunda_re_enterprise/data/missions/demo_chart.png")
    res = generate_bar_chart(cats, vals, "Chamunda RE Monthly Workshop Job Cards by Platform", "Engine Platform", "Bikes Serviced", out)
    print(f"Chart saved successfully: {res}")
