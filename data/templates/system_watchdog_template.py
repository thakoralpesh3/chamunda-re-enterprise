#!/usr/bin/env python3
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
