# This is a simple class which reads the rceapp.yml installed by Puppet
# or any other configuration management.

from yaml import load, dump

class RCEAppGlobalError(Exception):
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
    return repr('A stanza in %s is missing the global value heading.'
        %(self.cfg))

class RCEAppDefaultError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which says that at least one version of an app should have the
  default set to True

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr("Either at least one version requires the default\
     boolean in %s, two versions have the default boolean, or default is\
     not set to true or false." %(self.cfg))


class RCEAppGlobalMemoryError(Exception):
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
    return repr('A stanza in %s is missing a global memory value.'
        %(self.cfg))

class RCEAppGlobalCpuError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which says that a default stanza in the provided YML is
  missing a default cpu assignment.

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr('A stanza in %s is missing a cpu value.'
        %(self.cfg))


class RCEAppIntError(Exception):
  """
  This is a self-defined exception such that I can output a useful error
  message which notifies you if you accidentially used non-integer
  characters in the memory field.

  Variables:
  cfg: path to the RCEApp YML configuration
  value: KeyError exception object
  """

  def __init__(self, cfg, value):
    self.value = value
    self.cfg = cfg
  def __str__(self):
    return repr('Default memory/cpu values in %s must be integers.'
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
      map(lambda app: self.data[app]['global'], self.apps())
    except KeyError as e:
      raise RCEAppGlobalError(self.cfg, e)

    # Checks whether default stanzas contain default memory
    try:
      map(lambda app: self.data[app]['global']['memory'],
        self.apps())
    except KeyError as e:
      raise RCEAppGlobalMemoryError(self.cfg, e)

    # Checks whether default stanzas contain default cpu count
    try:
      map(lambda app: self.data[app]['global']['cpu'],
          self.apps())
    except KeyError as e:
      raise RCEAppGlobalCpuError(self.cfg, e)

    # Checks whether default memory is an integer, which it should be.
    try:
      map(lambda app: self.data[app]['global']['memory'] + 1,
          self.apps())
    except TypeError as e:
      raise RCEAppIntError(self.cfg, e)

    # Checks whether default cpu is an integer, which it should be.
    try:
      map(lambda app: self.data[app]['global']['cpu'] + 1,
          self.apps())
    except TypeError as e:
      raise RCEAppIntError(self.cfg, e)



    # Checks whether at least one version is default, no more than one
    # default key per entry, and that value is a boolean.
    default_map = map(lambda app: map(lambda version:
      self.data[app][version]['default'] if
      self.data[app][version].has_key('default') else None,
      self.versions(app)),
      self.apps())

    sorted_count = sorted(map(lambda x: x.count(True), default_map))
    if sorted_count[0] == 0:
      raise RCEAppDefaultError(self.cfg, "No default.")
    elif sorted_count[-1] > 1:
      raise RCEAppDefaultError(self.cfg, "Too many defaults.")

  def apps(self):
    """apps() returns the keys of the data loaded from the yaml"""
    return self.data.keys()

  def versions(self,app):
    """
    versions() returns all the versions listed for an app, specified
    by the app argument, in an array.
    """

    return filter(
        lambda key: key != 'global',
        self.data[app].keys()
        )

  def app_version_exists(self,app,version=None):
    if version:
      return (True if app in self.apps() and version in
      self.versions(app) else False)
    else:
      return (True if app in self.apps() else False)

  def command(self,app,version=None):
    """
    command() returns the full path of an application given its version and
    application name as arguments.
    """
    _version = version if version else self.get_default_version(app)
    return self.data[app][_version]['command']

  def args(self,app,version=None):
    """
    args() returns a string of arguments for an given application's
    version.
    """
    _version = version if version else self.get_default_version(app)

    try:
      return ' '.join(self.data[app][_version]['args'])
    except:
      try:
        return ' '.join(self.data[app]['global']['args'])
      except:
        return None

  def get_default_version(self, app):
    _versions = map (lambda version: version if self.is_default(app,version) else
        None,
        self.versions(app))
    return sorted(_versions)[-1]

  def is_default(self,app,version):
    """
    Returns True if app,version is the default version for the app.
    """

    try:
      return self.data[app][version]['default']
    except:
      return False

  def memory(self,app,version=None):
    """
    memory() returns the default memory requirements of an application's
    specified version. If a memory default is not specified for that
    particular version, it grabs the default memory from the default
    stanza for that app.
    """
    _version = version if version else self.get_default_version(app)
    try:
      return self.data[app][_version]['memory']
    except:
      return self.data[app]['global']['memory']

  def cpu(self,app,version=None):
    """
    cpu() returns the default CPU count requirement of an application's
    specified version. If a cpu default is not specified for that
    particular version, it grabs the default memory from the default
    stanza for that app.
    """
    _version = version if version else self.get_default_version(app)
    try:
      return self.data[app][_version]['cpu']
    except:
      return self.data[app]['global']['cpu']
