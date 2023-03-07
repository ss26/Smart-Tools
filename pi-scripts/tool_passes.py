import OLED
import os
import warnings
import get_data
import time

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

warnings.filterwarnings('ignore')

data_getter = get_data.DataCollector()

sma_window = 30

buffer_time = int(input("Enter time of activity: "))

act_start_time = time.time()

num_passes = 0 
start_times = []
stop_times = []
forces = []
angles = []

try:
    while time.time() <= act_start_time + buffer_time:
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

        if current > 1.9:
            start_times += [time.perf_counter()]
        if current < 1.9:
            stop_times += [time.perf_counter()]

        forces += [force]
        angles += [roll]
    
    while True:
        if stop_times[0] < start_times[0]:
            stop_times = stop_times[1:]
        else:
            break
    assert len(stop_times) == len(start_times)
    total_times = [x - y for x,y in zip(stop_times, start_times)]
    text = f"Num Passes = {num_passes}\nAvg. Time/Pass = {sum(total_times)/len(total_times)} s\nAvg. Force = {sum(forces)/len(forces)} lbf\nAvg. Roll Angle = {sum(angles)/len(angles)} deg."
    OLED.print_on_OLED(text)
        
        
except KeyboardInterrupt:
    exit()
