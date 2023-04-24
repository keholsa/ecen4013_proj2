from machine import Pin, I2C
import time

# Power-on-reset time for the BNO055 is 650 ms. Give it time to start.
time.sleep(1)

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
i = 0
while True:
    i += 1
    bytes = i2c.readfrom_mem(0x28, 0x00, 1)
    if i % 1136 == 0:
        print(i, hex(bytes[0]))