#!/bin/bash


convert -append *100-*.png 100.png
convert -append *1000-*.png 1000.png
convert -append *10000-*.png 10000.png
convert -append *500-*.png 500.png
convert -append *5000-*.png 5000.png
convert -append *50000-*.png 50000.png

convert +append 100.png 500.png 1000.png 5000.png 10000.png 50000.png out.PNG

rm *.png