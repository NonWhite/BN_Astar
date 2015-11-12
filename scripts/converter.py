import os
import signal
import time
from subprocess import Popen

DATASET_FILE = 'sets.txt'
DATA_DIR = '../data/'

def convertPss( pssFile ) :
	print "PROCESSING DATASET %s" % pssFile
	child = None
	bicscores = {}
	with open( pssFile , 'r' ) as f :
		for line in f :
			line = line[ :-1 ]
			if line.startswith( 'META' ) : continue
			if len( line ) == 0 : continue
			if line.startswith( 'VAR' ) :
				child = line.split()[ 1 ]
				bicscores[ child ] = []
				#print child
			else :
				sp = line.split()
				score , parents = sp[ 0 ] , sp[ 1: ]
				bicscores[ child ].append( ( score , parents ) )
				#print score , parents
	
	outfile = pssFile.replace( '.pss' , '_scores.txt' )
	with open( outfile , 'w' ) as f :
		for field in bicscores :
			tmp = sorted( bicscores[ field ] )
			for ( sc , p ) in tmp :
				f.write( "%s %s %s\n" % ( field , parse( p ) , sc ) )

def parse( arr ) :
	if not arr : return '_'
	return ','.join( arr )

if __name__ == "__main__" :
	with open( DATASET_FILE , 'r' ) as f :
		for line in f :
			if line.find( '..' ) < 0 : continue
			line = line.replace( 'csv' , 'pss' )
			convertPss( line[ :-1 ] )
