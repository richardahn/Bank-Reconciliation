import xlwings as xw
import pandas as pd

class Ledger:
	book = None
	sheet = None
	ledger = None # Pandas DataFrame
	name = None # Name of the Ledger

	# TODO: Add a custom index column(invisible to user). This allows us to cross-reference from pivot table back to the original table

	def readLedger(self, *file, index=None):
		"""
		Constructor Helper Function for Ledger
		"""

		if index is None:
			index = 'A1' # TODO: How do I do an automatic table corner detector for displaced tables?

		# Get ledger
		file=file[1] # In order to not get the self object and get the file object
		book = xw.Book(file[0])
		sheet = book.sheets[file[1]]
		table = sheet.range(index).expand().options(pd.DataFrame, index=False).value # index must be false to allow the index column to be recognized as a column

		self.book = book
		self.sheet = sheet
		self.ledger = table
		self.name = sheet.name


	def __init__(self, file=None, ledger=None, name=None):
		# if cfg is None:
			# Return an error

		if file is not None:
			# Read the file and make a ledger
			self.readLedger(self, file, index=None)

		elif ledger is not None:
			# Take in ledger
			self.ledger = ledger

		# If a name is specified, it takes priority
		if name is not None:
			self.name = name
