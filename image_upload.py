import requests as re
import os
# import time

# used in the rpi side
url = "http://127.0.0.1:5000"

def upload_img(file_name):
    with open(file_name,"rb") as img:
        files = {"file":img}
        r = re.post(f"{url}/traffic/",files=files)
        print(r.text)

def save_img_camera():
    file_name = "./images/camera_feed.jpg"
    os.system(f"libcamera-jpeg -o {file_name} -t 100 --width 640 --height 480")
    return file_name

if __name__ == "__main__":
    # file_n = save_img_camera()
    upload_img(r"C:\Users\Dell\OneDrive\Pictures\tesla_plaid.png")