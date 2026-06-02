import platform
import sys
import psutil
from datetime import datetime

def get_system_info() -> str:
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        info = [
            f"OS: {platform.system()} {platform.release()}",
            f"Python: {sys.version.split()[0]}",
            f"CPU: {psutil.cpu_percent(interval=1)}% usage",
            f"Memory: {psutil.virtual_memory().percent}% used",
            f"Uptime: {str(uptime).split('.')[0]}"
        ]
        return "\n".join(info)
    except Exception as e:
        return f"Error: {str(e)}"