## SETUP

### For MacOS if you want to display GUI in python

1. `brew install socat`
2. Download and install xquartz https://www.xquartz.org/
3. Setting
`open -a XQuartz` then config “allow connections from network clients” is checked “on” on Security tab of Preferences
(Source: https://cntnr.io/running-guis-with-docker-on-mac-os-x-a14df6a76efc)
4. `docker-compose pull`

## RUN

`sh run`
or
`docker-compose run --rm app python app/app.py` after start socat & XQuartz
or
`sh run python app/detect.py` to run a custom command

## Example

```
sh run python app/detect.py
```
```
sh run darknet detect cfg/yolo.cfg yolo.weights data/dog.jpg
```
```
sh run darknet detector demo cfg/coco.data cfg/yolo.cfg yolo.weights app/storage/sample.mp4
```

### use tiny version
```
sh run darknet detector test cfg/voc.data cfg/tiny-yolo-voc.cfg tiny-yolo-voc.weights data/dog.jpg
```
```
sh run darknet detector demo cfg/voc.data cfg/tiny-yolo-voc.cfg tiny-yolo-voc.weights app/storage/sample.mp4
```

## Training YOLO on VOC
Learn more: https://pjreddie.com/darknet/yolo/#train-voc

1. Get The Pascal VOC Data
Download files and unzip to `train` folder

2. Generate Labels for VOC
```
docker-compose run --rm app bash -c "cd app/train && python voc_label.py"
```

3. Modify Cfg for Pascal Data
I updated the config file in train/cfg/voc.data and volume it into docker

4. Download Pretrained Convolutional Weights
Download file to `train` folder
```
wget https://pjreddie.com/media/files/darknet19_448.conv.23
```

5. Train The Model
```
docker-compose run --rm app ./darknet detector train app/train/cfg/voc.data cfg/yolo-voc.cfg app/train/darknet19_448.conv.23
```

* Train from a checkpoint
```
docker-compose run --rm app ./darknet detector train app/train/cfg/voc.data cfg/yolo-voc.cfg app/train/backup/yolo-voc.backup
```

## NOTE:
có 1 vài output quan trọng trong quá trình train:
 - Region Avg IOU: 0.164715 càng tiến về 1 càng tốt, tức là tỉ lệ giao hợp càng gần 100% càng tốt
 - 426.823456 avg: trung bình lỗi càng thấp càng tốt, 0.060730 avg, you can stop training
 - kết quả sau khi train nằm trong folder backup định nghĩa trong config, ở trường hợp của mình là sau mỗi 100 iteration thì nó backup 1 lần để làm checkpoint
