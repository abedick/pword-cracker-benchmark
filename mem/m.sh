#!/bin/bash

for f in *md5*.png
do	
	# N="hd-"$f
	# mv $f $N
	# mv $N ../../../../mem
	mv $f md5/
	# mv $f size/
done
