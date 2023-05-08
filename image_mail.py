import smtplib
# import imghdr
# from email.message import EmailMessage

# Sender_Email = ""
# Reciever_Email = ""
# # Password = input('Enter your email account password: ')

# newMessage = EmailMessage()    #creating an object of EmailMessage class
# newMessage['Subject'] = "Alert Email" #Defining email subject
# newMessage['From'] = Sender_Email  #Defining sender email
# newMessage['To'] = Reciever_Email  #Defining reciever email
# newMessage.set_content('Hello, Please check!') #Defining email body

# with open('img.jpeg', 'rb') as f:
#     image_data = f.read()
#     image_type = imghdr.what(f.name)
#     image_name = f.name

# newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#     smtp.login(Sender_Email,'app_pwd') #Login to SMTP server
#     smtp.send_message(newMessage)      #Sending email using send_message method by passing EmailMessage object

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

msg = MIMEMultipart('alternative')
msg['Subject'] = "SEND YES IF THIS IS WORKING FINE"
msg['From'] = ''
msg['To'] = ''

text = MIMEText('<img src="cid:image1"> <br/> <img src="cid:image2">', 'html')
msg.attach(text)

image = MIMEImage(open('img.jpg', 'rb').read())
image_2 = MIMEImage(open('imag.jpg', 'rb').read())

# Define the image's ID as referenced in the HTML body above
image.add_header('Content-ID', '<image1>')
msg.attach(image)
image_2.add_header('Content-ID', '<image2>')
msg.attach(image_2)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('','app_pwd') #Login to SMTP server
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())

# s = smtplib.SMTP('localhost')
# s.sendmail('', '', msg.as_string())
# s.quit()

