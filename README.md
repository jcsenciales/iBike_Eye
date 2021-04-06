# iBike_Eye

Intelligent Automatic Photo shooter for my Mountain Bike

[![Watch the video](https://user-images.githubusercontent.com/4199937/113694741-6e21b980-96d0-11eb-8a50-110985f31798.png)](https://user-images.githubusercontent.com/4199937/113674956-175db500-96bb-11eb-9dd5-73f872fc44c0.mp4)


## Motivation

How many times you are riding at your favorite MTB route, and you see a horse or a cow or a great boat and you want to take
it a photo.So you need to stop, grab your mobile phone and take your photo to share with strava, twitter or using
another social net with your followers. When I ride with my daughters this situation could repeat several times, really I
hate to stop every 10 minutes to take photos, so I mean could be useful to have an intelligent camera on my bike to take
automatically photos only if the camera automatically detect a set of animals or objects I have previously defined. For this, in
this project is used object detection deep learning models.

## Description

iBike_Eye is a project to automatically take photos or make videos while you are riding on your bike. For this purpose I used an
OAK-1 embedded 4k camera and a visual edge compute processor [Intel Movidius™ Myriad™ X](https://www.intel.com/content/www/us/en/products/details/processors/movidius-vpu/movidius-myriad-x.html) that enables CNN-based deep learning inference on the edge. I upload deep learning models into OAK-1 camera, and the intel unit run the deep-learning models and return detections using USB-3 interface. So I need a host mini computer to save photos and videos, here is where can to play my Raspberry-Pi. The main characteristics are:

1. Take automatically photos using deep learning models.
2. It can be used several models with different precisions (mobilenet, yolo,...) or train your own amazing deep learning model.
3. I have several parameters to configure frequency between photos, fps, score confidence.
4. Is needed to configure a list of classes I am interested to take it photos. ('aeroplane', 'bicycle', 'bird', 'boat', 'car', 'cat', 'cow', 'dog', 'horse', ...)
5. I have used Raspberry-Pi GPIO to implement a physical button to save videos. These videos also show all model boxes detections. 

<img src="https://user-images.githubusercontent.com/4199937/112661508-e2e62f80-8e56-11eb-88e8-9f6338f819eb.png" width="30%" height="30%" alt="OAK-1 Camera" title="OAK-1 Camera">


## Hardware used

1. Raspberry pi 4 Model B with case and a cooler fan
2. Camera OAK-1 with edge compute intel Myriad X visual processor inside
3. 32GB MicroSD Class I
4. Mini switch and two Dupont wires for GPIO Button_video
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
5. Install [GPIO Library](https://gpiozero.readthedocs.io/en/stable/) to control video button

With all the above steps we have the Raspberry ready to use OAK-1 and go out to take automatic photos. it´s needed to
ensure when we connect power to Raspberry all software it´s started without keyboard and without a screen because on a
bike I will use the minimal devices possible.

## Raspberry Automatic script run

When I connect power to Raspberry-pi on my Bike, I need to start all the process automatically without any intervention.
This is solved using crontab.
```
@reboot  /home/pi/depthai/run_bike_eye.sh
```
It is used a bash script ('run_bike_eye.sh') that activate the python3 virtualenv and run the Bike_eye_pi.py python script. After that I can
start my bike route taken automatically photos using the Deep Learning Models deployed into OAK-1.
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
score_confidence = 80 # score to save image or not
```
video parameters:
```
video_duration = 20 #durations of videos 
video_fps = 15.0 #video frame per second 
video_path = './outvideo/' #path to save videos
```
Also, in this config file we can select between use MobileNetSSD or Yolo-v3 models and configure our desired object classes.
```
my_wanted_objects = ['bicycle', 'motorbike', 'aeroplane', 'bus', 'train', 'boat', 'horse', 'dog', 'cat', 'bird',
                      'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'frisbee', 'skis', 'snowboard',
                      'sports_ball', 'kite', 'skateboard', 'surfboard', 'tennis_racket']
```

## Video recording Feature

Alos, It is allowed save short videos when is pressed the mini button connected to Raspberry GPIO. These videos have a
fixed duration you can configure in the config file. This video feature saves frames, and the objects detected by the
model in real time, so if you want save something interesting while riding you only need to press this button.

While a video is been recording the video button is disabled and if you press several times it has any effect.

## Bike Installation

I use a camera clamp on the bike handlebar as you can see on images bellow.

<img src="https://user-images.githubusercontent.com/4199937/112726347-358a1f00-8f1d-11eb-84e4-be4c2b51a9ee.jpg" width="30%" height="30%" alt="OAK-1 Camera on Bike" title="OAK-1 Camera on Bike">

I carry the battery and Raspberry-pi in a little waist bag with care about ventilation.

<img src="https://user-images.githubusercontent.com/4199937/112726353-3cb12d00-8f1d-11eb-87a6-9d234ef2394f.jpg" width="30%" height="30%" alt="Battery and Raspberry in a bag" title="Battery and Raspberry in a bag">

## Battery duration and temperature

I always begin my route with the battery 100% charged, my routes has a maximun duration 1,5 hours and the battery arrives with 50% charge left.

The temperature is moving between 57 and 64 degrees celsius. The fan is configurated to operate at 60 degrees celsius.

![Raspberry_temperature](https://user-images.githubusercontent.com/4199937/112727827-8f421780-8f24-11eb-9197-0eda6dcb357a.png)

The memory comsuptions is minimal, remember all the deep_learning model process is done on the intel Myriad X edge processor.

![Raspberry_htop](https://user-images.githubusercontent.com/4199937/112727816-87827300-8f24-11eb-96b5-b5f56f5065cd.png)


## Costs

1. [OAK-1](https://store.opencv.ai/products/oak-1): 149$
2. [RaspBerry pi 4 MODEL B 4GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/): 49€
3. Raspberry case: 7.20€
4. Raspberry Fan: 5€
5. 32GB Microsd class I: 7 €
6. mini switch: 0 €, it is from an old car cd player.


## TO-DO & More Ideas

1. Change the code to DepthAI API gen2.
2. Test detecting other interesting objects with custom trained deep learnig model.
3. Make a car plates detector using a two stage pipeline and save all number plates in a log file. So I have
   saved all the cars plates seen in my bike route.
4. Count people with and without COVID-19 mask while I ride to get a COVID-19 mask use percent.
5. Connect some class detections with social networks as Twitter, Strava to upload photos while I am riding in real time with the Raspberry
   connected to Wifi mobile.
6. Detect holes on the road, fallen tree branches..., take photos and notify the city council repair services to fix it.
7. Connect a GPS module to Raspberry-Pi to add longitude and latitude to all detections.



## Results
1. I have saved some tests routes with Strava (The Strava API not allow me upload image for free on air, so I´ve uploaded manually), <a href="https://www.strava.com/athletes/79682242">You can see my tests on strava profile.</a>. 
2. Bellow you can see some real photos taken automatically while I ride. 


<img src="https://user-images.githubusercontent.com/4199937/112039057-e2425600-8b43-11eb-88a6-3969b59ddf99.jpg" width="60%" height="60%" alt="Example_1">

<img src="https://user-images.githubusercontent.com/4199937/112760109-26c36b00-8ff6-11eb-9aa3-59a87a623a1c.jpg" width="60%" height="60%" alt="Example_2">

<img src="https://user-images.githubusercontent.com/4199937/113420297-59d87680-93c9-11eb-9428-9eaa48a3213b.jpg" width="60%" height="60%" alt="Example_3">

<table>
<tr>
<td><img src="https://user-images.githubusercontent.com/4199937/113266947-17823d00-92d6-11eb-88d6-223661d778aa.jpg" alt="Example_4"></td>
<td><img src="https://user-images.githubusercontent.com/4199937/113282040-b151e600-92e6-11eb-8db4-26a170372c52.jpg" alt="Example_5"></td>
</tr>
</table>

<img src="https://user-images.githubusercontent.com/4199937/113267239-65974080-92d6-11eb-85ee-5a48e03445a6.jpg" width="60%" height="60%" alt="Example_6">

<img src="https://user-images.githubusercontent.com/4199937/113267462-aabb7280-92d6-11eb-8b3f-fbdd02477d9b.jpg" width="60%" height="60%" alt="Example_7">

<img src="https://user-images.githubusercontent.com/4199937/113276143-d131db80-92df-11eb-87ad-a27d340ee258.jpg" width="60%" height="60%" alt="Example_8">

<img src="https://user-images.githubusercontent.com/4199937/113420338-6bba1980-93c9-11eb-8031-d6e6e6fe6303.jpg" width="60%" height="60%" alt="Example_9">

<img src="https://user-images.githubusercontent.com/4199937/113283487-a8621400-92e8-11eb-8aa0-f51a57d31f4e.jpg" width="60%" height="60%" alt="Example_10">

<img src="https://user-images.githubusercontent.com/4199937/113401039-0f440380-93a3-11eb-82d6-00dec59fc162.jpg" width="60%" height="60%" alt="Example_11">

<img src="https://user-images.githubusercontent.com/4199937/113510946-93da8180-955d-11eb-8390-59569c9db600.jpg" width="60%" height="60%" alt="Example_12">

<img src="https://user-images.githubusercontent.com/4199937/113510980-b8cef480-955d-11eb-969d-28c0b05ffed9.jpg" width="60%" height="60%" alt="Example_13">

<img src="https://user-images.githubusercontent.com/4199937/113510976-b2407d00-955d-11eb-8729-db48f0801dae.jpg" width="60%" height="60%" alt="Example_14">

<img src="https://user-images.githubusercontent.com/4199937/113511003-dac87700-955d-11eb-89cd-189472b89e7f.jpg" width="60%" height="60%" alt="Example_15">

<img src="https://user-images.githubusercontent.com/4199937/113585057-fe59f300-962b-11eb-9939-e1cb3ed7480a.jpg" width="60%" height="60%" alt="Example_16">

<img src="https://user-images.githubusercontent.com/4199937/113585496-9657dc80-962c-11eb-8dee-4739886b5221.jpg" width="60%" height="60%" alt="Example_17">

<img src="https://user-images.githubusercontent.com/4199937/113585652-d15a1000-962c-11eb-9678-c5a40cb2e305.jpg" width="60%" height="60%" alt="Example_18">

<img src="https://user-images.githubusercontent.com/4199937/113585803-01091800-962d-11eb-9dcd-835ff2e12fa4.jpg" width="60%" height="60%" alt="Example_19">

<img src="https://user-images.githubusercontent.com/4199937/113586462-d53a6200-962d-11eb-8046-4cdd3aef5c13.jpg" width="60%" height="60%" alt="Example_20">

<img src="https://user-images.githubusercontent.com/4199937/113586165-75dc5200-962d-11eb-922e-8f6178760a32.jpg" width="60%" height="60%" alt="Example_21">


