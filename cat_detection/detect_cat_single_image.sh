#!/bin/bash

rm tmp/*
cp $1 tmp/

source ../app/venv/bin/activate
python detect.py --image_folder tmp
