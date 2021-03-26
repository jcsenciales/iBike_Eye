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

iBike_Eye is a project to automatically take photos or make videos while you are riding. For that purpose I used an
OAK-1 embedded 4k camera and neural compute edge compute intel processor. I upload deep learning models into this camera,
and the camera run the deep-learning model and return detections using USB-3 interface. So I need some mini computer to
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
3. Mini switch and two wires for GPIO Button_video
4. Battery Power Bank 5v USB 10400 mAh
5. Two USB wires to connect with the camera and supply power to Rasberry-pi

<img src="https://user-images.githubusercontent.com/4199937/112680418-a3770d80-8e6d-11eb-9669-4fe94257d099.jpg" width="40%" height="40%" alt="RaspBerry Pi y OAK-1 Camera" title="RaspBerry Pi, Battery and OAK-1 Camera">



## Deep Learning Models used
1. Rasberri pi 4
2. Camera OAK-1 with edge visual compute intel Myriad X inside
3. Battery 5v USB 10400ma

## Rasberry Configuration
1. Rasberri pi 4
2. Camera OAK-1 with edge visual compute intel Myriad X inside
3. Battery 5v USB 10400ma

## Rasberry Automatic script run
1. Rasberri pi 4
2. Camera OAK-1 with edge visual compute intel Myriad X inside
3. Battery 5v USB 10400ma

## iBike Eye Configuration
1. Rasberri pi 4
2. Camera OAK-1 with edge visual compute intel Myriad X inside
3. Battery 5v USB 10400ma

## Bike Instalation

## TO-DO , TO-TEST , MORE Ideas

## Examples
1. I save my test routes with Strava (The Strava API not allowe upload image for free, so I upload manually)
1.1 <a href="https://www.strava.com/athletes/79682242">You can see my test on strava!</a>


![Example_1](https://user-images.githubusercontent.com/4199937/112039057-e2425600-8b43-11eb-88a6-3969b59ddf99.jpg)

<img src="https://user-images.githubusercontent.com/4199937/112039057-e2425600-8b43-11eb-88a6-3969b59ddf99.jpg" width="50%" height="50%" alt="Example_1">
