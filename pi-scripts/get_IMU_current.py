import logging
import sys
import time
from Adafruit_BNO055 import BNO055
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class Current_IMU:
    def __init__(self):
        self.bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.current = AnalogIn(self.ads, ADS.P0)
        self.mic = AnalogIn(self.ads, ADS.P2)
        
        if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
            logging.basicConfig(level=logging.DEBUG)

        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

        status, self_test, error = self.bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        # sw, bl, accel, mag, gyro = self.bno.get_revision()
    
    # print('Software version:   {0}'.format(sw))
    # print('Bootloader version: {0}'.format(bl))
    # print('Accelerometer ID:   0x{0:02X}'.format(accel))
    # print('Magnetometer ID:    0x{0:02X}'.format(mag))
    # print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
    # print('Reading BNO055 data, press Ctrl-C to quit...')
    
    def get_data(self):
#         heading, roll, pitch = self.bno.read_euler()
        bx,by,bz = self.bno.read_magnetometer()
        wx,wy,wz = self.bno.read_gyroscope()
        Accx,Accy,Accz = self.bno.read_accelerometer()

        
        return Accx, Accy, Accz, wx, wy, wz, bx, by, bz, self.current.value, self.mic.value
        # print(f'AccX={Accx:.2F} AccY={Accy:.2F} AccZ={Accz:.2F} wx={wx:.2F} wy={wy:.2F} wz={wz:.2F} bx={bx:.2F} by={by:.2F} bz={bz:.2F} heading = {heading:.2F} Roll = {roll:.2F} Pitch = {pitch:.2F}' )
        # print(f'Isens={chan.value:.2F}')