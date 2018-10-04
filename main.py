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

