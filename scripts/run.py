import os
import signal
import time
from subprocess import Popen

DATASET_FILE = 'sets.txt'
PROGRAM = 'python ../code/astar.py %s %s'
CONF_LINES = 3
TIMEOUT = 10800

def timeout_command( command , timeout ) :
	start = time.time()
	process = Popen( command )
	while process.poll() is None :
		time.sleep( 0.1 )
		now = time.time()
		if now - start > timeout :
			os.kill( process.pid , signal.SIGKILL )
			os.waitpid( -1 , os.WNOHANG )

if __name__ == "__main__" :
	with open( DATASET_FILE , 'r' ) as f :
		lines = [ l[ :-1 ] for l in f.readlines() ]
		for i in xrange( 0 , len( lines ) , CONF_LINES ) :
			dataset , ommit , _ = lines[ i:(i+CONF_LINES) ]
			print "PROCESSING DATASET %s" % dataset
			inst = ( PROGRAM % ( dataset , ommit ) ).split()
			timeout_command( inst , TIMEOUT )
			#call( inst )
