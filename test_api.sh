#!/bin/bash

IMAGE_PATH="/home/khushal/hobby/hostarADMuter/imageDb/1741357290.png" 

curl -X GET -F "image=@${IMAGE_PATH}" "http://localhost:5000/predict_image?prompt=what%20do%20you%20see%20in%20this%20photo%3F"