

import subprocess
import re
import os
import random
from io import StringIO
from passlib.hash import lmhash
import hashlib

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

	mem = True
	if mem:
		mkdir("output/john/dict/mem")
		mkdir("output/john/brute/mem")
		mkdir("output/hc/dict/mem")
		mkdir("output/hc/brute/mem")

	# for generating hash files for the dictionary attacks
	gen_hash_files(sizes, ltr)

	'''
		Dictionary Attacks
	'''

	# for running john with dictionary list rockyou
	#start_john_dict(trials, mem)

	# for running hash_cat with dictionary list rockyou
	#start_hc_dict(trials, mem)

	'''
		Brute Force Attacks
	'''

	# for running john with brute froce
	#start_john_brute(trials, mem)

	# for running hans_cat with brute force
	#start_hc_brute(trials, mem)

def gen_hash_files(sizes, ltr):
	if os.path.exists("hashes"):
		return

	# Generate hashed files for dictionary attacks
	print("generating hashed word lists for dictionary attacks")
	mkdir("./hashes/md5/random")
	mkdir("./hashes/sha1/random")
	mkdir("./hashes/lm/random")
	words = sample_wordList("./input/100_000.txt")

	for x in sizes:
		for y in ltr:
			gen_hashes(words, "random", 99_999, x, y)

	# generate hashes files for brute force attacks
	print("generating hashed word lists for brute force attacks")
	mkdir("./hashes/md5/fivechar")
	mkdir("./hashes/sha1/fivechar")
	mkdir("./hashes/lm/fivechar")
	words = gen_wordList_fivechar("lists/rockyou.txt")

	for x in sizes:
		for y in ltr:
			if x < 1001:
				gen_hashes(words, "fivechar", 7499, x, y)

def gen_hashes(words, dst, ra, size, ltr):

	md5 = open("./hashes/md5/"+dst+"/"+str(size)+"-"+ltr+".txt", "w")
	sha = open("./hashes/sha1/"+dst+"/"+str(size)+"-"+ltr+".txt", "w")
	lm = open("./hashes/lm/"+dst+"/"+str(size)+"-"+ltr+".txt", "w")

	index_list = open("./hashes/indexlist"+str(size)+"-"+ltr+".txt","w")

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
		sha_hash = hashlib.sha1(bytes(words[target], 'utf-8')).hexdigest()
		lm_hash = lmhash.hash(words[target])

		md5.write((str(md5_hash))[2:-3] + "\r\n")
		sha.write(str(sha_hash) + "\r\n")
		lm.write(str(lm_hash) + "\r\n")

	md5.close()
	sha.close()
	lm.close()

	index_list.write(str(found))
	index_list.close()

'''
	John the Ripper
'''

def start_john_dict(trials, mem):
	print("running john with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:

		args1 = ["lists/rockyou.txt", "./hashes/md5/random/"+trial+".txt", "md5crypt", "md5_"+trial, str(i), str(len(trials)*3
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"john_dict", mem, "./output/john/dict/mem/md5_"+trial+".dat")

		args2 = ["lists/rockyou.txt", "./hashes/sha1/random/"+trial+".txt", "Raw-SH1", "sha_"+trial, str(i+1), str(len(trials)*3)]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"john_dict", mem, "./output/john/dict/mem/sha_"+trial+".dat")

		args3 = ["lists/rockyou.txt", "./hashes/lm/random/"+trial+".txt", "LM", "lm_"+trial, str(i+2), str(len(trials)*3)]
		args3 = ','.join(str(x) for x in args3)
		forkExec(args3,"john_dict", mem, "./output/john/dict/mem/lm_"+trial+".dat")		

		i += 3

def start_john_brute(trials, mem):
	print("running john with brute force attack")
	i = 1
	for trial in trials:

		args1 = ["md5crypt", "./hashes/md5/fivechar/"+trial+".txt", "md5_"+trial, str(i), str(len(trials)*2)]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"john_brute", mem, "./output/john/brute/mem/md5_"+trial+".dat")

		args2 = ["sha256crypt", "./hashes/sha256/fivechar/"+trial+".txt", "sha256_"+trial, str(i+1), str(len(trials)*2)]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"john_brute", mem, "./output/john/brute/mem/sha_"+trial+".dat")

		i += 2

'''
	hashcat
'''

def start_hc_dict(trials, mem):
	print("running hashcat with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:

		args1 = ["lists/rockyou.txt", "./hashes/md5/random/"+trial+".txt", "500", "md5_"+trial, str(i), str(len(trials)*2)]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"hc_dict", mem, "./output/hc/dict/mem/md5_"+trial+".dat")

		args2 = ["lists/rockyou.txt", "./hashes/sha256/random/"+trial+".txt", "7400", "sha_"+trial, str(i+1), str(len(trials)*2)]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"hc_dict", mem, "./output/hc/dict/mem/sha_"+trial+".dat")

		i += 2

def start_hc_brute(trials, mem):
	print("running hashcat with dictionary attack using list rockyou.txt")
	i = 1
	for trial in trials:
		args1 = ["./hashes/md5/fivechar/"+trial+".txt", "500", "md5_"+trial, str(i), str(len(trials)*2)]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"john_dict", mem, "./output/hc/brute/mem/md5_"+trial+".dat")

		args2 = ["./hashes/sha256/fivechar/"+trial+".txt", "7400", "sha_"+trial, str(i+1), str(len(trials)*2)]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"john_dict", mem, "./output/hc/brute/mem/sha_"+trial+".dat")

		i += 2

''' 
	helpers
'''

def forkExec(args, ptype, mem, outputFile):
		if mem:
			subprocess.call(["mprof", "run", "-M", "-C", "-o",outputFile, "python3","run.py", ptype, args])
		else:
			subprocess.call(["python3","run.py", ptype, args])

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
