class StatsCalculator :
	def __init__( self , fpath = None ) :
		if fpath :
			self.set_plot_values( fpath )
			self.read_content( fpath )
			self.calculate_stats()
			self.set_plot_bounds()

	def calculate_stats( self ) :
		'''
			Calculate stats and save them in self.data
		'''
		raise NotImplementedError( 'Should have implemented this' )
	
	def print_stats( self ) :
		'''
			Print stats
		'''
		raise NotImplementedError( 'Should have implemented this' )
	
	def read_content( self , filepath ) :
		'''
			Extract data from file and save in self.data
		'''
		raise NotImplementedError( 'Should have implemented this' )
	
	def set_plot_bounds( self ) :
		'''
			Calculate bounds for plotting stats
		'''
		raise NotImplementedError( 'Should have implemented this' )
	
	def get_plot_bounds( self ) :
		'''
			Return bounds for plotting stats
		'''
		raise NotImplementedError( 'Should have implemented this' )
