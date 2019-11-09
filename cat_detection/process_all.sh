#!/bin/bash

source venv/bin/activate

for file in $(ls -1 ../data/*/*)
do
    echo "Processing $file at $(date)" | tee -a process_all.log
    python pipeline.py $file | tee -a process_info.tsv
done

