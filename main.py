# importing libraries
from machine import Pin, I2C, UART
import time
from bno055 import *
import sdcard
import os


# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(14),
                  mosi=machine.Pin(15),
                  miso=machine.Pin(12))

# Initialize SD card
sd = sdcard.SDCard(spi, cs)


# initialize pins on board
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

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

def gps_func():
    
    uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

    # initializing variables
    flag = 0
    rawDataArr = []
    

    # while loop that gets first line of data
    while flag <= 4:
        
        # checking if any uart comm on device
        if uart.any():
            
            # try and catch due to unicode error
            try:
                
                # reading in values and converting from utf-8 characters
                command = uart.readline().decode('utf-8')
                
                # adding each character into an array
                rawDataArr.append(command)
            
                
                
                # stopping data read at end of line
                if(command.startswith('$')):
                    flag += 1
                
                
            # exception case for UnicodeError
            except UnicodeError as e:
                
                # ignores exception, continues loop
                pass

    dataString = ''.join(rawDataArr)

    # removes last character
    dataString = dataString[:-1]


    dataArr = dataString.split(',')
    

    outputArr = [dataArr[3] + dataArr[4], dataArr[5] + dataArr[6], dataArr[30], dataArr[28]]

    return outputArr

def bluetooth_func(gps_data, magnetic_field_data, gyroscope_data, accelerometer_data):
        
    # defining elements of array for concatenate sequence
    # GPS data
    latitude = str(gps_data[0])
    longitude = str(gps_data[1])
    elevation = str(gps_data[2])
    numSatellites = str(gps_data[3])
    
    # IMU data
    mag_x = str(magnetic_field_data[0])
    mag_y = str(magnetic_field_data[1])
    mag_z = str(magnetic_field_data[2])
    
    gyro_x = str(gyroscope_data[0])
    gyro_y = str(gyroscope_data[1])
    gyro_z = str(gyroscope_data[2])
    
    accel_x = str(accelerometer_data[0])
    accel_y = str(accelerometer_data[1])
    accel_z = str(accelerometer_data[2])
    
    # write command
    uart.write("\n-------GPS--------\n")
    uart.write("Latitude and Longitude: " + latitude + ", " + longitude + "\n")
    uart.write("Elevation: " + elevation + "ft\n")
    uart.write("Satellite count: " + numSatellites + "\n")
    uart.write("\n-------IMU--------\n")
    uart.write("Linear Acceleration Vector: " + accel_x + ", " + accel_y + ", " + accel_z + "\n")
    uart.write("Gyroscope Vector: " + gyro_x + ", " + gyro_y + ", " + gyro_z + "\n")
    uart.write("Magnetic Field Vector: " + mag_x + ", " + mag_y + ", " + mag_z + "\n")
    print("Bluetooth has been updated...")
    

def sd_func_initialize(gps_data, magnetic_field_data, gyroscope_data, linear_acceleration_data):
    
    # Define the filename
    filename = "/sd/GPS.csv"
    with open(filename, "w") as file:
        # Write the data rows

        # GPS data
        latitude = str(gps_data[0])
        longitude = str(gps_data[1])
        elevation = str(gps_data[2])
        numSatellites = str(gps_data[3])

        # IMU data
        mag_x = str(magnetic_field_data[0])
        mag_y = str(magnetic_field_data[1])
        mag_z = str(magnetic_field_data[2])

        gyro_x = str(gyroscope_data[0])
        gyro_y = str(gyroscope_data[1])
        gyro_z = str(gyroscope_data[2])

        accel_x = str(linear_acceleration_data[0])
        accel_y = str(linear_acceleration_data[1])
        accel_z = str(linear_acceleration_data[2])

        # Write the row to the file
        file.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(latitude, longitude, elevation, numSatellites, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z))

def sd_func(gps_data, magnetic_field_data, gyroscope_data, linear_acceleration_data):
    
    # Define the filename
    filename = "/sd/GPS.csv"

    with open(filename, "a") as file:

        # GPS data
        latitude = str(gps_data[0])
        longitude = str(gps_data[1])
        elevation = str(gps_data[2])
        numSatellites = str(gps_data[3])

        # IMU data
        mag_x = str(magnetic_field_data[0])
        mag_y = str(magnetic_field_data[1])
        mag_z = str(magnetic_field_data[2])

        gyro_x = str(gyroscope_data[0])
        gyro_y = str(gyroscope_data[1])
        gyro_z = str(gyroscope_data[2])

        accel_x = str(linear_acceleration_data[0])
        accel_y = str(linear_acceleration_data[1])
        accel_z = str(linear_acceleration_data[2])

        # Write the row to the file
        file.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(latitude, longitude, elevation, numSatellites, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z))

        print("SD card updated...")
# Mount filesystem
os.mount(sd, "/sd")
sd_func_initialize(["Latitude","Longitude", "Elevation", "Satellites"],
                   ["Magnetism X","Magnetism Y", "Magnetism Z"],
                   ["Gyroscope X","Gyroscope Y", "Gyroscope Z"],
                   ["Accelerometer X","Accelerometer Y", "Accelerometer Z"])
if "/sd" in os.listdir():
    os.umount("/sd")
while True:
    magnetic_field_data, gyroscope_data, accelerometer_data = imu_func()

    gpsArr = gps_func()

    print(gpsArr)
    print(accelerometer_data)
    print(magnetic_field_data)
    print(gyroscope_data)
    
    bluetooth_func(gpsArr, magnetic_field_data, gyroscope_data, accelerometer_data)

    sd_func(gpsArr, magnetic_field_data, gyroscope_data, accelerometer_data)


