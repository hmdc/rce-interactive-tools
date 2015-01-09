# This is a simple class which reads the rceapp.yml installed by Puppet
# or any other configuration management.

from yaml import load, dump

class RCEAppDefaultError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which says that a stanza in the YAML is missing the default
  value heading.

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr('A stanza in %s is missing the default value heading.'
        %(self.cfg))

class RCEAppDefaultMemoryError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which says that a default stanza in the provided YML is
  missing a default memory assignment.

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr('A stanza in %s is missing a default memory value.'
        %(self.cfg))

class RCEAppIntError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which says that a default stanza in the provided YML is
  missing a default memory assignment.

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr('Default memory values in %s must be integers.'
        %(self.cfg))


class rceapp:
  """
  This is the rceapp class which manipulates an RCEApp YAML

  Variables:
  cfg = path to RCEApp YML configuration
  """

  def __init__(self, cfg):
    self.cfg = cfg
    
    try:
      with file(cfg, 'r') as _data_stream:
        self.data = load(_data_stream)
    except:
      raise

    self.__validate()

  def __str__(self):
    """
    When you call str on an rceapp object, it just returns the yaml
    as a hash
    """

    return dump(self.data)

  def __validate(self):
    """
    Validates the loaded yml data self.data to ensure that each app has
    a default section at least. If you're not familiar with map and
    lambda, basically this is a loop that applies the lambda function
    over self.apps() which returns an array.

    """
    try:
      map(lambda app: self.data[app]['default'], self.apps())
    except KeyError as e:
      raise RCEAppDefaultError(self.cfg, e)

    # Checks whether default stanzas contain default memory
    try:
      map(lambda app: self.data[app]['default']['memory'],
        self.apps())
    except KeyError as e:
      raise RCEAppDefaultMemoryError(self.cfg, e)

    # Checks whether default memory is an integer, which it should be.
    try:
      map(lambda app: self.data[app]['default']['memory'] + 1,
          self.apps())
    except TypeError as e:
      raise RCEAppIntError(self.cfg, e)
      
  def apps(self):
    """apps() returns the keys of the data loaded from the yaml"""
    return self.data.keys()

  def versions(self,app):
    """
    versions() returns all the versions listed for an app, specified
    by the app argument, in an array.
    """

    _versions = []
    return self.data[app].keys()

  def path(self,app,version):
    """
    path() returns the full path of an application given its version and
    application name as arguments.
    """
    return self.data[app][version]['path']

  def args(self,app,version):
    """
    args() returns a string of arguments for an given application's
    version.
    """

    return ' '.join(self.data[app][version]['args'])

  def memory(self,app,version):
    """
    memory() returns the default memory requirements of an application's
    specified version. If a memory default is not specified for that
    particular version, it grabs the default memory from the default
    stanza for that app.
    """

    _memory = 0
    try:
      _memory = self.data[app][version]['memory']
    except:
      _memory = self.data[app]['default']['memory']
    return _memory