import board
import busio
import adafruit_bno055
import serial
import time
uart = serial.Serial('/dev/serial0')
sensor = adafruit_bno055.BNO055_UART(uart)



while True:

    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
#     print("Magnetometer (microteslas): {}".format(sensor.magnetic))
#     print("Gyroscope (rad/sec): {}".format(sensor.gyro))
#     print("Euler angle: {}".format(sensor.euler))
  


