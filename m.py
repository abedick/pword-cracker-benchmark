

import subprocess
import os

def main():

	testWords = ["qwerty", "1234"]
	print(testWords)

	sample_wordList()
	
def sample_wordList():
	print("sampling wordlist")
	filename = "./100_000.txt"
	file = open(filename, "r", encoding="ISO-8859-1")

	print(file.readline())
	
	lines = file.read().splitlines()
	print(lines[500])	


def gen_hashes(testWords):

	md5crypt = "./hashes/md5"
	if not os.path.exists(md5crypt):
		os.makedirs(md5crypt)

	sha256 = "./hashes/sha256"
	if not os.path.exists(sha256):
		os.makedirs(sha256)

	print("generating hashes for word list")
	for word in testWords:
		f = open(md5crypt + "/" +word+".txt", "w")
		subprocess.call(["openssl", "passwd", "-1", word], stdout=f)

		g = open(sha256 + "/" +word+".txt", "w")
		subprocess.call(["openssl", "passwd", "-5", word], stdout=g)

main()