#!/bin/bash

split -a 3 -d -l 100 dopythona.txt in
ls -l in* | cut -c 49-54 > doxargs.txt

# xargs -a doxargs.txt  -n 1 -P 30 python3 jpl2.py -f
# ls in* | xargs -n 1 -P 30 -i python3 jpl2.py -f '{}'