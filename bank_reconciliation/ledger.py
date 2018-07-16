import xlwings as xw
import pandas as pd

class Ledger:
	ledger = None # Pandas DataFrame
	name = None # Name of the Ledger

	# TODO: Add a custom index column(invisible to user). This allows us to cross-reference from pivot table back to the original table

	def readLedger(self, file=None, index=None):
		if index is None:
			index = 'A1' # TODO: How do I do an automatic table corner detector for displaced tables?

		# Get ledger
		book = xw.Book(file[0])
		sheet = book.sheets[file[1]]
		table = sheet.range(index).expand().options(pd.DataFrame).value

		self.ledger = table
		self.name = sheet.name


	def __init__(self, file=None, ledger=None, name=None):
		# if cfg is None:
			# Return an error

		if file is not None:
			# Read the file and make a ledger
			readLedger(self, file=file)

		else if ledger is not None:
			# Take in ledger
			self.ledger = ledger

		# If a name is specified, it takes priority
		if name is not None:
			self.name = name
