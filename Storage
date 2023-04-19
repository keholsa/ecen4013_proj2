import csv 
import os

sd_path = "/mnt/sdcard"

log_file = opencos.path.join(sd_path, "log.csv"),"a")

log_writer = csv.writer(log_file)

if os.stat(log_file.name).st_size == 0:
log_writer.writerow (["Date/Time", "sensor1 Value: , "Sensor 2 Value: " , "Sensor 3 Value: ", "Sensor 4 Value: "])

log_writer.writerow([data_time, sensor1_value, sensor2_value, sensor3_value, sensor4_value])
