# IMU individual return funciton
# initializes i2c pins for device before function call to increase speed
# returns array for magnetic field, angular acceleration, linear acceleration

#REQUIRES bno055.py, bno055_base.py

# importing libraries
from machine import Pin, I2C
import time
from bno055 import *

# initialize pins on board
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000) 

# function definition
def imu_func():

    # initializing arrays for storage to later be called in return
    mag_data = []
    gyro_data = []
    lin_acc_data = []

    # utilizing header module for bno055 chip
    imu = BNO055(i2c)
    
    # calibrating chip on call
    calibrated = False
    
    # giving chip time to read surrounding data
    time.sleep(.1)
    
    # executing calibration
    if not calibrated:
        calibrated = imu.calibrated()
        
    # reading x,y,z values into individual variables
    mag_x, mag_y, mag_z = imu.mag()
    gyro_x, gyro_y, gyro_z = imu.gyro()
    lin_acc_x, lin_acc_y, lin_acc_z = imu.lin_acc()

    # appending array with new values (could only get as a tuple for some reason)
    mag_data.append([mag_x, mag_y, mag_z])
    gyro_data.append([gyro_x, gyro_y, gyro_z])
    lin_acc_data.append([lin_acc_x, lin_acc_y, lin_acc_z])

    # return first index of array tuple for each element
    return mag_data[0], gyro_data[0], lin_acc_data[0]

# testing code and execution
magnetic_field_data, gyroscope_data, accelerometer_data = imu_func()

print(magnetic_field_data)
print(gyroscope_data)
print(accelerometer_data)
