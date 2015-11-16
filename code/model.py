import sys
from copy import deepcopy as copy
from utils import *
from data import Data
from math import log
from bitarray import bitarray

class Model :
	def __init__( self , dataobj = None , modelfile = None ) :
		if dataobj :
			self.data = dataobj
			self.initialize()
		if modelfile :
			self.loadmodel( modelfile )

	def initialize( self ) :
		self.entropyvalues = dict( [ ( field , {} ) for field in self.data.fields ] )
		self.sizevalues = dict( [ ( field , {} ) for field in self.data.fields ] )
		self.bicvalues = dict( [ ( field , {} ) for field in self.data.fields ] )
		self.bestparents = dict( [ ( field , [] ) for field in self.data.fields ] )
		self.bitsets = dict( [ ( field , {} ) for field in self.data.fields ] )
		self.precalculate_scores()

	def precalculate_scores( self ) :
		score_file = "%s/%s%s" % ( os.path.dirname( self.data.source ) , os.path.splitext( os.path.basename( self.data.source ) )[ 0 ] , '_scores.txt' )
		if os.path.isfile( score_file ) :
			print "Reading from %s all scores" % score_file
			with open( score_file , 'r' ) as f :
				for line in f :
					field , par , sc = line.split()
					if par == '_' : par = ''
					self.bicvalues[ field ][ par ] = float( sc )
					sp = par.split( ',' )
					if sp[ 0 ] == '' : sp = []
					self.bestparents[ field ].append( sp )
			self.create_bitsets()
		else :
			print "Pre-calculating all scores from model"
			self.data.calculatecounters()
			''' MDL_SCORE '''
			MAX_NUM_PARENTS = int( log( 2 * len( self.data.rows ) / log( len( self.data.rows ) ) ) )
			''' BIC SCORE '''
			#MAX_NUM_PARENTS = int( log( len( self.data.rows ) ) )
			files = []
			for field in self.data.fields :
				print "Calculating scores for field %s" % field
				field_file = "%s/%s_%s_%s" % ( os.path.dirname( self.data.source ) , os.path.splitext( os.path.basename( self.data.source ) )[ 0 ] , 'scores' , '%s.txt' % field )
				files.append( field_file )
				if os.path.isfile( field_file ) : continue
				options = copy( self.data.fields )
				options.remove( field )
				for k in xrange( 0 , MAX_NUM_PARENTS ) :
					print "Size = %s" % ( k + 1 )
					subconj = [ list( x ) for x in itertools.combinations( options , k ) ]
					for sub in subconj :
						sc = self.bic_score( field , sub )
						prune = False
						for f in sub :
							par_sub = copy( sub )
							par_sub.remove( f )
							par_sc = self.bic_score( field , par_sub )
							if compare( sc , par_sc ) < 0 :
								prune = True
								break
						if not prune :
							self.bestparents[ field ].append( copy( sub ) )
				tmp = [ ( self.bicvalues[ field ][ self.hashedarray( p ) ] , p ) for p in self.bestparents[ field ] ]
				tmp.sort( reverse = True )
				self.bestparents[ field ] = [ p[ 1 ] for p in tmp ]
				with open( field_file , 'w' ) as f :
					lstparents = self.bestparents[ field ]
					for p in lstparents :
						par = self.hashedarray( copy( p ) )
						hp = copy( par )
						if par == '' : hp = '_'
						f.write( "%s %s %s\n" % ( field , hp , self.bicvalues[ field ][ par ] ) )
				self.bicvalues.pop( field , None )
			self.data.deletecounters()
			merge_files( files , score_file )
			self.create_bitsets()

	def reduce_bicscores( self , field ) :
		print "Reducing score lists for field %s" % field
		tmp = [ ( self.bicvalues[ field ][ p ] , self.decodearray( p ) ) for p in self.bicvalues[ field ] ]
		tmp.sort( reverse = True )
		for i in xrange( len( tmp ) ) :
			( sc , p ) = tmp[ i ]
			prune = False
			if not set( p ).issubset( tmp[ 0 ][ 1 ] ) :
				for j in xrange( i ) :
					( old_sc , old_p ) = tmp[ j ]
					if set( old_p ).issubset( p ) :
						prune = True
						break
			if not prune : self.bestparents[ field ].append( p )
			else : self.bicvalues[ field ].pop( self.hashedarray( p ) , None )

	def create_bitsets( self ) :
		for f1 in self.data.fields :
			for f2 in self.data.fields :
				if f1 == f2 : continue
				lstpar = self.bestparents[ f1 ]
				coinc = ''.join( [ str( int( f2 in s ) ) for s in lstpar ] )
				self.bitsets[ f1 ][ f2 ] = bitarray( coinc )	

	def find_parents( self , field , options ) :
		rem = [ f for f in self.data.fields if ( f not in options ) and f != field ]
		le = len( self.bestparents[ field ] )
		full = bitarray( '1' * le )
		for f in rem :
			aux = copy( self.bitsets[ field ][ f ] )
			aux.invert()
			full &= aux
		pos = full.index( True )
		return self.bestparents[ field ][ pos ]

	def loadmodel( self , modelfile ) :
		self.modelfile = modelfile
		print "Loading model from %s" % modelfile
		fieldset = self.data.fields
		node = { 'parents' : [] , 'childs' : [] }
		self.network = dict( [ ( field , copy( node ) ) for field in fieldset ] )
		with open( modelfile , 'r' ) as f :
			lines = f.readlines()
			for l in lines :
				sp = l[ :-1 ].split( ':' )
				field = sp[ 0 ]
				childs = [ s.strip() for s in sp[ 1 ].split( ',' ) if len( s.strip() ) > 0 ]
				for ch in childs :
					self.network[ field ][ 'childs' ].append( ch )
					self.network[ ch ][ 'parents' ].append( field )
		print "Finding topological order for network"
		self.topological = topological( self.network , fieldset )
		print "Top. Order = %s" % self.topological

	def setnetwork( self , network , topo_order = None , train = True ) :
		self.network = copy( network )
		if not topo_order : self.topological = topological( self.network , self.data.fields )
		else : self.topological = topo_order
		if train : self.trainmodel()

	def trainmodel( self ) :
		#print "Training model..."
		''' START POINTER FUNCTIONS '''
		calc_probs = self.calculateprobabilities
		lstfields = self.data.fields
		''' END POINTER FUNCTIONS '''
		self.probs = dict( [ ( field , {} ) for field in lstfields ] )
		for field in self.data.fields :
			xi = [ field ]
			pa_xi = self.network[ field ][ 'parents' ]
			calc_probs( xi , pa_xi )

	def calculateprobabilities( self , xsetfield , ysetfield ) :
		#print "Calculating P( %s | %s )" % ( xsetfield , ysetfield )
		implies = self.data.evaluate( xsetfield )
		condition = self.data.evaluate( ysetfield )
		for xdict in implies :
			xkey , xval = xdict.keys()[ 0 ] , xdict.values()[ 0 ]
			if xval not in self.probs[ xkey ] : self.probs[ xkey ][ xval ] = {}
			if not condition :
				self.conditional_prob( xdict , {} )
				continue
			for y in condition :
				self.conditional_prob( xdict , y )

	def conditional_prob( self , x , y ) :
		xkey , xval = x.keys()[ 0 ] , x.values()[ 0 ]
		cond = self.data.hashed( y )
		if cond in self.probs[ xkey ][ xval ] : return self.probs[ xkey ][ xval ][ cond ]
		numerator = copy( x )
		for key in y : numerator[ key ] = y[ key ]
		denominator = y
		pnum = self.data.getcount( numerator )
		pden = len( self.data.rows ) if not denominator else self.data.getcount( denominator )
		pnum , pden = ( pnum + self.bdeuprior( numerator ) , pden + self.bdeuprior( denominator ) )
		resp = float( pnum ) / float( pden )
		self.probs[ xkey ][ xval ][ cond ] = resp
		return resp

	def bdeuprior( self , setfields ) :
		prior = 1.0
		fieldtypes = self.data.fieldtypes
		for field in setfields :
			tam = ( len( self.data.stats[ field ] ) if fieldtypes[ field ] == LITERAL_FIELD else 2 )
			prior *= tam
		return ESS / prior

	def score( self ) :
		resp = 0.0
		for field in self.data.fields :
			resp += self.bic_score( field , self.network[ field ][ 'parents' ] )
		self.network[ 'score' ] = resp
		return resp

	def bic_score( self , xsetfield , ysetfield ) :
		field = xsetfield
		cond = self.hashedarray( ysetfield )
		if cond in self.bicvalues[ field ] : return self.bicvalues[ field ][ cond ]
		#print "Calculating BIC( %s | %s )" % ( xsetfield , ysetfield )
		N = len( self.data.rows )
		H = self.entropy( xsetfield , ysetfield )
		S = self.size( xsetfield , ysetfield )
		resp = ( -N * H ) - ( log( N ) / 2.0 * S )
		#print "BIC( %s | %s ) = %s" % ( xsetfield , ysetfield , resp )
		self.bicvalues[ field ][ cond ] = resp
		return resp

	def mdl_score( self , xsetfield , ysetfield ) :
		field = xsetfield
		cond = self.hashedarray( ysetfield )
		if cond in self.bicvalues[ field ] : return self.bicvalues[ field ][ cond ]
		#print "Calculating BIC( %s | %s )" % ( xsetfield , ysetfield )
		N = len( self.data.rows )
		H = self.entropy( xsetfield , ysetfield )
		S = self.size( xsetfield , ysetfield )
		resp = N * H + ( log( N ) / 2.0 * S )
		#print "BIC( %s | %s ) = %s" % ( xsetfield , ysetfield , resp )
		self.bicvalues[ field ][ cond ] = resp
		return resp

	def entropy( self , xsetfield , ysetfield ) :
		field = xsetfield
		cond = self.hashedarray( ysetfield )
		if cond in self.entropyvalues[ field ] : return self.entropyvalues[ field ][ cond ]
		x = self.data.evaluate( [ xsetfield ] )
		y = self.data.evaluate( ysetfield )
		N = len( self.data.rows )
		resp = 0.0
		''' START POINTER FUNCTIONS '''
		getcount = self.data.getcount
		bdeuprior = self.bdeuprior
		''' END POINTER FUNCTIONS '''
		for xdict in x :
			xkey , xval = xdict.keys()[ 0 ] , xdict.values()[ 0 ]
			if not y :
				Nij = getcount( xdict ) + bdeuprior( xdict )
				resp += ( Nij / N ) * log( Nij / N )
				continue
			for ydict in y :
				ij = copy( ydict )
				ijk = copy( ij )
				ijk[ xkey ] = xval
				Nijk = getcount( ijk ) + bdeuprior( ijk )
				Nij = getcount( ij ) + bdeuprior( ij )
				resp += ( Nijk / N * log( Nijk / Nij ) )
		self.entropyvalues[ field ][ cond ] = -resp
		return -resp

	def size( self , xsetfield , ysetfield ) :
		field = xsetfield
		cond = self.hashedarray( ysetfield )
		if cond in self.sizevalues[ field ] : return self.sizevalues[ field ][ cond ]
		resp = len( self.data.evaluate( [ xsetfield ] ) ) - 1
		for field in ysetfield :
			resp *= len( self.data.evaluate( [ field ] ) )
		self.sizevalues[ field ][ cond ] = resp
		return resp

	def hashedarray( self , setfields ) :
		setfields.sort()
		return ','.join( setfields )

	def decodearray( self , st ) :
		par = st.split( ',' )
		if len( par ) == 1 and par[ 0 ] == '' : par = []
		return par

if __name__ == "__main__" :
	if len( sys.argv ) == 4 :
		datasetfile , field , parents = sys.argv[ 1: ]
		data = Data( datasetfile , discretize = False )
		model = Model( dataobj = data )
		par = parents.replace( '_' , '' ).replace( ',' , ' ' ).split()
		sc = model.bic_score( field , par )
		print "%s %s %s" % ( field , parents , sc )
