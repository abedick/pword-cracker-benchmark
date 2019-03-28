#!/bin/bash


BOOKMARK="bookmark.txt"

line=$(head -n 1 $BOOKMARK)
echo $line

line=$((10#$line + 1))
echo $line > $BOOKMARK

python3 main.py &> data/$line.txt

#rc=$?

#if [[ $rc != 0 ]]; then 
	#echo "error"
	#sleep 96
	#/usr/bin/git add .
	#/usr/bin/git git commit -am "err or fin"
	#/usr/bin/git push

#else


	#echo "reboot"
	#/usr/sbin/reboot
#fi
