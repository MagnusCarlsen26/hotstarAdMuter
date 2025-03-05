#!/bin/bash

IMAGE_PATH="imageDb/image.png" 

curl -X POST -F "image=@${IMAGE_PATH}" http://localhost:5000/upload