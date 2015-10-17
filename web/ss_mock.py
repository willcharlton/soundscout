#!/usr/bin/env python

import pyonep

_1P = pyonep.onep.OnepV1()

BELL_CIK = '213c297fa96efe50f56c2e62588e042f1c211a55'
AUTH={'cik': BELL_CIK}



while True:
	print(_1P.wait(AUTH, {'alias': 'soundscout'},{}))
