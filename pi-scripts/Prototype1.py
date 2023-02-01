
import logging
import sys
import time
from Adafruit_BNO055 import BNO055

# import board
# import busio
# i2c = busio.I2C(board.SCL, board.SDA)
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
# ads = ADS.ADS1115(i2c)
# chan = AnalogIn(ads, ADS.P0)

# import pandas as pd

# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
print('Reading BNO055 data, press Ctrl-C to quit...')

# accX_dict = {}
buf_time = time.perf_counter() + 5
# accX_dict['accX'] = [None]
# while time.perf_counter() <= buf_time:
while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Magnetometer data (in micro-Teslas):
    bx,by,bz = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    wx,wy,wz = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    Accx,Accy,Accz = bno.read_accelerometer()
#     accX_dict['accX'] += [Accx]
    # Other values you can optionally read:
    
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    #sys, gyro, accel, mag = bno.get_calibration_status()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    #x,y,z = bno.read_gravity()
    
    #Print everything out.
    print(f'AccX={Accx:.2F} AccY={Accy:.2F} AccZ={Accz:.2F} wx={wx:.2F} wy={wy:.2F} wz={wz:.2F} bx={bx:.2F} by={by:.2F} bz={bz:.2F} heading = {heading:.2F} Roll = {roll:.2F} Pitch = {pitch:.2F}' )
    #print(f'Isens={chan.value:.2F}')
 

    # Sleep for a second until the next reading.
    #time.sleep(12)

# df = pd.DataFrame.from_dict(accX_dict)
# df.dropna()
# df = df.agg(['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', 'mad', 'sum'])
# df.transpose()
# print(df)