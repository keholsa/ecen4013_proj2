# ecen4013_proj2
import board
import busio
import adafruit_sdcard
import adafruit_gps
import csv
import time

# Initialize SD card
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sdcard)
os.mount(vfs, "/sd")

# Initialize GPS
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)
gps.send_command(b'PMTK314,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

# Create a CSV file on the SD card to store the GPS data
filename = "/sd/gps_data.csv"
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Longitude", "Latitude", "Magnetic Field", "Elevation", "Number of Satellites", "Angular Velocity", "Linear Accleration"])

    # Continuously read GPS data and write it to the CSV file
    while True:
        gps.update()
        if gps.has_fix:
            csvwriter.writerow([gps.longitude, gps.latitude, gps.magnetic_variation, gps.altitude_m, gps.satellites, gps.speed_knots, gps.speed_kmph])
            print("Latitude:", gps.latitude)
            print("Longitude:", gps.longitude)
            print("Magnetic Field:", gps.magnetic_variation)
            print("Elevation:", gps.altitude_m)
            print("Number of Satellites:", gps.satellites)
            print("Angular Velocity:", gps.speed_knots)
            print("Linear Accleration:", gps.speed_kmph)
        time.sleep(1)
