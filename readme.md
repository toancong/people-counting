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
