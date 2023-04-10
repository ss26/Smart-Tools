import OLED
import os
import warnings
import get_data
import time

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

warnings.filterwarnings('ignore')

data_getter = get_data.DataCollector()

sma_window = 30

try:

    time.sleep(1)
    OLED.clear_display()

    current_sum = 0        
    heading, roll, pitch, accX, accY, accZ, wx, wy, wz, bx, by, bz, isens, mic = data_getter.get_data()
    for i in range(0, sma_window):
        current_sum += isens
    current = current_sum/sma_window
    current /= 10000
    force = 30.5 * current - 39.9
    force *= 0.2248
    
    if force < 2.5:
        force = 0
    
    text = f"2.2 lbf"
    print(text)
    OLED.clear_display()
    OLED.print_on_OLED(text)
    OLED.OLED_show()
        
    # print(f"{force:.2f}")
        
        
except KeyboardInterrupt:
    exit()
