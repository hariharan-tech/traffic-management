import read_data
import image_upload
import schedule
from gpiozero import TrafficLights
from time import sleep

sens = [read_data.Piezo_Sens(40, "N"), read_data.Piezo_Sens(
    38, "E"), read_data.Piezo_Sens(38, "W"), read_data.Piezo_Sens(38, "S")]


def reset_traffic():
    for sensor in sens:
        sensor.car_pass = 0


def read_traffic():
    for sensor in sens:
        print(f"{sensor.dir} - {sensor.car_pass}")


def send_img():
    fil_n = image_upload.save_img_camera()
    image_upload.upload_img(fil_n)


# schedule.every().seconds.do(read_traffic)
schedule.every().hour.do(reset_traffic)
schedule.every(5).seconds.do(send_img)  # send image every n seconds

standard_green_time = 60
dir_ref = {"N": [1, "Northern", 60], "E": [1, "Eastern", 60],
           "W": [1, "Western", 60], "S": [1, "Southern", 60]}

lights_lane1 = TrafficLights(2, 4, 3)
lights_lane2 = Trafficlights(14, 18, 15)
lights_lane3 = Trafficlights(17, 22, 27)
lights_lane4 = Trafficlights(23, 25, 24)

try:
    while True:
        schedule.run_pending()
        # Traffic light time changing algorithm
        norm_val = [1, 2, 3]
        for sensor in sens:
            if sensor.car_pass == 0:
                continue
            dir_ref[sensor.dir][0] = sensor.car_pass
            norm_val.append(dir_ref[sensor.dir][0])
        # Normalize the car_pass value => 0 to 1 (greater value indicates more traffic in that direction)
        for i in range(len(norm_val)):
            norm_val[i] /= sum(norm_val)
        # norm_val contains the normalized values of traffic count
        # norm_val.sort()
        green_time1 = norm_val[0]*60
        green_time2 = norm_val[1]*60
        green_time3 = norm_val[2]*60
        green_time4 = norm_val[3]*60
        # red_time1=(1-norm_val[4])*60
        # red_time2=(1-norm_val[3])*60
        # red_time3=(1-norm_val[2])*60
        # red_time4=(1-norm_val[4])*60
        # from gpiozero import LED
        # led = LED(17)
        # led.on()
        # led.off()
        lights_lane1.green.on()
        lights_lane2.red.on()
        lights_lane3.red.on()
        lights_lane4.red.on()
        sleep(green_time1)

        lights_lane1.green.off()
        lights_lane1.red.on()
        lights_lane2.red.off()
        lights_lane2.green.on()
        #  lights_lane3.red.on()
        #  lights_lane4.red.on()
        sleep(green_time2)

        #  lights_lane1.red.on()
        lights_lane2.red.on()
        lights_lane2.green.off()
        lights_lane3.red.off()
        lights_lane3.green.on()
        #  lights_lane4.red.on()
        sleep(green_time3)

        #  lights_lane1.red.on()
        #  lights_lane2.red.on()
        #  lights_lane2.green.off()
        lights_lane3.red.on()
        lights_lane3.green.off()
        lights_lane4.red.off()
        lights_lane4.green.on()
        sleep(green_time4)
        continue
except KeyboardInterrupt:
    read_data.__close_session()

    #  lights_lane1.red.on()
    #  sleep((1-red_time1=norm_val[4])*60)
    #  lights_lane1.off()
    #  lights_lane2.green.on()
    #  sleep(green_time2=norm_val[3]*40)
    #  lights_lane1.red.on()
    #  sleep(red_time2=norm_val[3]*20)
    #  lights_lane2.off()
    #  lights_lane3.green.on()
    #  sleep(green_time3=norm_val[2]*20)
    #  lights_lane3.red.on()
    #  sleep(red_time3=norm_val[2]*40)
    #  lights_lane3.off()
    #  lights_lane4.green.on()
    #  sleep(green_time4=norm_val[1]*10)
    #  lights_lane4.red.on()
    #  sleep(red_time4=norm_val[1]*60)
    #  lights_lane4.off()