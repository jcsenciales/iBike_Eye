from pathlib import Path
import numpy as np
import cv2  # opencv - display the video stream
import depthai  # access the camera and its data packets
import time
import glob
from bike_eye_config import *
from gpiozero import Button  # to control Rasberry_pi GPIO


device = depthai.Device('', False)
##Auto Focus does not work well while ride, because you go faster than focus works
#device.request_af_mode(depthai.AutofocusMode.AF_MODE_AUTO)
#depthai.CameraControl.Command.MOVE_LENS
#autofocus continuo
#device.request_af_mode(depthai.AutofocusMode.AF_MODE_CONTINUOUS_VIDEO)
# Create the pipeline using the 'previewout & metaout'. 'color' stream, establishing the first connection to the device.
# use previewout or color, not both at same time because image written are overwrite.
pipeline = device.create_pipeline(config={'streams': ['color', 'metaout'],
                                          'ai': {
                                              'blob_file': nn_model,
                                              'blob_file_config': nn_model_config,
                                              'blob_file2': '', 'blob_file_config2': '', 'calc_dist_to_bb': False,
                                              'keep_aspect_ratio': False,
                                              'camera_input': 'rgb', 'shaves': 14, 'cmx_slices': 14, 'NN_engines': 1},
                                          'ot': {'max_tracklets': 20, 'confidence_threshold': 0.5},
                                          'board_config': {'swap_left_and_right_cameras': True,
                                                           'rgb_fov_deg': 68.7938,
                                                           'store_to_eeprom': False, 'clear_eeprom': False,
                                                           'override_eeprom': False},
                                          'camera': {'rgb': {'resolution_h': 1080, "resolution_w":1920, 'fps': 30.0}},
                                          'app': {'sync_video_meta_streams': False, 'sync_sequence_numbers': False,
                                                  'usb_chunk_KiB': 64}})

#load label class for this model
labels = np.loadtxt(file_labels, dtype=str)

if pipeline is None:
    raise RuntimeError('Pipeline creation failed!')

detections = []

# get image file index to not over write an existing image
total_imgs = len(glob.glob(img_path + '*.jpg'))
_write_img = total_imgs + 1

# get video file index to not over write an existing video
total_videos = len(glob.glob(video_path + '*.avi'))
_write_video = total_videos + 1


_labels_detected = []

# Manual fixed focus
focus = 118
cam_c = depthai.CameraControl.CamId.RGB
cmd_set_focus = depthai.CameraControl.Command.MOVE_LENS
_set_focus_manual = 0


#image time variable to control when was saved the last image
_time_write = time.perf_counter()

#video control variables initial setting
save_video = False
video_out = None
_frames_saved = 0
_total_frames = video_fps * video_duration
video_button = Button(17)

while True:  # Retrieve data packets from the device. # A data packet contains the video frame data.
    nnet_packets, data_packets = pipeline.get_available_nnet_and_data_packets()

    #check video button is pressed
    if video_button.is_pressed:
        save_video = True

    for nnet_packet in nnet_packets:
        detections = list(nnet_packet.getDetectedObjects())
        # print(detections)
    _labels_detected = []
    for packet in data_packets:

        if packet.stream_name == 'previewout':
            meta = packet.getMetadata()
            camera = meta.getCameraName()
            window_name = 'previewout-' + camera
            data = packet.getData()
            # change shape (3, 300, 300) -> (300, 300, 3)            
            data0 = data[0, :, :]
            data1 = data[1, :, :]
            data2 = data[2, :, :]
            frame = cv2.merge([data0, data1, data2])

            img_h = frame.shape[0]
            img_w = frame.shape[1]

            for detection in detections:
                pt1 = int(detection.x_min * img_w), int(detection.y_min * img_h)
                pt2 = int(detection.x_max * img_w), int(detection.y_max * img_h)
                label = labels[int(detection.label)]
                score = int(detection.confidence * 100)
                # insert labels to be saved only if greater than _score_confidence
                if score >= _score_confidence:
                    _labels_detected.append(label)

                cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 1)
                cv2.putText(frame, str(score) + ' ' + label, (pt1[0] + 2, pt1[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 1)

#            cv2.imshow(window_name, frame)

            if _write_img < 25000:
                some_wanted_detected = len([obj for obj in my_wanted_objects if obj in _labels_detected])
                _current_time = time.perf_counter()
                if some_wanted_detected > 0 and (_current_time - _time_write) > _frecuency_img:
                    print('Elapse Time from before image writen is: %s' % (_current_time - _time_write))
                    cv2.imwrite(filename="%simg_%s_%s.jpg" % (img_path, model_name, _write_img), img=frame)
                    _write_img = _write_img + 1
                    _time_write = time.perf_counter()

        elif packet.stream_name == 'color': #this is used in real test, not the previewout
             _labels_detected = []
             meta = packet.getMetadata()
             packetData = packet.getData()
             w = meta.getFrameWidth()
             h = meta.getFrameHeight()
             yuv420p = packetData.reshape((h * 3 // 2, w))
             bgr = cv2.cvtColor(yuv420p, cv2.COLOR_YUV2BGR_IYUV)
             scale = 0.5
             bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

             img_h = bgr.shape[0]
             img_w = bgr.shape[1]

             for detection in detections:
                 #coordenates properly calculate if in config 'keep_aspect_ratio': False
                 pt1 = int(detection.x_min * img_w), int(detection.y_min * img_h)
                 pt2 = int(detection.x_max * img_w), int(detection.y_max * img_h)
                 label = labels[int(detection.label)]
                 score = int(detection.confidence * 100)
                 # insert labels to be saved only if greater than _score_confidence
                 if score >= score_confidence:
                     _labels_detected.append(label)

                 cv2.rectangle(bgr, pt1, pt2, (0, 0, 255), 1)
                 cv2.putText(bgr, str(score) + ' ' + label, (pt1[0] + 2, pt1[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                             (0, 255, 0), 1)

             if _write_img < 25000:
                 some_wanted_detected = len([obj for obj in my_wanted_objects if obj in _labels_detected])
                 _current_time = time.perf_counter()
                 if some_wanted_detected > 0 and (_current_time - _time_write) > frecuency_img:
                     print('Elapse Time from before image writen is: %s' % (_current_time - _time_write))
                     cv2.imwrite(filename="%sBig_img_%s_%s.jpg" % (img_path, model_name, _write_img), img=bgr)
                     _write_img = _write_img + 1
                     _time_write = time.perf_counter()

             # save video
             if save_video:
                 #create video writer first time
                 if video_out is None:
                     size = (img_w, img_h)
                     fourcc = cv2.VideoWriter_fourcc(*'XVID')
                     video_out = cv2.VideoWriter('%svideo_%s_%s.avi' % (video_path, model_name, _write_video), fourcc, 20, size)
                     _init_video_time = time.perf_counter()
                     _frames_saved = 0
                     print('VIDEO INIT')

                 #_current_video_time = time.perf_counter()
                 #if (_current_video_time - _init_video_time) < video_duration:
                 if _frames_saved < _total_frames:
                     video_out.write(bgr)
                     _frames_saved += 1
                 else:
                     # Close video output file if was opened
                     if video_out is not None:
                         video_out.release()
                     video_out = None
                     save_video = False
                     _write_video = _write_video + 1
                     print('VIDEO SAVED')

             #IMPORTANT:: you need to comment the bellow line when you don´t use screen monitor
             cv2.imshow("color", bgr)


    if cv2.waitKey(1) == ord('q'):
        break

    if cv2.waitKey(1) == ord('v'):
        save_video = True
    #set focus manual to a 12 meters distance more or less, Auto Focus does not work well while ride
    #repeat te setting 10 times because when the camera start not get the configuration at first.
    if _set_focus_manual < 10:
        _set_focus_manual += 1
        #print('INITIAL CAM CAM CAM %s Focus%s' % (cam_c, focus))
        device.send_camera_control(cam_c, cmd_set_focus, str(focus))

# Deleted the pipeline after exiting the loop. Otherwise device will continue working.
del pipeline
del device
