import os
import sys
import statistics
import numpy as np
from math import *
from utils import *
from pylab import *
from os.path import *
from copy import deepcopy as copy
from a_star_stats import AStarStatsCalculator
from greedy_search_stats import GreedySearchStatsCalculator

def get_stats_calculator( filepath ) :
	algorithm = alg_type( filepath )
	if algorithm in GREEDY_ALGS : return GreedySearchStatsCalculator( filepath )
	elif algorithm in ASTAR_ALGS : return AStarStatsCalculator( filepath )

def addCurve( x , y , col , lbl ) :
	style = '-'
	plot( x , y , color = col , linestyle = style , label = lbl )

def addPoint( x , y , col ) :
	plot( x , y , col+'o' )

def makePlot( directory , dataname ) :
	networkdata = []
	print ' ================================ %s =============================== ' % dataname.upper()
	for t in types :
		f = "%s%s_%s.txt" % ( directory , dataname , t )
		if not isfile( f ) : continue
		sc = get_stats_calculator( f )
		sc.print_stats()
		networkdata.append( sc )
	max_iterations = max( [ d.data[ 'max_iterations' ] for d in networkdata if 'max_iterations' in d.data ] )
	x_min , x_max , y_min , y_max = ( 1 , 1 , 1e10 , -1e10 )
	for sc in networkdata :
		data = sc.data
		if data[ 'timeout' ] : continue
		if sc.algorithm == 'a_star' :
			axhline( y = data[ 'score' ] , linestyle = '-' , color = sc.color , label = sc.label )
		elif sc.algorithm == 'greedy_search' :
			y = data[ 'avg_scores' ]
			x = range( 1 , len( y ) + 1 )
			addCurve( x , y , sc.color , sc.label )
			axvline( x = data[ 'avg_iterations' ] , linestyle = '--' , color = sc.color )
		bounds = sc.get_plot_bounds()
		diff = pow( 10 , log10( fabs( bounds[ 3 ] ) ) - 4 )
		x_min = min( x_min , bounds[ 0 ] )
		x_max = max( x_max , bounds[ 1 ] )
		y_min = min( y_min , bounds[ 2 ] )
		y_max = max( y_max , bounds[ 3 ] + diff )
		
	legend( loc = 'lower right' )
	xlabel( 'Iteration' )
	ylabel( 'BIC Score' )
	axis( ( x_min , x_max , y_min , y_max ) )
	savefig( "%s%s" % ( IMAGES_DIR , dataname ) )
	#show()
	clf()

if __name__ == "__main__":
	directory = RESULTS_DIR
	if len( sys.argv ) > 1 : datasets = sys.argv[ 1: ]
	for d in datasets :
		makePlot( directory , d )
