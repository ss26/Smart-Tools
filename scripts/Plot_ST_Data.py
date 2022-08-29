import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')
filename = '/Users/josebendana/Desktop/Smart Tools/Activity Recognition/ST_Data_Collection_V1-main/Raw_Data_2021/Run_1_Samples/Raul /Raul_R1637775000.csv'
data = pd.read_csv(filename)

time = np.array(data.Time)
x = np.array(data.accX) # [counts]
y = np.array(data.accY) # [counts]
z = np.array(data.accZ) # [counts]
wx = np.array(data.wx)  # [counts]
wy = np.array(data.wy)  # [counts]
wz = np.array(data.wz)  # [counts]

bx = np.array(data.bx)  # [counts]
by = np.array(data.by)  # [counts]
bz = np.array(data.bz)  # [counts]

Isens = np.array(data.Isens)  # [counts] - currently reading SLM
Srms = np.array(data.Srms)  # [counts] - microphone

# convert counts to gs
conv_accel = 1  # conversion rate from raw data [counts] to units of [g]
x_g = x*conv_accel   # [g]
y_g = y*conv_accel   # [g] 
z_g = z*conv_accel   # [g]

conv_gyro = 1    # conversion rate from raw data [counts] to [dps]
wx_dps = wx*conv_gyro   # [dps]
wy_dps = wy*conv_gyro   # [dps]
wz_dps = wz*conv_gyro   # [dps]

fig, axs = plt.subplots(3, 2)
axs[0, 0].plot(time, x_g, label='x')
axs[0, 0].plot(time, y_g, label='y')
axs[0, 0].plot(time, z_g, label='z')
axs[0, 0].set_title("Acceleration vs Time")
axs[0, 0].set_ylabel("[g]")
axs[0, 0].set_xlabel("[sec]")

axs[1, 0].plot(time, wx_dps, label='wx')
axs[1, 0].plot(time, wy_dps, label='wy')
axs[1, 0].plot(time, wz_dps, label='wz')
axs[1, 0].set_title("Angular rate vs Time")
axs[1, 0].set_ylabel("[dps]")
axs[1, 0].set_xlabel("[sec]")

axs[2, 0].plot(time, bx, label='bx')
axs[2, 0].plot(time, by, label='by')
axs[2, 0].plot(time, bz, label='bz')
axs[2, 0].set_title("Mag field vs Time")
axs[2, 0].set_ylabel("[T]")
axs[2, 0].set_xlabel("[sec]")

axs[0, 1].plot(time, Isens, label='Isens')
axs[0, 1].set_title("Current sensor voltage")
axs[0, 1].set_ylabel("[V]")
axs[0, 1].set_xlabel("[sec]")

axs[1, 1].plot(time, Srms, label='Srms')
axs[1, 1].set_title("Srms vs Time")
axs[1, 1].set_ylabel("[Srms]")
axs[1, 1].set_xlabel("[sec]")

fig.tight_layout()
plt.show()