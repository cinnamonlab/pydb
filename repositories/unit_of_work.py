import os
from os.path import dirname

from dbadapter.dbconfig import DBConfig
from dbadapter.dbconnect import DBConnect
from libraries.singleton import Singleton
from repositories.cat_repository import CatRepository
from utils.JsonLoader import JsonLoader


class UnitOfWork(Singleton):

    db = None
    # Repositories
    # ailog_repo: AiLogRepostory = None
    # project_repo: ProjectRepository = None
    __cat_repo = None

    def __init__(self):
        self.__initializeConnection()

    def __initializeConnection(self):
        """
        Connect to database with config file
        """
        json_loader = JsonLoader()
        config_file = dirname(os.path.dirname(__file__)) + format('/config.json')
        config_data = json_loader.loadBotConfig(config_file)
        app_config = DBConfig(config_data)
        db_host = app_config.db_host
        db_name = app_config.db_name
        db_user = app_config.db_user
        password = app_config.db_pass

        self.db = DBConnect(host=db_host, database=db_name, user=db_user, password=password)

    def petRepo(self) -> CatRepository:
        if self.__cat_repo is None:
            self.__cat_repo = CatRepository(self.db, 'cats')
        return self.__cat_repo
