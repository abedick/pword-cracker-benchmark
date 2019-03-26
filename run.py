import sys
import os
import subprocess

def main():
    if len(sys.argv) != 3:
        print("error; not enough or too many args")
        return

    args = sys.argv[2].split(',')
    if len(args) == 6:
        if sys.argv[1] == "john_dict":
            run_john_dict(args[0],args[1],args[2],args[3], args[4], args[5])
            return
        elif sys.argv[1] == "hc_dict":
            run_hc_dict(args[0],args[1],args[2],args[3], args[4], args[5])
            return

    elif len(args) == 5: 
        if sys.argv[1] == "john_brute":
            run_john_brute(args[0],args[1],args[2],args[3], args[4])
            return
        elif sys.argv[1] == "hc_brute":
            run_hc_brute(args[0],args[1],args[2],args[3], args[4])
            return

    print("error; wrong number of args")

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

def run_hc_dict(dic, hashFile, format, fname, x, y):
	print("("+x+"/"+y+") hashcat " + format + " " + fname)

	path = "output/hc/dict/"
	mkdir(path)
	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	# hashcat -a 0 -m 500 ./hashes/100_000_md5.txt ./lists/rockyou.txt
	subprocess.call(["hashcat", "--opencl-device-types", "1", "-a", "0", "-m", format, hashFile, dic, "--force"],stdout=f, stderr=g)

	# Remove the pot and session
	subprocess.call(["rm", "/root/.hashcat/hashcat.potfile"])
	subprocess.call(["rm", "-rf", "/root/.hashcat/sessions"])

def run_hc_brute(format, hashFile, fname, x, y):
	print("("+x+"/"+y+") hashcat " + format + " " + fname)

	path = "output/hc/brute/"
	mkdir(path)
	f = open(path+fname+"_out.txt", "w")
	g = open(path+fname+"_err.txt", "w")

	# hashcat -a 3 -m 500 l?l?l?l?
	subprocess.call(["hashcat", "--opencl-device-types", "1", "-a", "3", "-m", format, hashFile, "?l?l?l?l?l", "--force"],stdout=f, stderr=g)

	# Remove the pot and session
	subprocess.call(["rm", "/root/.hashcat/hashcat.potfile"])
	subprocess.call(["rm", "-rf", "/root/.hashcat/sessions"])

# makes fpath dir is not exist
def mkdir(fpath):
	if not os.path.exists(fpath):
		os.makedirs(fpath)

main()
