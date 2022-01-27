import sqlite3
import hashlib
from sqlite3.dbapi2 import Cursor
import uuid
from urllib.request import pathname2url

class Credential:
    add_user_sql = "INSERT INTO users VALUES (?,?,?);"
    

    def create_database(self):
        user_table_definition = """
            CREATE TABLE users (
            username TEXT,
            salt TEXT,
            hpassword TEXT
        )"""
        try:
            dburi = 'file:{}?mode=rw'.format(pathname2url("D:\projects\SocketProgramming\login.db"))
            self.connection = sqlite3.connect(dburi, uri=True,check_same_thread=False)
            self.cursor = self.connection.cursor()
            #self.cursor.execute(user_table_definition)
        except sqlite3.OperationalError:
            self.connection = sqlite3.connect("D:\projects\SocketProgramming\login.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute(user_table_definition)


    # Add incoming user
    def add_new_user(self,username,password):
        username = username
        password = password

        salt = uuid.uuid4().hex
        hashedpassword = hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()
        data = (username,salt,hashedpassword)
        self.cursor.execute(self.add_user_sql,data)
        self.connection.commit()
        return True

    # Check incoming user
    def check_user(self,username,password):
        username = username
        password = password

        row = self.cursor.execute("SELECT salt, hpassword FROM users WHERE username = ?",(username,)).fetchone()
        try:
            salt, hpassword = row  # Unpacking the row information - btw this would fail if the username didn't exist
        except:

            with self.connection:
                self.cursor.execute("SELECT * FROM users")
                print(self.cursor.fetchall())
            return "user not found"
        hashedIncomingPwd = hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()

        if hashedIncomingPwd == hpassword:
            return "pass"
        else:
            return "failed"
         