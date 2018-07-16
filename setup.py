#!/usr/bin/env python

from distutils.core import setup # Do I need to import distutils.core? some people dont

# install_requires = [] # For dependencies
# tests_require = [] # For test dependencies

setup(name='Bank Reconciliation',
	version='1.0',
	description='Automatic Bank Reconciliation',
	author='Richard Ahn',
	author_email='richahn2@gmail.com',
	url='richardahn.net',
	packages=['bank_reconciliation']
	)