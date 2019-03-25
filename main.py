

import subprocess
import os
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

	testWords = ["qwerty", "1234"]
	print(testWords)

	sample_wordList()

	# out = subprocess.check_output(["openssl", "passwd", "-1", "test"])
	# print(out)

	
def sample_wordList():
	print("sampling wordlist")
	filename = "./input/100_000.txt"
	file = open(filename, "r", encoding="ISO-8859-1")

	print(file.readline())
	
	lines = file.read().splitlines()

	gen_hashes_sample(lines)


def gen_hashes_sample(words):

	mkdir("./hashes")

	md5 = open("./hashes/1000_a_md5.txt", "w")
	sha = open("./hashes/1000_a_sha256.txt", "w")

	i = 0
	for word in words:
		i += 1
		if i > 1000:
			break
		
		md5_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-1", word])
		sha_hash = subprocess.check_output(["openssl", "passwd", "-salt", "\"\"", "-5", word])

		md5.write((str(md5_hash))[2:-3] + "\r\n")
		sha.write((str(sha_hash))[2:-3] + "\r\n")

	md5.close()
	sha.close()

def gen_hashes(testWords):

	md5crypt = "./hashes/md5"
	mkdir(md5crypt)

	sha256 = "./hashes/sha256"
	mkdir(sha256)

	print("generating hashes for word list")
	for word in testWords:
		f = open(md5crypt + "/" +word+".txt", "w")
		subprocess.call(["openssl", "passwd", "-1", word], stdout=f)

		g = open(sha256 + "/" +word+".txt", "w")
		subprocess.call(["openssl", "passwd", "-5", word], stdout=g)

def run_jtr(passwordFile, hash):
	print("running john the ripper")

	mkdir("output")
	f = open("output/john.txt", "w")

	subprocess.run()

def mkdir(fpath):
	if not os.path.exists(fpath):
		os.makedirs(fpath)

main()