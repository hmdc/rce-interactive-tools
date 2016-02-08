import pytest
import os

class TestHmdcCondorClass:

  def test_get_entitlements_method_success(self, monkeypatch, condor):
    "Test whether get_entitlements returns the right entitlements string."

    monkeypatch.setattr('pwd.getpwuid', lambda uid: ['app'])
    assert condor._get_entitlements() == "admin"
  
  def test_get_entitlements_method_failure(self, monkeypatch, condor):
    "Tests whether an unknown LDAP user returns an undefined value"

    import classad
    monkeypatch.setattr('pwd.getpwuid', lambda uid: ['xyzxyzxyzxyzxyz'])
    assert condor._get_entitlements() == classad.Value.Undefined

  def test_get_environment_method(self, monkeypatch, condor):
    """test_get_environment_method() checks whether _get_environment()
    returns environment variables as a space separated string
    subtracting all GNOME and DBUS variables"""

    import os

    monkeypatch.setattr('os.environ', { 'HOME': '/home/app',
      'PYTHONPATH': '/home/app/.local',
      'DBUS_ID': '0XFF',
      'GNOME_ID': '0XFF' })

    assert condor._get_environment() == \
    "HOME='/home/app' PYTHONPATH='/home/app/.local'"

  def test_create_classad_returns_classad(self, monkeypatch, condor):
    """_create_classad() should return a classad"""
    import classad
    monkeypatch.setattr('pwd.getpwuid', lambda uid: ['app'])
    assert isinstance( condor._create_classad('shell', '2.1.32',
      '/usr/bin/gnome-terminal', [], 1, 2048), classad.ClassAd )

  def test_create_classad_creates_correct_output_dir_entries(self,
    monkeypatch, condor):
    """determines whether _create_classad() creates a proper classad"""
    import classad
    import pwd
    import datetime
    import os

    monkeypatch.setattr('pwd.getpwuid', lambda uid: ['app'])
    monkeypatch.setattr('pwd.getpwnam', lambda uid: pwd.struct_passwd( (
      'app', '******', '1000', '10', 'App', '/home/app', '/bin/bash')))

    ad = condor._create_classad('shell', '2.1.32', '/usr/bin/gnome-terminal',
      [], 1, 2048)

    ad['ClusterId'] = '1.0'

    assert os.path.isabs(ad['Out'].eval())
    assert os.path.isabs(ad['Err'].eval())
    assert os.path.isabs(ad['LocalJobDir'].eval())

    assert '/home/app' in ad['Out'].eval()
    assert '/home/app' in ad['Err'].eval()
    assert '/home/app' in ad['LocalJobDir'].eval()
 
  def test_poll_xpra_thread(self, monkeypatch, poll_xpra_thread_function):
    display_id = poll_xpra_thread_function("{0}/fixtures/shell_2.31.3_129_201601271453946250/out.txt".format(os.path.dirname(os.path.realpath(__file__))))
    assert int(display_id) >= 0

