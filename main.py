import read_data
import image_upload
import schedule


sens = [read_data.Piezo_Sens(40,"N"),read_data.Piezo_Sens(38,"E"),read_data.Piezo_Sens(38,"W"),read_data.Piezo_Sens(38,"S")]

def reset_traffic():
    for sensor in sens:
        sensor.car_pass = 0

def read_traffic():
    for sensor in sens:
        print(f"{sensor.dir} - {sensor.car_pass}")

def send_img():
    fil_n = image_upload.save_img_camera()
    image_upload.upload_img(fil_n)

#schedule.every().seconds.do(read_traffic)
schedule.every().hour.do(reset_traffic)
schedule.every(2).seconds.do(send_img) #send image every 2 seconds

standard_green_time = 60
dir_ref = {"N":[0,"Northern",60],"E":[0,"Eastern",60],"W":[0,"Western",60],"S":[0,"Southern",60]}

try:
    while True:
        schedule.run_pending()
        # Traffic light time changing algorithm
        norm_val = []
        for sensor in sens:
            dir_ref[sensor.dir][0] = sensor.car_pass
            norm_val.append(dir_ref[sensor.dir][0])
        # Normalize the car_pass value => 0 to 1 (greater value indicates more traffic in that direction)
        for i in range(len(norm_val)):
            norm_val[i] /= sum(norm_val)
        # norm_val contains the normalized values of traffic count
        
        continue
except KeyboardInterrupt:
    read_data.__close_session()