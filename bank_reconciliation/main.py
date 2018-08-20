'''
Bank Reconciliation
Published by Richard(Woocheol) Ahn
'''

# Custom Libraries
import config as cfg # Config file
import utils as ut # for general reading and conversion
import algorithms as alg # for bank reconciliation
from ledger import Ledger # Only get the Ledger class

def readLedgers(cfg, type):
	"""
	Reads a list of excel files from the list specified in cfg for the type specified

	Args:
		cfg: The config file that contains the list of files
		type: The name of the list that you want from cfg
	Returns:
		A list of Ledger objects that contain the data within the excel files
	Raises:
		Nothing
	"""

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



