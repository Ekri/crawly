import sqlite3


class UrlCache(object):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sites
            (url text unique)''')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def set(self, url):
        print "url", url

        """
        store the content for a given domain and relative url
        """
        self.cursor.execute("INSERT OR IGNORE INTO sites VALUES (?)",
                            (url,))
        self.conn.commit()

    def get(self, urlQuery):
        """
        return the content for a given domain and relative url
        """
        self.cursor.execute("SELECT content FROM sites WHERE  url=?",
                            urlQuery)
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self, url):
        """
        return all the URLS within a domain
        """
        self.cursor.execute("SELECT url FROM sites WHERE url=?", (url,))
        # could use fetchone and yield but I want to release
        # my cursor after the call. I could have create a new cursor tho.
        # ...Oh well
        return [row[0] for row in self.cursor.fetchall()]

    def get_all(self):
        self.cursor.execute("SELECT * FROM sites")
        return [row[0] for row in self.cursor.fetchall()]
