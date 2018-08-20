import xlwings as xw # For excel file manipulation
import pandas as pd # For Pandas Dataframe for internal data manipulation
import numpy as np
import os

# Pandas DataFrame Utilities
def newExcel(ledger, bookName=None, sheetName=None):
	# Add a book and link the Ledger with the book
	book = xw.Book()
	ledger.book = book
	sheet = book.sheets[0]
	ledger.sheet = sheet
	if sheetName is not None:
		sheet.name = sheetName

	# Get rid of the internal matches column
	ledgerToShow = ledger.ledger.drop('Matches', axis=1)

	# Add all the values
	sheet.range('A1').value = ledgerToShow

	# Save it
	dir = ''
	if bookName is None:
		dir = os.getcwd() + r'\output\example.xlsx'
	else:
		dir = os.getcwd() + '\\output\\' + bookName # Didn't use r cause otherwise warning
	book.save(dir) # Backslashes are treated as a literal

def sortByDate(ledger):
	ledger.ledger.sort_values(by=[clean_string('Date')], ascending=True, inplace=True, kind='mergesort') # For the stable property
	return

def clean_string(x):
	if isinstance(x, (bytes, str)):
		return x.replace(' ', '_').replace('/', '')
	else:
		return x

def clean_columns(df):
	cols = df.columns
	cols = cols.map(clean_string)
	df.columns = cols
	return

# TODO: Should I use the config file instead? That means I have to use a cfg file every time tho
def toPivotTable(df, values=None, index=None, columns=None, aggfunc=None, fill_value=0):
	if values is None:
		values_title = 'Amount'
		values = clean_string(values_title)
	if index is None:
		index_title = 'Posting Date'
		index = [clean_string(index_title)]
	if columns is None:
		columns_title = 'Bal. Account Type'
		columns = [clean_string(columns_title)] # I need to clean this string because I was forced to clean them beforehand, so I must use cleaned strings to match now
	if aggfunc is None:
		aggfunc = np.sum

	'''
	I need the v
	'''
	return pd.pivot_table(df, values, index, columns, aggfunc, fill_value).reset_index()



