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

>PIR sensor

```
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

```

>Servo motor

```
import RPi.GPIO as GPIO  
import time  
import signal  
import atexit  

atexit.register(GPIO.cleanup)    

servopin = 21  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(servopin, GPIO.OUT, initial=False)  
p = GPIO.PWM(servopin,50) #50HZ  
p.start(0)  
time.sleep(2)  

def open_door():
    for i in range(0,181,10):  
        p.ChangeDutyCycle(2.5 + 10 * i / 180) 
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.2)  

    for i in range(181,0,-10):  
        p.ChangeDutyCycle(2.5 + 10 * i / 180)  
        time.sleep(0.02)  
        p.ChangeDutyCycle(0)  
        time.sleep(0.2)
```


>main.py

```

#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import signal  
import atexit
from sensor import isDetected
import dlib         # 人脸识别的库dlib
import pandas as pd # 数据处理的库Pandas


from face_reco_from_camera import reco_face

GPIO_PIR = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR, GPIO.IN)

# face recognition model, the object maps human faces into 128D vectors
facerec = dlib.face_recognition_model_v1("data/dlib_dat/dlib_face_recognition_resnet_model_v1.dat")

# 处理存放所有人脸特征的 CSV
path_features_known_csv = "data/features_all.csv"
csv_rd = pd.read_csv(path_features_known_csv, header=None)

# 用来存放所有录入人脸特征的数组
features_known_arr = []

# Dlib 预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib_dat/shape_predictor_68_face_landmarks.dat')

# known faces
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    for j in range(0, len(csv_rd.ix[i, :])):
        features_someone_arr.append(csv_rd.ix[i, :][j])
    #    print(features_someone_arr)
    features_known_arr.append(features_someone_arr)
print("Faces in Database：", len(features_known_arr))

while 1:
    if isDetected():
        start_time=time.time()
        reco_face(facerec, features_known_arr, detector, predictor,start_time)
```

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


