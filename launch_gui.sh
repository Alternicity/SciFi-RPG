#!/bin/bash

cd /home/stuart/SciFi-RPG || exit

source .venv/bin/activate

python main.py

read -p "Press enter to close..."