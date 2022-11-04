import toml

def initConfig(path):
    Myconfig = toml.load(path)
    return Myconfig