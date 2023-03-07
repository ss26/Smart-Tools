from process_data import Preprocess
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
    while True:
        time.sleep(1)
        OLED.clear_display()

        current_sum = 0        
        heading, roll, pitch, accX, accY, accZ, wx, wy, wz, bx, by, bz, isens, mic = data_getter.get_data()
        for i in range(0, sma_window):
            current_sum += isens
        current = current_sum/sma_window
        current /= 10000
        force = 30.5 * current - 39.9
        
        text = f"Force: {force} N"
        OLED.print_on_OLED(text)
        
        
        

except KeyboardInterrupt:
    exit()
