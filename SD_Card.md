# ecen4013_proj2
import machine
import sdcard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(8))

# Initialize SD card
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")


# Create a file and write something to it
with open("/sd/Data01.txt", "w") as file:
    file.write("Hello, SD World!\r\n")
    file.write("This is a test\r\n")
    file.write("Angular Velocity: " sck)
    file.write("Linear Acceleration: " mosi)
    file.write("Magnetic Field: " miso )
    file.write("Latitude ")
    file.write("Longitude ")
    file.write("Number of Satellites: ")
    file.write("Elevation: ")
    
    
    
#-----------WE CHANGE THE NAME OF THE FILE TO WHATEVER--------------

# Open the file we just created and read from it
with open("/sd/Data01.txt", "r") as file:
    data = file.read()
    print(data)
