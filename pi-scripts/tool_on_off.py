from process_data import Preprocess
import OLED
import os
import warnings

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

warnings.filterwarnings('ignore')

preprocess = Preprocess()




try:
    while True:
        raw_df = preprocess.get_raw_df(make=True, timestamp=True, labels=True, raw_buf_time=5)
        current = raw_df['Isens'].mean()
        
        OLED.clear_display()
        
        if current > 10000 and current < 17000:
            text = "Tool is on"
            OLED.print_on_OLED(text)
        elif current > 18000:
            text = "Tool is working"
            OLED.print_on_OLED(text)
        else:
            text = "Tool is off"
            OLED.print_on_OLED(text)
        

except KeyboardInterrupt:
    exit()
