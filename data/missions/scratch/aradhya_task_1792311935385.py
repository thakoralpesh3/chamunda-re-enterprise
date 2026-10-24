import os, sys
os.environ['MPLBACKEND'] = 'Agg'
try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    pass
import os
import sys
import pandas as pd
from datetime import datetime

# Configuration
TARGET_DIR = "/home/alpesh"
SIZE_THRESHOLD_MB = 50  # Define large file threshold (50 MB)
OUTPUT_DIR = "/home/alpesh/chamunda_re_enterprise/data/missions"

def find_large_files():
    print(f"[*] Chamunda Automobile Parts & Service - Storage Audit Initiated")
    print(f"[*] Target Directory: {TARGET_DIR}")
    print(f"[*] Threshold: Files larger than {SIZE_THRESHOLD_MB} MB\n")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    large_files = []
    
    threshold_bytes = SIZE_THRESHOLD_MB * 1024 * 1024
    
    for root, dirs, files in os.walk(TARGET_DIR):
        # Skip hidden virtual environments or git directories if necessary to speed up
        if '.git' in root or '.cache' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if os.path.islink(filepath):
                    continue
                file_size = os.path.getsize(filepath)
                if file_size >= threshold_bytes:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                    large_files.append({
                        'File Name': file,
                        'Path': filepath,
                        'Size (MB)': round(file_size / (1024 * 1024), 2),
                        'Last Modified': mod_time
                    })
            except (PermissionError, FileNotFoundError):
                continue

    if not large_files:
        print("[+] No files found exceeding the specified size threshold.")
        return

    df = pd.DataFrame(large_files)
    df = df.sort_values(by='Size (MB)', ascending=False)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_csv = os.path.join(OUTPUT_DIR, f"large_files_audit_{timestamp}.csv")
    df.to_csv(output_csv, index=False)
    
    print(f"[+] Audit Complete. Found {len(df)} large files.")
    print(f"[+] Report saved successfully at: {output_csv}\n")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    find_large_files()