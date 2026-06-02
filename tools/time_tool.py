from datetime import datetime
import pytz

def get_current_time(timezone: str = "Asia/Kuala_Lumpur") -> str:
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_timezone_info(timezone: str = "Asia/Kuala_Lumpur") -> str:
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        offset = now.strftime('%z')
        return f"Timezone: {timezone}\nOffset: {offset}\nCurrent: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error: {str(e)}"