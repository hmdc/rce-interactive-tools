import pytest

@pytest.fixture(scope="module")
def condor():
  from hmdccondor import HMDCCondor
  return HMDCCondor()

@pytest.fixture(scope="module")
def poll_xpra_thread_function():
  from hmdccondor.HMDCCondor import poll_xpra_thread
  return poll_xpra_thread
  
