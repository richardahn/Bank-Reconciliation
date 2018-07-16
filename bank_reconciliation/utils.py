import xlwings as xw # For excel file manipulation
import pandas as pd # For Pandas Dataframe for internal data manipulation
import numpy as np

# Pandas DataFrame Utilities

def sortByDate(book, bank):
	return -1

def clean_string(x):
	if isinstance(x, (bytes, str))
		return x.replace(' ', '_').replace('/', '')
	else
		return x

def clean_columns(df):
	cols = df.columns
	cols = cols.map(clean_string)
	#cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (bytes, str)) else x)
	df.columns = cols
	return

# TODO: Should I use the config file instead? That means I have to use a cfg file every time tho
def toPivotTable(df, values=None, index=None, columns=None, aggfunc=None, fill_value=0):
	if values is None:
		values = 'Amount'
	if index is None:
		index = ['Posting Date']
	if columns is None:
		columns = ['Bal._Account_Type']
	if aggfunc is None:
		aggfunc = np.sum

	return pd.pivot_table(df, values, index, columns, aggfunc, fill_value)



