#!/bin/bash

for f in *.dat
do
	mprof plot $f  -o $f.png
done
