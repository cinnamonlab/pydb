# Extract information config  from config.json file at the root folder

class DBConfig:
    db_host = ""
    db_user = ""
    db_pass = ""
    db_name = ""

    def __init__(self, configdata):
        self.db_host = configdata['db_host']
        self.db_user = configdata['db_user']
        self.db_pass = configdata['db_pass']
        self.db_name = configdata['db_name']