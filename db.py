import sqlite3


class TeleDB:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS details(Name text, profile text, Date_Time text, peak_experience text, purpose text, contribution text, three_people text, qualities text)"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def add_item(self, Name, profile, Date_Time, peak_experience, purpose, contribution, three_people, qualities):


        stmt = f"INSERT INTO details (Name, profile, Date_Time, peak_experience, purpose, contribution, three_people, qualities) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        args = (Name, profile, Date_Time, peak_experience, purpose, contribution, three_people, qualities)
        self.conn.execute(stmt, args)
        self.conn.commit()
