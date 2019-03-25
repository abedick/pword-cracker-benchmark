

import subprocess
import re
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

	sizes = [10,50,100,500,1000]
	ltr = ["a", "b", "c"]

	trials = []
	for x in sizes:
		for y in ltr:
			trials.append(str(x)+"-"+y)

	# for generating hash files for the dictionary attacks
	gen_hash_files(sizes, ltr)

	'''
		Dictionary Attacks
	'''

	# for running john with dictionary list rockyou
	start_john_dict(trials)

	# for running hash_cat with dictionary list rockyou
	start_hc_dict(trials)

	'''
		Brute Force Attacks
	'''

	# for running john with brute froce
	start_john_brute(trials)

	# for running hans_cat with brute force
	start_hc_brute(trials)

def gen_hash_files(sizes, ltr):
	if os.path.exists("hashes"):
		return

	# Generate hashed files for dictionary attacks
	print("generating hashed word lists for dictionary attacks")
	mkdir("./hashes/md5/random")
	mkdir("./hashes/sha256/random")
	words = sample_wordList("./input/100_000.txt")

	for x in sizes:
		for y in ltr:
			gen_hashes(words, "random", 99_999, x, y)

	# generate hashes files for brute force attacks
	print("generating hashed word lists for brute force attacks")
	mkdir("./hashes/md5/fivechar")
	mkdir("./hashes/sha256/fivechar")
	words = gen_wordList_fivechar("lists/rockyou.txt")

	for x in sizes:
		for y in ltr:
			if x < 1001:
				gen_hashes(words, "fivechar", 7499, x, y)

def gen_hashes(words, dst, ra, size, ltr):

	md5 = open("./hashes/md5/"+dst+"/"+str(size)+"-"+ltr+".txt", "w")
	sha = open("./hashes/sha256/"+dst+"/"+str(size)+"-"+ltr+".txt", "w")

	found = {}
	i = 0
	while i < size:

		target = random.randint(0,ra)
		if hasattr(found, str(target)):
			continue
		else:
			found[str(target)] = True
			i += 1

		md5_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-1", words[target]])
		sha_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-5", words[target]])

		md5.write((str(md5_hash))[2:-3] + "\r\n")
		sha.write((str(sha_hash))[2:-3] + "\r\n")

	md5.close()
	sha.close()

'''
	John the Ripper
'''

def start_john_dict(trials):
	print("running john with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:
		run_john_dict("lists/rockyou.txt", "./hashes/md5/random/"+trial+".txt", "md5crypt", "md5_"+trial, str(i), str(len(trials)*2))		
		run_john_dict("lists/rockyou.txt", "./hashes/sha256/random/"+trial+".txt", "sha256crypt", "sha_"+trial, str(i+1), str(len(trials)*2))
		i += 2

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

def start_john_brute(trials):
	print("running john with brute force attack")
	i = 1
	for trial in trials:
		run_john_brute("md5crypt", "./hashes/md5/fivechar/"+trial+".txt", "md5_"+trial, str(i), str(len(trials)*2))
		run_john_brute("sha256crypt", "./hashes/sha256/fivechar/"+trial+".txt", "sha256_"+trial, str(i+1), str(len(trials)*2))
		i += 2

def run_john_brute(format, hashFile, fname, x, y):
	print("("+x+"/"+y+") john " + format + " " + fname)

	path = "output/john/brute/"
	mkdir(path)

	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	subprocess.call(["john", "--incremental=lower", "--format="+format, hashFile],stdout=f, stderr=g)

	# Remove the pot
	subprocess.call(["rm", "/root/.john/john.pot"])
	subprocess.call(["rm", "/root/.john/john.log"])

'''
	hashcat
'''

def start_hc_dict(trials):
	print("running hashcat with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:
		run_hc_dict("lists/rockyou.txt", "./hashes/md5/random/"+trial+".txt", "500", "md5_"+trial, str(i), str(len(trials)*2))
		run_hc_dict("lists/rockyou.txt", "./hashes/sha256/random/"+trial+".txt", "7400", "sha_"+trial, str(i+1), str(len(trials)*2))
		i += 2

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

def start_hc_brute(trials):
	print("running hashcat with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:
		run_hc_brute("./hashes/md5/fivechar/"+trial+".txt", "500", "md5_"+trial, str(i), str(len(trials)*2))
		run_hc_brute("./hashes/sha256/fivechar/"+trial+".txt", "7400", "sha_"+trial, str(i+1), str(len(trials)*2))
		i += 2

def run_hc_brute(hashFile, format, fname, x, y):
	print("("+x+"/"+y+") hashcat " + format + " " + fname)

	path = "output/hc/brute/"
	mkdir(path)
	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	# hashcat -a 3 -m 500 l?l?l?l?
	subprocess.call(["hashcat", "-a", "3", "-m", format, hashFile, "?l?l?l?l?l", "--force"],stdout=f, stderr=g)

	# Remove the pot and session
	subprocess.call(["rm", "/root/.hashcat/hashcat.potfile"])
	subprocess.call(["rm", "-rf", "/root/.hashcat/sessions"])


''' 
	helpers
'''

# Reds a file and returns it as an array with each element a single line
def sample_wordList(fpath):
	file = open(fpath, "r", encoding="ISO-8859-1")	
	return file.read().splitlines()	

# Scans file fpath for the first 7500 5 lowercase words; returns them as array
def gen_wordList_fivechar(fpath):
	f = open(fpath, "r")
	res = []
	while len(res) < 7500:
		ln = f.readline().strip()
		if [ln] == re.findall(r"[a-z][a-z][a-z][a-z][a-z]", ln):
			res.append(ln)
	return res	

# makes fpath dir is not exist
def mkdir(fpath):
	if not os.path.exists(fpath):
		os.makedirs(fpath)

main()