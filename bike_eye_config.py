### deep learning model to use
# mobilenet
# model_name = 'mobilenet'
# nn_model = '/home/pi/depthai/resources/nn/mobilenet-ssd/mobilenet-ssd.blob.sh14cmx14NCE1'
# nn_model_config = '/home/pi/depthai/resources/nn/mobilenet-ssd/mobilenet-ssd.json'
# file_labels = 'labels_mobilenet_ssd.txt'
# # class labels I want to take photo images
# my_wanted_objects = ['aeroplane', 'bicycle', 'bird', 'boat', 'bus', 'car', 'cat', 'cow', 'dog', 'horse', 'motorbike',
#                       'sheep', 'train']

# yolo-v3
model_name = 'yoloV3'
nn_model = '/home/pi/depthai/resources/nn/yolo-v3/yolo-v3.blob.sh14cmx14NCE1'
nn_model_config = '/home/pi/depthai/resources/nn/yolo-v3/yolo-v3.json'
file_labels = 'labels_yolo_v3.txt'
# class labels I want to take photo images
my_wanted_objects = ['bicycle', 'motorbike', 'aeroplane', 'boat', 'horse', 'dog', 'cat', 'bird',
                      'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'frisbee', 'skis', 'snowboard',
                      'sports_ball', 'kite', 'skateboard', 'surfboard', 'tennis_racket']

### images parameters
img_path = './outimg/' #path to save images
frecuency_img = 1  # n seconds for waiting between write every image to disk
score_confidence = 90  # score to be save image or not

### video parameters
video_duration = 10 #durations of videos
video_fps = 60.0 #video frame per second
video_path = './outvideo/' #path to save videos