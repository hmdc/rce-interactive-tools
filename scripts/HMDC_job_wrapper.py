#!/usr/bin/python
import sys
from hmdccondor import HMDCWrapper

wrapper = HMDCWrapper(sys.argv)
wrapper.run()
