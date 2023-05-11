import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

img_file = ".\\images\\new_pic.jpg"

def send_mail_alert():
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Traffic Violation ALERT!"
    msg['From'] = 'sender@sender.com'
    msg['To'] = 'receiver@receiver.com'

    text = MIMEText('<img src="cid:image1"> <br> <img src="cid:image2">', 'html')
    msg.attach(text)

    image = MIMEImage(open(img_file, 'rb').read())
    image_2 = MIMEImage(open('.\images\camera_cv2.jpg', 'rb').read())

    # Define the image's ID as referenced in the HTML body above
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)
    image_2.add_header('Content-ID', '<image2>')
    msg.attach(image_2)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('sender@sender.com','pwd') #Login to SMTP server
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

# s = smtplib.SMTP('localhost')
# s.sendmail('', '', msg.as_string())
# s.quit()
