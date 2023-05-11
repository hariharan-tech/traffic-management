import RPi.GPIO as gpio
gpio.setwarnings(0)
gpio.setmode(gpio.BCM)

class Piezo_Sens:
    sensor_ID = 0 # sensor ID
    car_pass = 0 # number of cars that has been detected
    
    def __init__(self,pin_no,dir):
        self.pin_no = pin_no
        self.dir = dir
        self.sensor_ID+=1
        gpio.setup(self.pin_no,gpio.IN)
        gpio.add_event_detect(self.pin_no,gpio.FALLING,callback=self.car_pass_callback,bouncetime=50)

    def car_pass_callback(self,channel):
        self.car_pass+=1
        print(f"car passed {self.car_pass} - in direction {self.dir}")

    # def get_curr_state(self):
        #return gpio.input(self.pin_no)

def __close_session():
    gpio.cleanup()

# Testing code
if __name__=="__main__":
    sensor1 = Piezo_Sens(40)
    print(sensor1.pin_no)
    try:
        while True:
            continue
    except:
        __close_session()
