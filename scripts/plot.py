import os
import statistics
import numpy as np
from pylab import *
from os.path import *
from copy import deepcopy as copy

color = [ 'b' , 'r' , 'g' ]
datasets = [ 'census' , 'voting' , 'letter' , 'hepatitis' , 'image' , 'heart' , 'mushroom' , 'parkinsons' , 'autos' , 'flag' ]
types = [ 'random' , 'unweighted' , 'weighted' ]
labeltype = [ 'Random' , 'DFS-based' , 'FAS-based' ]
SOL_DELIMITER = ' =='
IMAGES_DIR = '../doc/images/'

def read_content( fpath , name ) :
	data = { 'name' : name , 'solutions' : [] }
	sol = { 'score' : [] , 'iterations' : 0 , 'time' : 0 }
	print fpath
	with open( fpath , 'r' ) as f :
		lines = [ l[ :-1 ] for l in f.readlines() ]
		idx = 0
		while idx < len( lines ) :
			if lines[ idx ].startswith( SOL_DELIMITER ) :
				solution = copy( sol )
				while True :
					line = lines[ idx ]
					if line.startswith( 'SCORE' ) :
						score = float( line.split( ' = ' )[ -1 ] )
						solution[ 'score' ].append( score )
					elif line.startswith( 'NUM IT' ) :
						iterations = int( line.split( ' = ' )[ -1 ] )
						solution[ 'iterations' ] = iterations
					elif line.startswith( 'TIME' ) :
						time = float( line.split( ' = ' )[ -1 ] )
						solution[ 'time' ] = time
					idx += 1
					if idx >= len( lines ) or \
						lines[ idx ].startswith( SOL_DELIMITER ) or \
						lines[ idx ].startswith( 'BEST' ) :
						break
				data[ 'solutions' ].append( solution )
			if idx >= len( lines ) or lines[ idx ].startswith( 'BEST' ) : break
	init_sc = [ s[ 'score' ][ 0 ] for s in data[ 'solutions' ] ]
	avg_init_sc = statistics.mean( init_sc )
	std_init_sc = statistics.stdev( init_sc )
	best_sc = [ s[ 'score' ][ -1 ] for s in data[ 'solutions' ] ]
	avg_best_sc = statistics.mean( best_sc )
	std_best_sc = statistics.stdev( best_sc )
	max_sc = max( best_sc )
	num_sols = sum( [ 1 for s in data[ 'solutions' ] if s[ 'score' ][ -1 ] == max_sc ] )
	total_sols = len( data[ 'solutions' ] )
	perc_sols = float( num_sols ) / total_sols * 100.0
	all_it = [ s[ 'iterations' ] for s in data[ 'solutions' ] ]
	max_iterations = max( all_it )
	avg_iterations = statistics.mean( all_it )
	stdev_iterations = statistics.stdev( all_it )
	all_times = [ s[ 'time' ] for s in data[ 'solutions' ] ]
	max_time = max( all_times )
	avg_time = statistics.mean( all_times )
	stdev_time = statistics.stdev( all_times )
	print " ====== %s ====== " % name.upper()
	print "TOTAL NUM SOLUTIONS = %s" % total_sols
	print "NUM OF SOLUTIONS WITH MAX SCORE = %s" % num_sols
	print "BEST SCORE = %s +/- %s (%s)" % ( avg_best_sc , std_best_sc , max_sc )
	print "PERCENTAGE WITH MAX SCORE = %s" % perc_sols
	print "INIT SCORE = %s +/- %s" % ( avg_init_sc , std_init_sc )
	print "NUM ITERATIONS = %s +/- %s (%s)" % ( avg_iterations , stdev_iterations , max_iterations )
	print "CPU TIME = %s +/- %s (%s)" % ( avg_time , stdev_time , max_time )
	#print "%.3f & %.3f $\pm$ %.2f & %.3f $\pm$ %.2f & %.2f & %.2f $\pm$ %.2f" % ( max_sc , avg_init_sc , std_init_sc , avg_best_sc , std_best_sc , perc_sols , avg_iterations , stdev_iterations )
	max_length = max( [ len( s[ 'score' ] ) for s in data[ 'solutions' ] ] )
	avg_scores = []
	for i in xrange( max_length ) :
		sc = 0.0
		q = 0
		for sol in data[ 'solutions' ] :
			if len( sol[ 'score' ] ) <= i : continue
			q += 1
			sc += sol[ 'score' ][ i ]
		avg_scores.append( sc / q )
	data[ 'score' ] = avg_scores
	data[ 'iterations' ] = len( avg_scores )
	data[ 'avg_iterations' ] = avg_iterations
	data.pop( 'solutions' )
	return data

def addCurve( x , y , col , lbl ) :
	style = '-'
	plot( x , y , color = col , linestyle = style , label = lbl )

def addPoint( x , y , col ) :
	plot( x , y , col+'o' )

# TODO
def makePlot( directory , dataname ) :
	networkdata = []
	print ' ================================ %s =============================== ' % dataname.upper()
	for i in xrange( len( types ) ) :
		t = types[ i ]
		lbl = labeltype[ i ]
		f = "%s%s_%s.txt" % ( directory , dataname , t )
		if not isfile( f ) : continue
		networkdata.append( read_content( f , lbl ) )
	return 'gg'
	max_iterations = max( [ d[ 'iterations' ] for d in networkdata ] )
	for i in range( len( networkdata ) ) :
		data = networkdata[ i ]
		y = data[ 'score' ]
		x = range( 1 , len( y ) + 1 )
		col = color[ i ]
		addCurve( x , y , col , data[ 'name' ] )
		axvline( x = data[ 'avg_iterations' ] , linestyle = '--' , color = col )
	legend( loc = 'lower right' )
	xlabel( 'Iteration' )
	ylabel( 'BIC Score' )
	savefig( "%s%s" % ( IMAGES_DIR , dataname ) )
	#show()
	clf()
	print ' ====================================================== '

if __name__ == "__main__":
	directory = '../results/'
	for d in datasets :
		makePlot( directory , d )
