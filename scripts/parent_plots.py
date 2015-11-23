import os
import sys
import statistics
import numpy as np
from math import *
from utils import *
from pylab import *
from os.path import *
from copy import deepcopy as copy

def read_content( fpath ) :
	conf_lines = 7
	data = { 'labels' : [] , 'layers' : [ [] , [] , [] ] }
	with open( fpath , 'r' ) as f :
		lines = [ l[ :-1 ] for l in f.readlines() ]
		for idx in xrange( 0 , len( lines ) , conf_lines ) :
			name , n , d , total , limited , pruned = lines[ idx : idx+conf_lines-1 ]
			data[ 'labels' ].append( "%s" % ( name.lower() ) )
			data[ 'layers' ][ 0 ].append( int( total ) )
			data[ 'layers' ][ 1 ].append( int( limited ) )
			data[ 'layers' ][ 2 ].append( int( pruned ) )
			p1 = float( limited ) / float( total ) * 100
			p2 = float( pruned ) / float( total ) * 100
			print "%s & %s & %s & %s (%.2f) & %s (%.5f) \\\\ \\hline" % ( name.capitalize() , d , total , limited , p1 , pruned , p2 )
	return data

def makePlot( fpath ) :
	data = read_content( fpath )
	colors = [ 'red' , 'yellow' , 'green' ]

	bar_width = 0.2
	opacity = 0.4
	error_config = { 'ecolor': '0.3' }
	num_groups = len( data[ 'labels' ] )
	num_data = len( data[ 'layers' ] )

	index= np.arange( 0.0 , ( num_data + 1 ) * bar_width * num_groups - bar_width , ( num_data + 1 ) * bar_width )
	cont = 0
	for layer in data[ 'layers' ] :
		bar( index + cont * bar_width , layer , bar_width , alpha = opacity , color = colors[ cont ] )
		cont += 1
	
	xlabel( 'Datasets' )
	ylabel( 'Number of scores' )
	xticks( index + bar_width , tuple( data[ 'labels' ] ) )

	tight_layout()

	savefig( "%s%s" % ( IMAGES_DIR , 'num_scores' ) )
	#show()
	clf()

if __name__ == "__main__" :
	num_files = 1
	for k in xrange( num_files ) :
		fpath = '../results/num_scores_%s.txt' % ( k + 1 )
		makePlot( fpath )
