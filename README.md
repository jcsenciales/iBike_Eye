# iBike_Eye

Intelligent Automatic Photo shooter for my Mountain Bike

## Motivation

How many times you are riding at your favorite route, and you see a horse or a cow or a great boat and you want to take
it a photo.Then you need to stop, grab your mobile phone and take your photo to share with strava, twitter or using
other social net with your followers. When I ride with my daughters this situation could repeat several times, really I
hate to stop every 10 minutes to take photos, so I think could be useful to have an intelligent camera in my bike to
automatically take photos only if the camera automatically see a set of animals or objects I define. For this I use in
this project deep learning models.

## Description

iBike_Eye is a project to automatically take photos or make videos while you are riding. For this purpose I used an
OAK-1 embedded 4k camera and neural compute edge compute [Intel Movidius™ Myriad™ X](https://www.intel.com/content/www/us/en/products/details/processors/movidius-vpu/movidius-myriad-x.html) that enables CNN-based deep learning inference on the edge. I upload deep learning models into OAK-1 camera, and the intel unit run the deep-learning models and return detections using USB-3 interface. So I need some mini computer to
save photos and videos, here can to play my Raspberry. The main characteristics are:

1. Take automatically photos using deep learning models.
2. It can be used several models with different precisions (mobilenet, yolo,...) or train your own amazing model.
3. I have several parameters to configure frequency between photos, fps, score confidence.
4. Is needed to configure a list of classes I am interested to take it photos. ('aeroplane', 'bicycle', 'bird', 'boat', 'car', 'cat', 'cow', 'dog', 'horse', ...)
5. I have used Raspberry-Pi GPIO to implement a physical button to save videos. These videos also have all boxes detections. 

<img src="https://user-images.githubusercontent.com/4199937/112661508-e2e62f80-8e56-11eb-88e8-9f6338f819eb.png" width="30%" height="30%" alt="OAK-1 Camera" title="OAK-1 Camera">


## Hardware used

1. Raspberry pi 4 Model B with case and fan for ventilation
2. Camera OAK-1 with edge compute intel Myriad X visual processor inside
3. 32GB MicroSD Class I
4. Mini switch and two wires for GPIO Button_video
5. Battery Power Bank 5v USB 10400 mAh
6. Two USB wires to connect with the camera and supply power to Raspberry-pi

<img src="https://user-images.githubusercontent.com/4199937/112680418-a3770d80-8e6d-11eb-9669-4fe94257d099.jpg" width="40%" height="40%" alt="RaspBerry Pi y OAK-1 Camera" title="RaspBerry Pi, Battery and OAK-1 Camera">

## Deep Learning Models used

it´s used mainly two models in all the test done. MobileNetSSD and Yolo_v3. These are open free models for object
detections from [OpenVINO](https://docs.openvinotoolkit.org/latest/index.html). Only we need to compile these models to
get model files compatible with the edge 
compute [Intel Movidius™ Myriad™ X](https://www.intel.com/content/www/us/en/products/details/processors/movidius-vpu/movidius-myriad-x.html).

1. [MobileNetSSD](https://docs.openvinotoolkit.org/2021.2/omz_models_public_mobilenet_ssd_mobilenet_ssd.html), trained
   on a dataset with 20 classes.
2. [Yolo-v3](https://docs.openvinotoolkit.org/latest/omz_models_model_yolo_v3_tf.html), trained on COCO dataset with 80
   classes.


## Raspberry Configuration

1. Install [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) into 32GB MicroSD.
2. Create a python3 virtualenv to install libs.
3. Install [DepthAI Library gen1](https://docs.luxonis.com/en/gen1_master/pages/api/#supported-platforms), (in a future
   I need to update to gen2 API)
4. Install my Bike_eye_pi.py script and its configuration script
5. Install GPIO Library to control video button

With all the above steps we have the Raspberry ready to use OAK-1 and go out to take automatic photos. it´s needed to
ensure when we connect power to Raspberry all software it´s started without keyboard and without a screen because on a
bike I will use the minimal devices possible.

## Raspberry Automatic script run

When I connect power to Raspberry-pi in my Bike, I need to start all the process automatically without any intervention.
This is solved using crontab.
```
@reboot  /home/pi/depthai/run_bike_eye.sh
```
It is used a bash script ('run_bike_eye.sh') that activate the python3 virtualenv and run the Bike_eye_pi.py python script. After that I can
begin my bike route taken automatically photos using the Deep Learning Models deployed into OAK-1.
```
#!/bin/bash

source /home/pi/depthai/venv/bin/activate
cd /home/pi/depthai
python3 Bike_eye_pi.py
```

## iBike Eye Configuration

The script configuration can be changed in the file "bike_eye_config.py"

The main parameters are:

image parameters:
```
img_path = './outimg/' #path to save images 
frecuency_img = 2 # n seconds for waiting between write every image to disk 
score_confidence = 80 # score to be save image or not
```
video parameters:
```
video_duration = 20 #durations of videos 
video_fps = 15.0 #video frame per second 
video_path = './outvideo/' #path to save videos
```
Also, in this config file we can select between use MobileNetSSD or Yolo-v3 models and configure our object classes.
```
my_wanted_objects = ['bicycle', 'motorbike', 'aeroplane', 'bus', 'train', 'boat', 'horse', 'dog', 'cat', 'bird',
                      'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'frisbee', 'skis', 'snowboard',
                      'sports_ball', 'kite', 'skateboard', 'surfboard', 'tennis_racket']
```

## Video recording Feature

The software allow save short videos when is pressed the mini button connected to Raspberry GPIO. These videos have a
fixed duration you can configure in the config file. The video feature saves frames, and the objects detected by the
model in real time, so if you want save something interesting while riding you only need to press this button.

While a video is been recording the video button is disabled and if you press it has any effect.

## Bike Installation

I use a camera clamp on the bike handlebar as you can see on the photos.

<img src="https://user-images.githubusercontent.com/4199937/112726347-358a1f00-8f1d-11eb-84e4-be4c2b51a9ee.jpg" width="30%" height="30%" alt="OAK-1 Camera on Bike" title="OAK-1 Camera on Bike">

I carry the battery and Raspberry-pi in a little waist bag with care about ventilation.

<img src="https://user-images.githubusercontent.com/4199937/112726353-3cb12d00-8f1d-11eb-87a6-9d234ef2394f.jpg" width="30%" height="30%" alt="Battery and Raspberry in a bag" title="Battery and Raspberry in a bag">

## Battery duration and temperature

I always begin my route with the battery 100% charged, my routes has a maximun duration 1,5 hours and the battery arrive with 50% charge left.

The temperature is moving between 57 and 64 degrees celsius. The fan is configurated to operate at 60 degrees celsius.

![Raspberry_temperature](https://user-images.githubusercontent.com/4199937/112727827-8f421780-8f24-11eb-9197-0eda6dcb357a.png)

The memory comsuptions is minimal, remember all the deep_learning model process is done on the intel edge processor.

![Raspberry_htop](https://user-images.githubusercontent.com/4199937/112727816-87827300-8f24-11eb-96b5-b5f56f5065cd.png)


## Costs

1. [OAK-1](https://store.opencv.ai/products/oak-1): 149$
2. [RaspBerry pi 4 MODEL B 4GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/): 49€
3. Raspberry case: 7.20€
4. Raspberry Fan: 5€
5. 32GB Microsd class I: 7 €
6. mino switch: 0 €, it is from an old car cd player.


## TO-DO, TO-TEST, More Ideas

1. Change the code to DepthAI API gen2.
2. Test for detecting object with custom models.
3. Make a car plates detector using a two stage pipeline and save all number plates in a log file. In that way I have
   saved all the cars plates seen in my bike route.
4. Count people with and without COVID-19 mask while I ride to get a mask use percent.
5. Connect some detections with social networks as Twitter, Strava to upload photos while I am riding with the Raspberry
   connected to Wifi mobile.
6. Detect holes on the road, fallen tree branches... take photos and notify the city council repair services to fix it.
7. 



## Results
1. I have saved some tests routes with Strava (The Strava API not allow me upload image for free on air, so I´ve uploaded manually), <a href="https://www.strava.com/athletes/79682242">You can see my tests on this strava! profile.</a>


<img src="https://user-images.githubusercontent.com/4199937/112039057-e2425600-8b43-11eb-88a6-3969b59ddf99.jpg" width="60%" height="60%" alt="Example_1">

<img src="https://user-images.githubusercontent.com/4199937/112760109-26c36b00-8ff6-11eb-9aa3-59a87a623a1c.jpg" width="60%" height="60%" alt="Example_2">

<img src="https://user-images.githubusercontent.com/4199937/113266947-17823d00-92d6-11eb-88d6-223661d778aa.jpg" alt="Example_3">

<img src="https://user-images.githubusercontent.com/4199937/113267239-65974080-92d6-11eb-85ee-5a48e03445a6.jpg" width="60%" height="60%" alt="Example_4">

<img src="https://user-images.githubusercontent.com/4199937/113267462-aabb7280-92d6-11eb-8b3f-fbdd02477d9b.jpg" width="60%" height="60%" alt="Example_5">



