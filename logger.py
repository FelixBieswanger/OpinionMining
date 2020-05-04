import logging as logger_py

class Logger:
    def __init__(self,search_term,site):
        # setup logger
        self.logger = logger_py
        self.logger.basicConfig(filename=("./logs/log_"+site+"_"+search_term+".log"), level=self.logger.INFO,
                        format="%(levelname)s;%(asctime)s;%(filename)s;%(lineno)s;%(message)s")
        self.logger.getLogger("requests").setLevel(self.logger.NOTSET)

        self.logger.info("=====================================")
        self.logger.info("Srart Scrape of "+site+" with search-term '"+search_term+"'")

    def getLogger(self):
        return self.logger
        
