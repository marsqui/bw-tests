#!/usr/bin/python
import os
import sys
import time
import getopt
import signal


def main(argv):
	#default values
	bandwidth = 1 # 1 MB/s
	file = "/tmp/file"
	try:
	    opts, args = getopt.getopt(argv,"hgf:b:",["file=","bandwidth="])
	except getopt.GetoptError:
		printhelp()
		sys.exit(2)

	for opt, arg in opts:

		if opt == '-h':
			printhelp()
			sys.exit()
		elif opt in ("-f", "--file"):
			file = arg
		elif opt in ("-g", "--generate"):
			print "Generating 1GB file in "+file+"..."
			generate_file(file)
		elif opt in ("-b", "--bandwidth"):
			bandwidth = arg

	print "Reading from disk file "+file+" in loop with BW=" + str(bandwidth) + "MB/s"
	dropcaches()
	read_in_chunks(file, bandwidth)

def printhelp():
	print 'USAGE: sudo ./interferences.py -f <file> -b <bandwidth> -g'
	print "------- if file not specified, /tmp/file will be used."
	print '------- -g will generate a 1GB file in <file> location.'

def dropcaches():
	os.system("sync && echo 3 > /proc/sys/vm/drop_caches")

def generate_file(file):
	command = "dd if=/dev/urandom of="+file+" bs=1M count=1000"
	os.system(command)

def read_in_chunks(file_object,bandwidth):
	bandwidth_bytes = float(bandwidth)*1024*1024 #bw in bytes
  	chunk_size = 256*1024 #256k in bytes
	sleep_time = chunk_size/bandwidth_bytes
	f = open(file_object,'rb')
	while True:
		data = f.read(chunk_size)
		time.sleep(sleep_time)
		if not data:
			f.seek(0,0)
			dropcaches()

if __name__ == "__main__":
	main(sys.argv[1:])
