FAITH_WRITE_READ_URI = "vault/faith/retrieved.db"
FAITH_WRITE_READ_MATCHES_URI = "vault/faith/matches.db"

import os


class UrisHelper(object):
    @staticmethod
    def get_path(parentDirectory, path):
        return os.path.join(parentDirectory, path)
