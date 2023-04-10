import OLED
import time

try:
    time.sleep(1)

    # text = f"Roll: 89°\nPitch: 91°"
    text = f"Num Passes = 3\nAvg. Time/Pass = 16.23 s\nAvg. Force = 2.2 lbf\nAvg. Roll Angle = 89°"
    OLED.clear_display()
    OLED.print_on_OLED(text)
    OLED.OLED_show()

except KeyboardInterrupt:
    exit()
