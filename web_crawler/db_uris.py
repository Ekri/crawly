FAITH_WRITE_READ_URI = "vault/faith/retrieved.db"
FAITH_WRITE_READ_MATCHES_URI = "vault/faith/matches.db"

import os


class UrisHelper(object):
    @staticmethod
    def get_path(parent_directory, path):
        return os.path.join(parent_directory, path)

    @staticmethod
    def get_parent_path():
        return os.path.dirname(os.getcwd())

    @staticmethod
    def get_path_with_parent(path):
        return os.path.join(UrisHelper.get_parent_path(), path)
