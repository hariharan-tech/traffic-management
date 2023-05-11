import read_data
import image_upload
import schedule
import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(0)
gpio.setmode(gpio.BCM)


sens = [read_data.Piezo_Sens(20, "N"), read_data.Piezo_Sens(
    26, "E"), read_data.Piezo_Sens(16, "W"), read_data.Piezo_Sens(19, "S")]


def reset_traffic():
    for sensor in sens:
        sensor.car_pass = 0

def read_traffic():
	for sensor in sens:
		print(f"{sensor.dir} - {sensor.car_pass}")

def send_img():
	print("hi")
	fil_n = image_upload.save_img_camera()
	image_upload.upload_img(fil_n)

schedule.every().hour.do(reset_traffic)
schedule.every(5).seconds.do(send_img)  # send image every n seconds

standard_green_time = 60
dir_ref = {"N": [1, "Northern", 60], "E": [1, "Eastern", 60],
           "W": [1, "Western", 60], "S": [1, "Southern", 60]}

l1_r,l1_g = 2, 3
l2_r, l2_g = 14,15
l3_r,l3_g = 17, 27
l4_r, l4_g = 23,24

temp = [2,3,14,15,17,27,23,24]

for i in range(len(temp)):
	gpio.setup(temp[i],gpio.OUT,initial=0)

try:
	while True:
		schedule.run_pending()
		# Traffic light time changing algorithm
		norm_val = [1,1,1,1]
		for i in range(len(sens)):
			#print("chumma")
			if sens[i].car_pass == 0:
				continue
			dir_ref[sens[i].dir][0] = sens[i].car_pass
			norm_val[i] = dir_ref[sens[i].dir][0]
		print(norm_val)
		# Normalize the car_pass value => 0 to 1 (greater value indicates more traffic in that direction)
		for i in range(len(norm_val)):
			norm_val[i] /= sum(norm_val)
		# norm_val contains the normalized values of traffic count
		green_time1 = norm_val[0]*5
		green_time2 = norm_val[1]*5
		green_time3 = norm_val[2]*5
		green_time4 = norm_val[3]*5
		
		gpio.output(l4_g,0)
		gpio.output(l1_r,0)
		
		gpio.output(l1_g,1)
		gpio.output(l2_r,1)
		gpio.output(l3_r,1)
		gpio.output(l4_r,1)
		sleep(green_time1)
				
		gpio.output(l1_g,0)
		gpio.output(l1_r,1)
		gpio.output(l2_r,0)
		gpio.output(l2_g,1)
		sleep(green_time2)
		
		gpio.output(l2_r,1)
		gpio.output(l2_g,0)
		gpio.output(l3_r,0)
		gpio.output(l3_g,1)
		sleep(green_time3)
		
		gpio.output(l3_r,1)
		gpio.output(l3_g,0)
		gpio.output(l4_r,0)
		gpio.output(l4_g,1)
		sleep(green_time4)
		continue

except KeyboardInterrupt:
	read_data.__close_session()
