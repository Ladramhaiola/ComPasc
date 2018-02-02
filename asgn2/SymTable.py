class SymTable (object):
	def __init__(self):
		self._symbols = OrderedDict();

	def define(self, symbol):
		print('Define: %s' % symbol)
		self._symbols[symbol.name] = symbol

	def lookup(self, name):
		print('Lookup: %s' % name)
		symbol = self._symbols.get(name)
		return symbol