from machine import Pin,UART
import time

#TODO: wait until GPS chip is initialized
def gps_func():
    # initializing uart communication on pins 16/17
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

while True:
    gpsArr = gps_func()
    print(gpsArr)






