import OLED
import time

try:
    time.sleep(1)
    text = f"Roll: 89°\nPitch: 91°"
    OLED.clear_display()
    OLED.print_on_OLED(text)
    OLED.OLED_show()

except KeyboardInterrupt:
    exit()
