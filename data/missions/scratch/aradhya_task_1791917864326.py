import os, sys
os.environ['MPLBACKEND'] = 'Agg'
try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    pass

import os, sys, datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

print("🚀 [Aradhya Worker] Initializing Autonomous Data & Plotting Engine...")

# Directive: Create a chart comparing Royal Enfield bike sales and calculate average revenue
categories = ["Classic 350", "Hunter 350", "Interceptor 650", "Himalayan 450", "Continental GT"]
sales_count = [54, 38, 22, 19, 14]
total_revenue_lakhs = [118.8, 68.4, 74.8, 62.7, 51.8]

# Create CSV Dataset
out_csv = "/home/alpesh/chamunda_re_enterprise/data/missions/motorcycle_fleet_metrics.csv"
os.makedirs(os.path.dirname(out_csv), exist_ok=True)
df = pd.DataFrame({
    "Model": categories,
    "Units_Sold": sales_count,
    "Revenue_Lakhs": total_revenue_lakhs
})
df.to_csv(out_csv, index=False)
print(f"✅ Dataset successfully created: {out_csv}")
print(f"• Total Units: {df['Units_Sold'].sum()} | Total Revenue: ₹{df['Revenue_Lakhs'].sum():.1f} Lakhs")

# Generate Chart PNG
out_png = "/home/alpesh/chamunda_re_enterprise/data/missions/fleet_sales_performance.png"
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=140)
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
bars = ax.bar(categories, sales_count, color=colors, edgecolor="black", linewidth=0.8)

ax.set_title("Chamunda Automobile • Royal Enfield Fleet Units Sold", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Motorcycle Model", fontsize=10, labelpad=8)
ax.set_ylabel("Units Delivered", fontsize=10, labelpad=8)
ax.grid(axis="y", linestyle="--", alpha=0.5)

for bar in bars:
    h = bar.get_height()
    ax.annotate(f"{h} units", xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig(out_png)
plt.close()
print(f"📊 Visualization generated & saved: {out_png}")
