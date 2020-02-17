#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_for_predict_cpu.txt
export FLASK_APP=app.py
flask run
