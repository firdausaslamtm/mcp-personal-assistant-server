from tools.time_tool import get_current_time
from tools.weather_tool import get_weather
from tools.notes_tool import add_note, list_notes
from tools.system_tool import get_system_info

print("Current time in Asia/Kuala_Lumpur:", get_current_time())
print()
print(get_weather("Putrajaya"))
print()
print(add_note("Test note from CLI"))
print()
print(list_notes())
print()
print(get_system_info())