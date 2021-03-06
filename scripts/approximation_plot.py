import os
import sys
import statistics
import numpy as np
from math import *
from utils import *
from pylab import *
from os.path import *
from copy import deepcopy as copy

algs = [ 'static_d2' , 'static_d3' , 'random' , 'DFS-based' , 'FAS-based' ]
colors = [ 'red' , 'yellow' , 'green' , 'purple' , 'black' , 'blue' ]

def read_content( fpath ) :
	conf_lines = 7
	data = { 'labels' : [] , 'layers' : [ [] , [] , [] , [] , [] ] }
	get_t = lambda x : float( x ) if x.find( 'T' ) < 0 else 0
	with open( fpath , 'r' ) as f :
		lines = [ l[ :-1 ] for l in f.readlines() ]
		for idx in xrange( 0 , len( lines ) , conf_lines ) :
			name = lines[ idx ]
			times = lines[ idx+1 : idx+conf_lines-1 ]
			data[ 'labels' ].append( "%s" % name.lower() )
			for k in xrange( len( times ) ) :
				data[ 'layers' ][ k ].append( get_t( times[ k ] ) )
			print "%s & %s & %s & %s & %s & %s \\\\ \\hline" % ( name.capitalize() , get_t( times[ 0 ] ) , get_t( times[ 1 ] ) , get_t( times[ 2 ] ) , get_t( times[ 3 ] ) , get_t( times[ 4 ] ) )
	return data

def makePlot( fpath ) :
	data = read_content( fpath )
	return 'gg'

	bar_width = 0.2
	opacity = 0.4
	error_config = { 'ecolor': '0.3' }
	num_groups = len( data[ 'labels' ] )
	num_data = len( data[ 'layers' ] )

	index= np.arange( 0.0 , ( num_data + 1 ) * bar_width * num_groups - bar_width , ( num_data + 1 ) * bar_width )
	cont = 0
	for layer in data[ 'layers' ] :
		bar( index + cont * bar_width , layer , bar_width , alpha = opacity , color = colors[ cont ] , label = algs[ cont ] )
		cont += 1
	
	xlabel( 'Datasets' )
	ylabel( 'Time (seconds)' )
	xticks( index + bar_width , tuple( data[ 'labels' ] ) )

	legend( loc = 'upper left' )

	tight_layout()

	savefig( "%s%s" % ( IMAGES_DIR , 'approx_astar' ) )
	#show()
	clf()

if __name__ == "__main__" :
	fpath = '../results/approx_astar.txt'
	makePlot( fpath )
