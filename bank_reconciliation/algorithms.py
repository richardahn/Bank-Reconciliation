import xlwings as xw
import utils as ut
import pandas as pd
import numpy as np
from ledger import Ledger

# TODO: Should rename this file to reconciliation.py

# TODO: Incomplete
def dateElimination(): 
	return -1

# TODO: Incomplete
def consecutiveMatch(): # have a limit for how far you go(10?)
	return -1

def isDebit(val):
	return val <= 0

def isCredit(val):
	return val >= 0

def appendMatchColumn(ledger):
	"""
	Adds an extra column to ledger labeled Matches that tells you if the row has been matched or not(0 = no match, 1 = match).
	If you have an existing Matches column, this will overwrite it with 0's

	Args:
		ledger: a Ledger object 
	Returns:
		Nothing - the insertion is done in place.
	Raises:
		Nothing
	"""
	length = len(ledger.ledger[ledger.ledger.columns[0]])
	ledger.ledger = ledger.ledger.assign(Matches=pd.Series(np.zeros(length)).values)
	return 

def isEmpty(val):
	"""
	Returns true if the number is 0 or NaN

	Args:
		val: a number
	Returns:
		A boolean
	Raises:
		Nothing
	"""
	return val == 0 or np.isnan(val)

def oneToOneMatch(book, bank, bookCol, bankCol):
	"""
	Matches two Ledger objects based on the value within the specified columns. 
	It matches with the one-to-one algorithm O(m * n) where m and n are the # of items in book and bank respectively

	Args:
		book: a ledger
		bank: a ledger
		bookCol: the column that you want to match in book
		bankCol: the column that you want to match in bank
	Returns:
		Nothing - the algorithm functions in place
	Raises:
		Nothing
	"""
	# Output table that shows matches
	ut.sortByDate(bank)

	print(bank.ledger[bankCol])
	for bookIndex in book.ledger.index.values: # Note: i can also retrieve the key value if necessary
		bookMatch = book.ledger.at[bookIndex, 'Matches']
		bookValue = book.ledger.at[bookIndex, bookCol]
		bookIsEmpty = isEmpty(bookValue)
		if (not bookMatch) and (not bookIsEmpty):
			for bankIndex in bank.ledger.index.values:
				bankMatch = bank.ledger.at[bankIndex, 'Matches']
				bankValue = bank.ledger.at[bankIndex, bankCol]
				bankIsEmpty = isEmpty(bankValue)
				if (not bankMatch) and (not bankIsEmpty):
					# Check if matching
					if abs(bookValue) == abs(bankValue):
						# Assign it as matching
						book.ledger.at[bookIndex, 'Matches'] = 1
						bank.ledger.at[bankIndex, 'Matches'] = 1
						break
	return 

def highlightMatches(ledger): # Use the extra highlight column to figure out what was reconciled
	"""
	Highlights the corresponding excel file of the Ledger based on whether it found a match or not.

	Args:
		ledger: a Ledger object
	Returns:
		Nothing - the changes are shown in the excel file
	Raises:
		Nothing
	"""
	lightYellow = (255, 255, 224)
	for index in ledger.ledger.index.values:
		index = int(index) # To make it compatible with xlwings, it must be converted from float to int
		match = ledger.ledger.at[index, 'Matches']
		if match:
			# Highlight row
			begInd = ((index+2), 1)
			endInd = ((index+2), len(ledger.ledger.columns.values))
			ledger.sheet.range(begInd, endInd).color = lightYellow
	return


def reversePivotMapping(book, bookByBank, vendorPivotTable, customerPivotTable):
	"""
	Maps matched values from the pivot table to its corresponding un-pivoted Ledger

	Args:
		book: the un-pivoted Ledger of pivotTable
		bookByBank: is necessary to identify book entries belonging to a specific bank
		vendorPivotTable: a pivoted Ledger object for vendors
		customerPivotTable: a pivoted Ledger object for customers
	Returns:
		Nothing - the changes are reflected in book
	Raises:
		Nothing
	"""
	appendMatchColumn(book)
	# The pivots share the same indices
	indexValues = vendorPivotTable.ledger.index.values
	for pivotIndex in indexValues:
		vendorAmount = vendorPivotTable.ledger.at[pivotIndex, ut.clean_string('Vendor')]
		customerAmount = customerPivotTable.ledger.at[pivotIndex, ut.clean_string('Customer')]
		date = vendorPivotTable.ledger.at[pivotIndex, ut.clean_string('Posting Date')]
		rows = bookByBank.ledger[bookByBank.ledger[ut.clean_string('Posting Date')].isin([date])]
		# Get the sum of all debits, check if it matches
		amounts = rows[ut.clean_string('Amount')]
		debits = amounts[isDebit(amounts)]
		credits = amounts[isCredit(amounts)]
		if vendorAmount == debits.sum():
			for i in debits.index.values:
				book.ledger.at[i, 'Matches'] = 1
		if customerAmount == credits.sum():
			for i in credits.index.values:
				book.ledger.at[i, 'Matches'] = 1
	return

def reconcile(book, bank, externalData):
	"""
	Reconciles a book statement with a bank statement, supported by extra external data.

	Args:
		book: a Ledger object 
		bank: a Ledger object
		externalData: extra data such as previous bank reconciliations
	Returns:
		Nothing 
	Raises:
		Nothing
	"""
	# Algorithm 1: One-to-one reconciliation
	ut.clean_columns(book.ledger)
	bankColumn = ut.clean_string('G/L Account Name') # Filter by bank
	bookByBank = Ledger(ledger=book.ledger.query('{} == "{}"'.format(bankColumn, bank.name)))
	pivotTable = Ledger(ledger=ut.toPivotTable(bookByBank.ledger))
	vendorPivotTable = Ledger(ledger=pivotTable.ledger.drop('Customer', axis=1).copy())
	customerPivotTable = Ledger(ledger=pivotTable.ledger.drop('Vendor', axis=1).copy())
	appendMatchColumn(vendorPivotTable)
	appendMatchColumn(customerPivotTable)
	appendMatchColumn(bank)
	oneToOneMatch(vendorPivotTable, bank, ut.clean_string('Vendor'), ut.clean_string('Debit'))
	oneToOneMatch(customerPivotTable, bank, ut.clean_string('Customer'), ut.clean_string('Credit'))

	# After getting all pivot table matches, map it back up to the Book Ledger
	reversePivotMapping(book, bookByBank, vendorPivotTable, customerPivotTable)

	# Reflect changes in excel
	highlightMatches(book)
	highlightMatches(bank)
	ut.newExcel(vendorPivotTable, 'VendorByDate.xlsx', 'Reconciliation')
	ut.newExcel(customerPivotTable, 'CustomerByDate.xlsx', 'Reconciliation')
	highlightMatches(vendorPivotTable)
	highlightMatches(customerPivotTable)
	return

def bankReconciliation(books, banks, externalData):
	"""
	Reconciles multiple banks all at once
	"""
	reconcile(books[0], banks[0], externalData)
	return



'''
First, reconcile with the previous bank reconciliation. Add the deposits in transit(maybe do a partial)
a) 1-to-1 matching with Bank Reconciliation values



Entry Reduction - Elimination of entries. Once we find a match or a partial match, we reduce it to 0 or get rid of it, and then highlight the cell to indicate a match
Bank Types
a) Vendor Accounts Payable - even if you don't know anything about these, you can still analyse the vendor column of your book ledger, and do 1-to-1 match with each bank entry.
b) Then do Receivables, but use consecutive numbers(must be done after vendor AP so you can get rid of entries)


Matching Types
1) Description Pattern identification(possible date?) - Put it as a partial match
	i) Once you have a partial match, you can do one-to-one matching, with the net value

2) One-to-one matching: O(n*m), n = book, m = bank
	i) More specifically, group by date first for both books and banks, then do the matching


CHEATS?(last resorts)
	- Maybe only look at the cent value
	- Maybe look at description, use word similarity 
	- 

Optional Features:
	Create a weighted system that determines what type of reconciliation strategies this company is more prone to use in order to have better reconciliation


'''