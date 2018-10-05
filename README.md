# Rasberry Pi Face Recognition via OpenCV and Dlib

Using OpenCV and Dlib to detect and recognize faces from raspberry pi camera

通过树莓派摄像头进行人脸识别

中文请参考https://zhuanlan.zhihu.com/p/45979175

Flow chart：
  - step 0: get faces——>tuen to 128d vectors——>save to csv
  - program start: get data from csv and turn to numpy array，motion detecting...

  - someone showup——>PIR sensor——>openCV videocapture——>openCV dealt image——>face recognition via Dlib  
&nbsp; &nbsp; &nbsp; &nbsp; |——>success——>servo motor control——>open door——>back to motion detecting  
——|  
&nbsp; &nbsp; &nbsp; &nbsp; |——>fail——>wait 50s——>close openCV window——>back to motion detecting  

PIR sensor
'''
#!/usr/bin/python

import time
import RPi.GPIO as GPIO

GPIO_PIR = 18


def detectedAndPrint():
    GPIO.setup(GPIO_PIR, GPIO.IN)
    print("nothing")
    while isDetected():
        time.sleep(0.1)
        print("PIR sensor detected some stuff")


def isDetected():
    while GPIO.input(GPIO_PIR) == GPIO.LOW:
        return False

    while GPIO.input(GPIO_PIR) == GPIO.HIGH:
        return True


if __name__ == '__main__':
    # rpi board gpio or bcm gpio
    GPIO.setmode(GPIO.BCM)

    # loop method
    detectedAndPrint()

'''

Credit: the face recognition libs is from [coneypo](https://github.com/coneypo/Dlib_face_recognition_from_camera)

below is the face recognition steps

<br>
	
	Face register >> Generate datebase >> Face recognition

  	人脸录入 >> 建立人脸数据库 >> 利用摄像头进行人脸识别

<br>

>**get\_face\_fro\_camera.py** : 
	
	Face register / 人脸录入
<br>

>**get\_features\_into\_CSV.py**: 
	
	 Generate the features from the photos you captured and write the datas into CSV / 将图像文件中人脸数据提取出来存入CSV
 	 Will generate a "features_all.csv" ( size: n*128 , n means n people you registered and 128 means 128D features of the face)
<br>

>**face\_reco\_from\_camera.py**: 
	
	 Face recognition from camera (support multi-faces) / 实时进行人脸识别
  	 Compare the faces captured from camera with the faces you have registered which are saved in "features_all.csv"
  	 将捕获到的人脸数据和之前存的人脸数据进行对比计算欧式距离


