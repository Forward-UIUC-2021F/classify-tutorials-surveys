#!/bin/bash
WD=$1
KEYWORD=$2

cd $WD/matthew-kurapatti-classify-tutorials-surveys

source env/bin/activate
cd google_scholars
python3 scholars_rf.py "$KEYWORD"