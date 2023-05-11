import requests as re
import os

# used in the rpi side
url = "http://127.0.0.1:5000"

def upload_img(file_name):
    try:
        with open(file_name,"rb") as img:
            files = {"file":img}
            r = re.post(f"{url}/traffic/",files=files)
            print(r.text)
    except:
        print("error")

def save_img_camera():
    file_name = "./images/camera_feed.jpg"
    try:
        os.system(f"libcamera-jpeg -o {file_name} -t 100 --width 640 --height 480")
    except KeyboardInterrupt:
        exit()
    except:
        print("can't take image")
    return file_name

if __name__ == "__main__":
    file_n = save_img_camera()
    print(file_n)
    upload_img(r"./images/camera_feed.jpg")
