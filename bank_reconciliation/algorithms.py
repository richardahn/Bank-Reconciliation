import xlwings as xw
import utils as ut

# TODO: Should rename this file to reconciliation.py

def dateElimination(): #
	return -1

# Pass these match functions in

def consecutiveMatch(): # have a limit for how far you go(10?)
	return -1


def oneToOneMatch(book, bank, bookCol):
	# Loop through 
	return -1

def highlight(): # Use the extra highlight column to figure out what was reconciled
	return -1

def reconcile(book, bank, externalData):
	# --------- Pivot Table by Date -------------
	ut.clean_columns(book.ledger)
	bankColumn = ut.clean_string('G/L Account Name') # Filter by bank
	vendors = book.ledger.query('{} == "{}"'.format(bankColumn, bank.name))
	pivotTable = ut.toPivotTable(vendors)

	print(pivotTable)
	oneToOneMatch(pivotTable, bank, 'Vendor')
	print(bank)


	# 1) Attempt to one match w/ previous bank rec
	# 	a) Do a one match with the externalData value


	# 2) Attempt to one match Vendors(column name of books)
	# 	a) Create a Pandas pivot table and do columns by Bal. Account Type
	#ut.clean_columns(books[0])
	#vendors = books[0].query('GL_Account_Name == "NJ BoH Checking 9666 (BBCN)"')
	#pivotTable = ut.toPivotTable(vendors) 
	#print(pivotTable)
	#oneToOneMatch(pivotTable, banks[0], 'Vendor')
	#print(banks[0])

	#	b) 

	# 3) Attempt to consec match Receivables


def bankReconciliation(books, banks, externalData):
	#for bank in banks:
	reconcile(books[0], banks[0], externalData)
		


	return -1



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