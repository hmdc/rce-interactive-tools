#!/usr/bin/env python2.6
import sys
from hmdccondor import HMDCWrapper

wrapper = HMDCWrapper(sys.argv)
wrapper.run()
