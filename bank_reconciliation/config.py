# Configuration file for bank reconciliation
# TODO: Later on, I can create a generateParameters() function that generates a dictionary(like config) and passes that instead of this external and global file
# Then, if i do it that way, it seems weird to separate the fact that i automatically assume the sheet name is the bank name from this generation process. I should include this in the generation process

# TODO: After the generation process, you can also create a UI that lets you easily enter data into config.py, to make it more user-friendly
config = {
	# Locate based on directory
	# TODO: Should I have a working directory that prefixes the files?
	'working_directory': '',

	# Inputs
	'files': {
		# Format: ('file-path', 'sheet-name', 'ledger-name')
		'books': {
			('data/sample/Book1.xlsm', 'BookLedger', None) 
			},
		'banks': {
			('data/sample/Bank1.xlsm', 'NJ BoH Checking 9666 (BBCN)', None)
		}
	},

	'bank-types': {
		('BBCN', 'EFT'), # Same day transfer, check within 1 day
		('Shinhan ACH 3282', 'ACH') # All kinds of transactions(AP and AR)
	},

	# TODO: Bank aliases? to see which previous bank rec to use from the prev bank rec sheet

	# Column aliases
	'column-aliases': {
		'Bal. Account Type': ('Balance Account Type', 'BAT')
	},

	# Outputs
	'output': '/output/BankReconciliationStatement.xlsm' 

}