from yaml import load, dump

class rceapp:
  def __init__(self, cfg):
    with file(cfg, 'r') as _data_stream:
      self.data = load(_data_stream)
  def __str__(self):
    return dump(self.data)
  def apps(self):
    return self.data.keys()
  def versions(self,app):
    _versions = []
    return self.data[app].keys()
  def path(self,app,version):
    return self.data[app][version]['path']
  def args(self,app,version):
    return ' '.join(self.data[app][version]['args'])
