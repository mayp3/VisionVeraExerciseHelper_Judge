import logging

global LoggingFactory

class InitLoggingFacotory:
    def __init__(self,config):
        logging.basicConfig(level=logging._nameToLevel[config["level"]],
                            filename=config["path"],
                            datefmt='[%m-%d %H:%M:%S]',
                            format = '%(asctime)s [%(levelname)s]  %(name)s/%(lineno)s || %(message)s')
        self.fh = logging.FileHandler(filename=config["path"],encoding="utf-8", mode="a")


    def logger(self,name):
        logger = logging.getLogger(name)
        logger.addFilter(self.fh)
        return logging.getLogger(name)


