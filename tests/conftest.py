import pytest

@pytest.fixture(scope="module")
def condor():
  from hmdccondor import HMDCCondor
  return HMDCCondor()
  
