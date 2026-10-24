"""
Synthesized Skill: system_health_hud
Description: Visual diagnostic HUD for laptop CPU/RAM/Disk.
Synthesized autonomously by Aradhya.
"""

def system_health_hud() -> dict:
    """Returns quick visual snapshot of CPU, RAM, and disk storage."""
    import psutil
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_used_pct": vm.percent,
        "ram_available_mb": round(vm.available / (1024*1024), 1),
        "disk_free_gb": round(disk.free / (1024**3), 1),
        "status": "OPTIMAL" if vm.percent < 85 else "HIGH_LOAD"
    }
