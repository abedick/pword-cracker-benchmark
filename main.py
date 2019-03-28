import subprocess
import re
import os
import sys
import random
import ast
from io import StringIO
from passlib.hash import lmhash
import hashlib

def main():

	sizes = [100,500,1000,5000,10000,50000]
	ltr = ["a","b","c", "d"]

	trials = []
	for x in sizes:
		for y in ltr:
			trials.append(str(x)+"-"+y)

	tests = []
	try:
		f = open("./remaining_tests.txt", "r")
		t = f.read()
		tests = ast.literal_eval(t)
	except OSError:

		t = ["1","2","3"]
		tests = []
		for x in trials:
			for y in t:
				tests.append(x + ":" + y)
		
		f = open("./remaining_tests.txt", "w")
		f.write(str(tests))
		sys.exit(1)

	if len(tests) == 0:
		sys.exit(1)
					

	thisInt = random.randint(0,len(tests)-1)
	thisOne = tests[thisInt].split(":")
	print(thisOne)

	# tests.remove(tests[thisInt])
	# f = open("./remaining_tests.txt", "w")
	# f.write(str(tests))

	mem = True
	if mem:
		mkdir("output/john/dict/mem")
		mkdir("output/john/brute/mem")
		mkdir("output/hc/dict/mem")
		mkdir("output/hc/brute/mem")
		mkdir("output/stdout")


	start_john_dict(thisOne, mem)
	#start_hc_brute(thisOne, mem)
	#start_john_brute(thisOne, mem)
	#start_hc_dict(thisOne, mem)

	sys.exit(0)
	# for generating hash files for the dictionary attacks
	#gen_hash_files(sizes, ltr)

def gen_hash_files(sizes, ltr):
	if os.path.exists("hashes"):
		return

	# Generate hashed files for dictionary attacks
	print("generating hashed word lists for dictionary attacks")
	mkdir("./hashes/md5/random")
	mkdir("./hashes/sha1/random")
	mkdir("./hashes/lm/random")
	words = sample_wordList("./input/1_000_000.txt")

	for x in sizes:
		for y in ltr:
			gen_hashes(words, "random", 999_990, x, y)

	# generate hashes files for brute force attacks
	print("generating hashed word lists for brute force attacks")
	mkdir("./hashes/md5/fivechar")
	mkdir("./hashes/sha1/fivechar")
	mkdir("./hashes/lm/fivechar")
	# words = gen_wordList_fivechar("lists/rockyou.txt")

	for x in sizes:
		for y in ltr:
			#if x < 1001:
			gen_hashes(words, "fivechar", 999_990, x, y)

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

		word = words[target]

		try:
			md5_hash = hashlib.md5(bytes(word, 'utf-8')).hexdigest()
			sha_hash = hashlib.sha1(bytes(word, 'utf-8')).hexdigest()
			lm_hash = lmhash.hash(word)

			md5.write(str(md5_hash) + "\r\n")
			sha.write(str(sha_hash) + "\r\n")
			lm.write(str(lm_hash) + "\r\n")
		except:
			i  -= 1

	md5.close()
	sha.close()
	lm.close()

	index_list.write(str(found))
	index_list.close()

'''
	John the Ripper
'''

def start_john_dict(trial, mem):
	print("running john with dictionary attack using list rockyou.txt")

	if trial[1] == "1":	
		args1 = ["lists/rockyou.txt", "./hashes/md5/random/"+trial[0]+".txt", "Raw-MD5", "md5_"+trial[0]]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"john_dict", mem, "./output/john/dict/mem/md5_"+trial[0]+".dat")

	elif trial[1] == "2":
		args2 = ["lists/rockyou.txt", "./hashes/sha1/random/"+trial[0]+".txt", "Raw-SHA1", "sha_"+trial[0]]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"john_dict", mem, "./output/john/dict/mem/sha_"+trial[0]+".dat")

	elif trial[1] == "3":
		args3 = ["lists/rockyou.txt", "./hashes/lm/random/"+trial[0]+".txt", "LM", "lm_"+trial[0]]
		args3 = ','.join(str(x) for x in args3)
		forkExec(args3,"john_dict", mem, "./output/john/dict/mem/lm_"+trial[0]+".dat")		


def start_john_brute(trial, mem):
	print("running john with brute force attack")

	if trial[1] == "1":	
		args1 = ["Raw-MD5", "./hashes/md5/fivechar/"+trial[0]+".txt", "md5_"+trial[0]]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"john_brute", mem, "./output/john/brute/mem/md5_"+trial[0]+".dat")

	elif trial[1] == "2":	
		args2 = ["Raw-SHA1", "./hashes/sha1/fivechar/"+trial[0]+".txt", "sha1_"+trial[0]]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"john_brute", mem, "./output/john/brute/mem/sha_"+trial[0]+".dat")

	elif trial[1] == "3":	
		args3 = ["LM", "./hashes/lm/fivechar/"+trial[0]+".txt", "lm"+trial[0]]
		args3 = ','.join(str(x) for x in args3)
		forkExec(args3,"john_brute", mem, "./output/john/brute/mem/lm_"+trial[0]+".dat")



'''
	hashcat
'''

def start_hc_dict(trial, mem):
	print("running hashcat with dictionary attack using list rockyou.txt")

	if trial[1] == "1":	
		args1 = ["lists/rockyou.txt", "./hashes/md5/random/"+trial[0]+".txt", "0", "md5_"+trial[0]]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"hc_dict", mem, "./output/hc/dict/mem/md5_"+trial[0]+".dat")

	elif trial[1] == "2":	
		args2 = ["lists/rockyou.txt", "./hashes/sha1/random/"+trial[0]+".txt", "100", "sha_"+trial[0]]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"hc_dict", mem, "./output/hc/dict/mem/sha_"+trial[0]+".dat")

	elif trial[1] == "3":	
		args3 = ["lists/rockyou.txt", "./hashes/lm/random/"+trial[0]+".txt", "3000", "sha_"+trial[0]]
		args3 = ','.join(str(x) for x in args3)
		forkExec(args3,"hc_dict", mem, "./output/hc/dict/mem/lm_"+trial[0]+".dat")



def start_hc_brute(trial, mem):
	print("running hashcat with brute force attack")

	if trial[1] == "1":	
		args1 = ["0", "./hashes/md5/fivechar/"+trial[0]+".txt", "md5_"+trial[0]]
		args1 = ','.join(str(x) for x in args1)
		forkExec(args1,"hc_brute", mem, "./output/hc/brute/mem/md5_"+trial[0]+".dat")

	elif trial[1] == "2":	
		args2 = ["100", "./hashes/sha1/fivechar/"+trial[0]+".txt", "sha1_"+trial[0]]
		args2 = ','.join(str(x) for x in args2)
		forkExec(args2,"hc_brute", mem, "./output/hc/brute/mem/sha_"+trial[0]+".dat")

	elif trial[1] == "3":	
		args3 = ["3000", "./hashes/lm/fivechar/"+trial[0]+".txt", "lm"+trial[0]]
		args3 = ','.join(str(x) for x in args3)
		forkExec(args3,"hc_brute", mem, "./output/hc/brute/mem/lm_"+trial[0]+".dat")

''' 
	helpers
'''

def forkExec(args, ptype, mem, outputFile):
		if mem:
			subprocess.call(["/usr/local/bin/mprof", "run", "-M", "-C", "-o",outputFile, "python3","run.py", ptype, args])
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
