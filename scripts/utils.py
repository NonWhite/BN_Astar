import sys
import os.path as op

''' DIRECTORY CONSTANTS '''
IMAGES_DIR = '../slides/images/'
RESULTS_DIR = '../results/'

''' NUMERIC CONSTANTS '''
EPS = sys.float_info.epsilon

''' GENERAL VARIABLES '''
datasets = [ 'census' , 'voting' , 'letter' , 'hepatitis' , 'image' , 'heart' , 'mushroom' , 'parkinsons' , 'autos' , 'flag' ]
GREEDY_ALGS = [ 'random' , 'unweighted' , 'weighted' ]
ASTAR_ALGS = [ 'simple' , 'dynamic_k2' , 'dynamic_k3' , 'dynamic_k4' , 'static_d2' , 'static_d3' ]
types = GREEDY_ALGS + ASTAR_ALGS

def basename( filepath ) :
	return op.splitext( op.basename( filepath ) )[ 0 ]

def alg_type( filepath ) :
	f = basename( filepath )
	return f[ f.find( '_' )+1: ]

def compare( f1 , f2 ) :
	if f1 + EPS < f2 : return -1
	if f1 - EPS > f2 : return 1
	return 0
