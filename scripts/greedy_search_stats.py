import statistics
from utils import *
from copy import deepcopy as copy
from stats_calculator import StatsCalculator

class GreedySearchStatsCalculator( StatsCalculator ) :
	labels = {
		'random' : 'Random' ,
		'unweighted' : 'DFS-based' ,
		'weighted' : 'FAS-based'
	}
	colors = {
		'random' : 'blue' ,
		'unweighted' : 'green' ,
		'weighted' : 'red'
	}

	def set_plot_bounds( self ) :
		if self.data[ 'timeout' ] :
			self.x_min = 1
			self.x_max = 1
			self.y_min = 0
			self.y_max = 0
		else :
			self.x_min = 1
			self.x_max = self.data[ 'max_iterations' ]
			self.y_min = min( self.data[ 'avg_scores' ] )
			self.y_max = max( self.data[ 'avg_scores' ] )

	def get_plot_bounds( self ) :
		return ( self.x_min , self.x_max , self.y_min , self.y_max )

	def set_plot_values( self , fpath ) :
		algorithm = alg_type( fpath )
		self.label = GreedySearchStatsCalculator.labels[ algorithm ]
		self.color = GreedySearchStatsCalculator.colors[ algorithm ]
		self.algorithm = 'greedy_search'

	def calculate_stats( self ) :
		data = self.data
		if data[ 'timeout' ] : return
		data[ 'num_solutions' ] = len( data[ 'solutions' ] )

		init_sc = [ s[ 'score' ][ 0 ] for s in data[ 'solutions' ] ]
		data[ 'avg_init_score' ] = statistics.mean( init_sc )
		data[ 'std_init_score' ] = statistics.stdev( init_sc )

		best_sc = [ s[ 'score' ][ -1 ] for s in data[ 'solutions' ] ]
		data[ 'avg_best_score' ] = statistics.mean( best_sc )
		data[ 'std_best_score' ] = statistics.stdev( best_sc )

		data[ 'best_score' ] = max( best_sc )
		num_sols = sum( [ 1 for s in data[ 'solutions' ] if compare( s[ 'score' ][ -1 ] , data[ 'best_score' ] ) ] )
		data[ 'percentage_best' ] = float( num_sols ) / data[ 'num_solutions' ] * 100.0

		all_it = [ s[ 'iterations' ] for s in data[ 'solutions' ] ]
		data[ 'max_iterations' ] = max( all_it )
		data[ 'avg_iterations' ] = statistics.mean( all_it )
		data[ 'std_iterations' ] = statistics.stdev( all_it )

		all_times = [ s[ 'time' ] for s in data[ 'solutions' ] ]
		data[ 'max_time' ] = max( all_times )
		data[ 'avg_time' ] = statistics.mean( all_times )
		data[ 'std_time' ] = statistics.stdev( all_times )
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
		data[ 'avg_scores' ] = avg_scores
		data.pop( 'solutions' , None )
		self.data = copy( data )

	def print_stats( self ) :
		data = self.data
		print " ====== %s ====== " % data[ 'name' ].upper()
		if data[ 'timeout' ] :
			print "No stats because of TLE (Time Limit Exceeded)"
		else :
			print "TOTAL NUM SOLUTIONS = %s" % data[ 'num_solutions' ]
			print "BEST SCORE = %s +/- %s (%s)" % ( data[ 'avg_best_score' ] , data[ 'std_best_score' ] , data[ 'best_score' ] )
			print "INIT SCORE = %s +/- %s" % ( data[ 'avg_init_score' ] , data[ 'std_init_score' ] )
			print "NUM ITERATIONS = %s +/- %s (%s)" % ( data[ 'avg_iterations' ] , data[ 'std_iterations' ] , data[ 'max_iterations' ] )
			print "CPU TIME = %s +/- %s (%s)" % ( data[ 'avg_time' ] , data[ 'std_time' ] , data[ 'max_time' ] )

	def read_content( self , filepath ) :
		data = { 'name' : basename( filepath ) , 'solutions' : [] }
		sol = { 'score' : [] , 'iterations' : 0 , 'time' : 0 }
		try :
			with open( filepath , 'r' ) as f :
				solution = None
				for line in f :
					if line.startswith( ' ===' ) :
						if solution : data[ 'solutions' ].append( copy( solution ) )
						solution = copy( sol )
					elif line.startswith( 'SCORE' ) :
						score = float( line.split( ' = ' )[ 1 ] )
						solution[ 'score' ].append( score )
					elif line.startswith( 'NUM ITERATIONS' ) :
						iterations = int( line.split( ' = ' )[ 1 ] )
						solution[ 'iterations' ] = iterations
					elif line.startswith( 'TIME' ) :
						time = float( line.split( ' = ' )[ -1 ] )
						solution[ 'time' ] = time
					elif line.startswith( 'BEST' ) :
						break
				data[ 'solutions' ].append( copy( solution ) )
			data[ 'timeout' ] = False
		except :
			data[ 'timeout' ] = True
		self.data = copy( data )

if __name__ == "__main__":
	sc = GreedySearchStatsCalculator( '../results/heart_random.txt' )
	sc.print_stats()
