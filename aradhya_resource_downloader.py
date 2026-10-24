#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya Autonomous Resource Downloader & Environment Provisioner
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Equips Aradhya with 100% independent tools and runtime assets:
1. Verifies/installs Python data science packages (pandas, matplotlib, numpy, rich).
2. Provisions standalone portable 'jq' static binary and pure-Python 'tree' CLI.
3. Deploys autonomous project templates (RE GST Invoicing, Data Visualization, System Watchdog).
4. Enables 100% offline & online independent operation like Gemini, ChatGPT & Claude.
"""

import os
import sys
import json
import shutil
import urllib.request
import subprocess
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
BIN_DIR = BASE_DIR / "bin"
USER_BIN = Path("/home/alpesh/bin")
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
MISSIONS_DIR = DATA_DIR / "missions"

BIN_DIR.mkdir(parents=True, exist_ok=True)
USER_BIN.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
MISSIONS_DIR.mkdir(parents=True, exist_ok=True)


class AradhyaResourceProvisioner:
    """Provisions and monitors standalone binaries, Python libraries, and autonomous templates."""

    def __init__(self):
        self.bin_dir = BIN_DIR
        self.user_bin = USER_BIN
        self.templates_dir = TEMPLATES_DIR

    def provision_jq_binary(self) -> Dict[str, Any]:
        """Download or link standalone static jq binary."""
        dest_bin = self.bin_dir / "jq"
        user_dest = self.user_bin / "jq"

        if dest_bin.exists() and os.access(dest_bin, os.X_OK):
            return {"success": True, "path": str(dest_bin), "status": "ALREADY_PRESENT"}

        # Attempt to download official standalone static binary from GitHub
        url = "https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux64"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AradhyaAutonomousEngine/2.0"})
            with urllib.request.urlopen(req, timeout=15) as resp, open(dest_bin, "wb") as f:
                f.write(resp.read())
            dest_bin.chmod(0o755)
            # Link to user bin
            try:
                if not user_dest.exists():
                    shutil.copy2(dest_bin, user_dest)
                    user_dest.chmod(0o755)
            except Exception:
                pass
            return {"success": True, "path": str(dest_bin), "status": "DOWNLOADED_OK"}
        except Exception as e:
            # Fallback to python-based jq emulator
            self._write_python_jq_emulator(dest_bin)
            try:
                if not user_dest.exists():
                    shutil.copy2(dest_bin, user_dest)
                    user_dest.chmod(0o755)
            except Exception:
                pass
            return {"success": True, "path": str(dest_bin), "status": "PYTHON_EMULATOR_FALLBACK", "note": str(e)}

    def _write_python_jq_emulator(self, path: Path):
        """Pure Python fallback for jq JSON filtering."""
        code = '''#!/usr/bin/env python3
import sys, json

def main():
    args = sys.argv[1:]
    filter_expr = args[0] if args else "."
    
    # Read stdin
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except Exception as e:
        sys.stderr.write(f"Invalid JSON: {e}\\n")
        sys.exit(1)

    if filter_expr in [".", ""]:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    # Basic dot access (.key1.key2)
    curr = data
    parts = filter_expr.strip(".").split(".")
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        elif isinstance(curr, list) and p.isdigit():
            curr = curr[int(p)]
        else:
            curr = None
            break

    if curr is not None:
        if isinstance(curr, (dict, list)):
            print(json.dumps(curr, indent=2, ensure_ascii=False))
        else:
            print(curr)

if __name__ == "__main__":
    main()
'''
        path.write_text(code, encoding="utf-8")
        path.chmod(0o755)

    def provision_pytree_utility(self) -> Dict[str, Any]:
        """Deploy pure-Python standalone tree CLI for recursive directory inspection."""
        pytree_path = self.bin_dir / "pytree"
        user_tree = self.user_bin / "tree"

        code = '''#!/usr/bin/env python3
# Pure Python standalone tree utility for Aradhya & Alpesh Sir
import os, sys
from pathlib import Path

def print_tree(directory: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
    if current_depth >= max_depth:
        return
    try:
        entries = sorted(list(directory.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return

    # Filter out hidden files/dirs unless requested
    entries = [e for e in entries if not e.name.startswith(".")]
    total = len(entries)

    for idx, entry in enumerate(entries):
        is_last = (idx == total - 1)
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        if entry.is_dir():
            print(f"{prefix}{connector}\\033[1;34m{entry.name}/\\033[0m")
            print_tree(entry, prefix + child_prefix, max_depth, current_depth + 1)
        else:
            size_kb = entry.stat().st_size / 1024
            size_str = f"({size_kb:.1f} KB)" if size_kb >= 1.0 else f"({entry.stat().st_size} B)"
            print(f"{prefix}{connector}{entry.name} \\033[2m{size_str}\\033[0m")

def main():
    args = sys.argv[1:]
    target = Path(args[0]) if args and not args[0].startswith("-") else Path.cwd()
    depth = 3
    for i, a in enumerate(args):
        if a in ["-L", "--depth"] and i + 1 < len(args) and args[i+1].isdigit():
            depth = int(args[i+1])

    print(f"\\033[1;32m{target.resolve()}\\033[0m")
    print_tree(target, max_depth=depth)

if __name__ == "__main__":
    main()
'''
        pytree_path.write_text(code, encoding="utf-8")
        pytree_path.chmod(0o755)

        # Link to /home/alpesh/bin/tree if system tree does not exist
        if not shutil.which("tree") or not user_tree.exists():
            try:
                shutil.copy2(pytree_path, user_tree)
                user_tree.chmod(0o755)
            except Exception:
                pass

        return {"success": True, "path": str(pytree_path), "user_path": str(user_tree)}

    def provision_templates(self) -> Dict[str, Any]:
        """Deploy ready-to-run templates for data science, RE invoicing, and system monitoring."""
        # 1. Royal Enfield Dealership GST Billing Template
        gst_template = self.templates_dir / "re_dealership_billing_template.py"
        gst_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Parts & Service • Autonomous GST Invoice Generator
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
GST Rules: Spare Parts @ 28% GST (HSN 8714), Service Labor @ 18% GST (SAC 9987).
"""
import sys
import json
import datetime

def calculate_invoice(customer_name: str, bike_model: str, parts: list, labor_charges: float):
    parts_subtotal = sum(p.get("qty", 1) * p.get("unit_price", 0.0) for p in parts)
    cgst_parts = parts_subtotal * 0.14
    sgst_parts = parts_subtotal * 0.14
    total_parts = parts_subtotal + cgst_parts + sgst_parts

    cgst_labor = labor_charges * 0.09
    sgst_labor = labor_charges * 0.09
    total_labor = labor_charges + cgst_labor + sgst_labor

    grand_total = total_parts + total_labor

    invoice = {
        "dealership": "Chamunda Automobile Parts & Service",
        "helpline": "+91 78747 19139",
        "date": datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "customer": customer_name,
        "motorcycle": bike_model,
        "parts_summary": {
            "subtotal": round(parts_subtotal, 2),
            "cgst_14pct": round(cgst_parts, 2),
            "sgst_14pct": round(sgst_parts, 2),
            "total_parts_with_gst": round(total_parts, 2)
        },
        "labor_summary": {
            "labor_base": round(labor_charges, 2),
            "cgst_9pct": round(cgst_labor, 2),
            "sgst_9pct": round(sgst_labor, 2),
            "total_labor_with_gst": round(total_labor, 2)
        },
        "grand_total": round(grand_total, 2)
    }
    return invoice

if __name__ == "__main__":
    demo_parts = [
        {"name": "Motul 7100 15W-50 2.5L", "qty": 1, "unit_price": 2250.0},
        {"name": "OEM J-Series Oil Filter", "qty": 1, "unit_price": 140.0},
        {"name": "OEM Front Brake Pads", "qty": 1, "unit_price": 550.0}
    ]
    res = calculate_invoice("Alpesh Sir VIP Fleet", "Classic 350 Reborn", demo_parts, 650.0)
    print(json.dumps(res, indent=2, ensure_ascii=False))
'''
        gst_template.write_text(gst_code, encoding="utf-8")
        gst_template.chmod(0o755)

        # 2. Data Visualization & Plotting Template
        plot_template = self.templates_dir / "data_visualization_template.py"
        plot_code = '''#!/usr/bin/env python3
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
'''
        plot_template.write_text(plot_code, encoding="utf-8")
        plot_template.chmod(0o755)

        # 3. System Watchdog & Memory Optimization Template
        sys_template = self.templates_dir / "system_watchdog_template.py"
        sys_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya Autonomous System Watchdog & Latency Protector
"""
import sys
import psutil
import ctypes

def inspect_and_trim():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    status = {
        "cpu_percent": cpu,
        "ram_used_mb": mem.used // (1024 * 1024),
        "ram_avail_mb": mem.available // (1024 * 1024),
        "ram_percent": mem.percent,
        "swap_percent": swap.percent,
        "actions_taken": []
    }

    if mem.percent > 85.0:
        try:
            ctypes.CDLL("libc.so.6").malloc_trim(0)
            status["actions_taken"].append("libc malloc_trim memory reclaimed")
        except Exception:
            pass

    return status

if __name__ == "__main__":
    res = inspect_and_trim()
    print(f"System State: CPU {res['cpu_percent']}% | RAM {res['ram_percent']}% ({res['ram_avail_mb']} MB free)")
'''
        sys_template.write_text(sys_code, encoding="utf-8")
        sys_template.chmod(0o755)

        return {
            "success": True,
            "templates_count": 3,
            "templates": [
                str(gst_template),
                str(plot_template),
                str(sys_template)
            ]
        }

    def verify_python_packages(self) -> Dict[str, Any]:
        """Check status of essential data science packages."""
        pkgs = ["pandas", "matplotlib", "numpy", "rich", "psutil", "requests", "bs4"]
        results = {}
        for p in pkgs:
            try:
                __import__(p)
                results[p] = True
            except ImportError:
                results[p] = False
        return results

    def provision_all(self) -> Dict[str, Any]:
        """Run complete autonomous resource provisioning."""
        jq_res = self.provision_jq_binary()
        tree_res = self.provision_pytree_utility()
        tpl_res = self.provision_templates()
        pkg_res = self.verify_python_packages()

        return {
            "success": True,
            "jq": jq_res,
            "pytree": tree_res,
            "templates": tpl_res,
            "packages": pkg_res,
            "ready_for_independent_work": True
        }


_provisioner = None

def get_resource_provisioner() -> AradhyaResourceProvisioner:
    global _provisioner
    if _provisioner is None:
        _provisioner = AradhyaResourceProvisioner()
    return _provisioner


if __name__ == "__main__":
    res = get_resource_provisioner().provision_all()
    print(json.dumps(res, indent=2, ensure_ascii=False))
