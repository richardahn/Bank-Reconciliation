'''
Bank Reconciliation
Published by Richard(Woocheol) Ahn
'''

# Custom Libraries
import config as cfg # Config file
import utils as ut # for general reading and conversion
import algorithms as alg # for bank reconciliation

def readLedgers(cfg, type):
	'''
	Reads a list of excel files

	Input: a list of pairs representing the excel file, and whether you want the book or bank ledgers
	Output: a list of Ledger objects
	'''

	# TODO: How do I do read-only access, and not have them open up when I call Book()?
	return [Ledger(file=file) for file in cfg['files'][type]]

def main():

	# 1) Read in book and bank ledgers, and any useful external data
	books = readLedgers(cfg.config, 'books')
	banks = readLedgers(cfg.config, 'banks')
	externalData = -1 # TODO: In order to have this be compatible, make externalData a Pandas DataFrame so that it can be plugged in, just like the books or banks

	# 2) Apply bank reconciliation
	alg.bankReconciliation(books, banks, externalData)


if __name__ == "__main__":
	main()



