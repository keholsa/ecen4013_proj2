#Bluetooth module test
#connects and allows input/output
#TODO: use uart.write to output input values from parameters

from machine import Pin,UART

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

            
while True:
    # print('checking BT')
    if uart.any():
        command = uart.readline()
        print(command)
    
    # write command
    # uart.write("Entered value")