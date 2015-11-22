import os.path
from utils import *
from copy import deepcopy as copy
from stats_calculator import StatsCalculator

class AStarStatsCalculator( StatsCalculator ) :
	labels = {
		'simple' : 'Simple' ,
		'dynamic_k2' : 'Dynamic (K=2)' ,
		'dynamic_k3' : 'Dynamic (K=3)' ,
		'dynamic_k4' : 'Dynamic (K=4)' ,
		'static_d2' : 'Static (D=2)' ,
		'static_d3' : 'Static (D=3)'
	}
	colors = {
		'simple' : 'blue' ,
		'dynamic_k2' : 'green' ,
		'dynamic_k3' : 'red' ,
		'dynamic_k4' : 'cyan' ,
		'static_d2' : 'yellow' ,
		'static_d3' : 'magenta'
	}

	def set_plot_bounds( self ) :
		if self.data[ 'timeout' ] :
			self.x_min = 1
			self.x_max = 1
			self.y_min = 0
			self.y_max = 0
		else :
			self.x_min = 1
			self.x_max = 1
			self.y_min = self.data[ 'score' ]
			self.y_max = self.data[ 'score' ]
	def get_plot_bounds( self ) :
		return ( self.x_min , self.x_max , self.y_min , self.y_max )

	def set_plot_values( self , fpath ) :
		algorithm = alg_type( fpath )
		self.label = AStarStatsCalculator.labels[ algorithm ]
		self.color = AStarStatsCalculator.colors[ algorithm ]
		self.algorithm = 'a_star'

	def calculate_stats( self ) :
		self.data[ 'timeout' ] = len( self.data ) < 2

	def print_stats( self ) :
		print " ====== %s ====== " % self.data[ 'name' ].upper()
		if self.data[ 'timeout' ] :
			print "No stats because of TLE (Time Limit Exceeded)"
		else :
			print "SCORE = %.6f" % self.data[ 'score' ]
			print "CPU TIME = %.2f" % self.data[ 'time' ]
			print "EXPANDED NODES = %d" % self.data[ 'expanded_nodes' ]
			print "GENERATED NODES = %d" % self.data[ 'generated_nodes' ]
	
	def read_content( self , filepath ) :
		data = { 'name' : basename( filepath ) }
		with open( filepath , 'r' ) as f :
			for line in f :
				if line.startswith( 'ORDER' ) :
					continue
				elif line.startswith( 'SCORE' ) :
					data[ 'score' ] = -float( line.split( ' = ' )[ 1 ] )
				elif line.startswith( 'TIME =' ) :
					data[ 'time' ] = float( line.split( ' = ' )[ 1 ] )
				elif line.startswith( 'EXPANDED' ) :
					data[ 'expanded_nodes' ] = int( line.split( ' = ' )[ 1 ] )
				elif line.startswith( 'GENERATED' ) :
					data[ 'generated_nodes' ] = int( line.split( ' = ' )[ 1 ] )
				elif line.startswith( 'BEST' ) :
					break
		self.data = copy( data )

if __name__ == '__main__' :
	sc = AStarStatsCalculator( '../results/heart_simple.txt' )
	sc.print_stats()
