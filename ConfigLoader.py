import yaml

class ConfigLoader:
  def __init__(self,config_file):
    self.config_file = config_file
    self.config = slef.load_config()

  def load_config(self):
    with open(self.config_file,'r')
    as file:
      config = yaml.safe_load(file)

    return config

  def get_database_config
