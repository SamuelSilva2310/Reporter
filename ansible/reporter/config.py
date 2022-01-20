import psutil
import os

CPU_COUNT = psutil.cpu_count()
headers = {
    "Time": ["Time Log"],
    "CPU": CPU_COUNT,
    "RAM": ["Ram %"],
    "DISK": ["Disk Read Time (ms)", "Disk Write Time (ms)", "Disk Read count", "Disk Write Count"],
    "NETWORK": ["bytes sent ", "bytes received", "errin", "errout", "dropin", "dropout"]
}

OUTPUT_DIR_CSV = os.path.join("Output", 'exports')
