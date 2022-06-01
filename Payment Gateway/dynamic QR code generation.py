from crud import manage
from datetime import datetime
import json
import serial
import time
import pyqrcode
import cv2
import png
from PIL import Image

cost = 0
ser = serial.Serial('COM5', 9800, timeout=1)  # defining serial port
time.sleep(2)  # adding delay
data = []
for i in range(500):
    b = ser.readline()  # reading a value through Python from the serial port
    string_n = b.decode()  # convert bytes to a string
    string = string_n.rstrip()
    rfid = string
    if string != '':
        print(string)
        data = manage.start(rfid)
        if data[0] == 'exit':
            cost = data[3]
            print(cost)
            print(data)

            # link UPI accounts for payments
            link = ('upi://pay?ver=01&mode=15&pa=rzr.qrtestcase4983247082@icic&pn=Testcase&tr=RZPIm0LTpEATn1PFlqrv2&tn'
                    '=PaymenttoTestcase&cu=INR&mc=0&qrMedium=04&am=')

            k = str(cost)
            data1 = link + k
            a = str(data1)
            img = pyqrcode.create(a)  # create dynamic QR code
            img.svg("Payment.jpg", scale=8)
            img.png("Payment.jpg", scale=6)
            img = Image.open('Payment.jpg')  # show QR code in a new window
            img.show()
            time.sleep(2)
