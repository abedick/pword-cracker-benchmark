

import subprocess
import os
import random
from io import StringIO

# For john the ripper
# john --wordlist=lists/rockyou.txt --format=md5crypt ./hashes/100_000_md5.txt

# For hashcat
# hashcat -a 0 -m 500 ./hashes/100_000_md5.txt ./lists/rockyou.txt

# for bruteforce hashcat
# -a 3 -m 500 l?l?l?l?

# for bruteforce john
# john --incremental=lower --format
# modify john.conf [incremental:lower]

def main():

	sizes = [10,50,100,500,1000,5000]
	ltr = ["a", "b", "c"]

	if not os.path.exists("./hashes"):
		
		print("generating hashed word lists")

		mkdir("./hashes/md5")
		mkdir("./hashes/sha256")
		
		words = sample_wordList("./input/100_000.txt")

		for x in sizes:
			for y in ltr:
				gen_hashes_sample(words,x,y)

	mkdir("./output")

	trials = []
	for x in sizes:
		for y in ltr:
			trials.append(str(x)+"-"+y)

	# # for running john with dictionary list rockyou
	# print("running john with dictionary attack using list rockyou.txt")
	# i = 1
	# for trial in trials:
	# 	run_john_dict(
	# 		"lists/rockyou.txt", 
	# 		"./hashes/md5/"+trial+".txt", 
	# 		"md5crypt", 
	# 		"md5_"+trial,
	# 		str(i), 
	# 		str(len(trials)))
	# 	i += 1

	# # for running hash_cat with dictionary list rockyou
	# print("running hashcat with dictionary attack using list rockyou.txt")
	# i = 1
	# for trial in trials:
	# 	run_hc_dict(
	# 		"lists/rockyou.txt", 
	# 		"./hashes/md5/"+trial+".txt", 
	# 		"md5crypt", 
	# 		"md5_"+trial,
	# 		str(i), 
	# 		str(len(trials)))
	# 	i += 1


	# # for running john with brute froce
	# # for running hans_cat with brute force

	
def sample_wordList(fpath):
	file = open(fpath, "r", encoding="ISO-8859-1")	
	return file.read().splitlines()


def gen_hashes_sample(words, size, ltr):

	md5 = open("./hashes/md5/"+str(size)+"-"+ltr+".txt", "w")
	sha = open("./hashes/sha256/"+str(size)+"-"+ltr+".txt", "w")

	for _ in range(size):
		target = random.randint(0,99_999)

		md5_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-1", words[target]])
		sha_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-5", words[target]])

		md5.write((str(md5_hash))[2:-3] + "\r\n")
		sha.write((str(sha_hash))[2:-3] + "\r\n")

	md5.close()
	sha.close()


def run_john_dict(dic, hashFile, format, fname, x, y):
	print("("+x+"/"+y+") john " + format + " " + fname)

	path = "output/john/dict/"
	mkdir(path)
	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	# john --wordlist=lists/rockyou.txt --format=md5crypt ./hashes/100_000_md5.txt
	subprocess.call(["john", "--wordlist="+dic, "--format="+format, hashFile],stdout=f, stderr=g)

	# Remove the pot
	subprocess.call(["rm", "/root/.john/john.pot"])
	subprocess.call(["rm", "/root/.john/john.log"])


def run_hc_dict(dic, hashFile, format, fname, x, y):
	print("("+x+"/"+y+") hashcat " + format + " " + fname)

	path = "output/hc/dict/"
	mkdir(path)
	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	# hashcat -a 0 -m 500 ./hashes/100_000_md5.txt ./lists/rockyou.txt
	subprocess.call(["hashcat", "-a", "0", "-m", format, hashFile, dic, "--force"],stdout=f, stderr=g)

	# Remove the pot and session
	subprocess.call(["rm", "/root/.hashcat/hashcat.potfile"])
	subprocess.call(["rm", "-rf", "/root/.hashcat/sessions"])


def mkdir(fpath):
	if not os.path.exists(fpath):
		os.makedirs(fpath)

main()