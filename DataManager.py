import sqlite3 as Lite
import mmap
import os.path

#using sqlite3
class BotSql:
    """This class helps storing a tweeter bot information in sqlite3"""
    def __init__(self, db_name = "botDB"):
        self.fileName = db_name + ".db"
        self.DatabaseName = db_name
        if os.path.isfile(self.fileName) == True:
            ##Database file does exist
            self.dbCon = Lite.connect(self.fileName)
            self.Curs = self.dbCon.cursor()
        else:
            ##Database does not exist there for make the database and all the needed tables
            self.dbCon = Lite.connect(self.fileName)
            self.dbCon.execute("CREATE TABLE Tweets(id INTEGER PRIMARY KEY AUTOINCREMENT, tweetid TEXT, tweetuserid TEXT);") ##All the processed tweets go here
            self.dbCon.execute("CREATE TABLE Ban(id INTEGER PRIMARY KEY AUTOINCREMENT, tweetuserid TEXT, reason TEXT);") ##Ban list
            self.dbCon.execute("CREATE TABLE Admins(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, tweetuserid TEXT, email TEXT);") ##A list of admins of the bot
            self.dbCon.execute("CREATE TABLE Mentions(id INTEGER PRIMARY KEY AUTOINCREMENT, tweetid TEXT, tweetuserid TEXT, command TEXT);") ## All the processed tweets in the mention timeline go here
            self.Curs = self.dbCon.cursor()

    ##Proccessed tweets
    def add_Tweet(self,tweetid,userid):
        sql_query = "INSERT INTO Tweets (tweetid,tweetuserid) VALUES (?, ?)"
        sql_data = (tweetid, userid)
        try:
            self.Curs.execute(sql_query, sql_data)
            self.dbCon.commit()
        except Lite.Error as er:
            print("(Add Tweet) Sqlite3 Error: " + str(er.__dict__))
    def remove_Tweet(self,tweetid):
        try:
            self.dbCon.execute("DELETE FROM Tweets WHERE tweetid = '" + tweetid +"'")
        except Lite.Error as er:
            print("(Remove Tweet)Sqlite3 Error: " + str(er.__dict__))
    def check_Tweet(self,tweetid):
        try:
            tweetid.replace(" ","")
            self.Curs.execute("SELECT COUNT(*) from Tweets where tweetid = '" + tweetid + "' OR tweetid = '" + tweetid + " '")
            res=self.Curs.fetchone()
            no_of_rows = res[0]
            if no_of_rows > 0:
                return True
            else:
                return False
        except Lite.Error as er:
            print("(Check Tweet) Sqlite3 Error: " + str(er.__dict__))

    ##Banned users
    def ban_User(self,userid, reason = "NONE PROVIDED"):
        sql_query = "INSERT INTO Ban (tweetuserid,reason) VALUES (?, ?)"
        sql_data = (userid, reason)
        try:
            self.Curs.execute(sql_query, sql_data)
            self.dbCon.commit()
        except Lite.Error as er:
            print("(Ban User) Sqlite3 Error: " + str(er.__dict__))
    def unban_User(self,userid):
        try:
            self.dbCon.execute("DELETE FROM Ban WHERE tweetuserid = '" + userid + "'")
        except Lite.Error as er:
            print("(Unban User) Sqlite3 Error: " + str(er.__dict__))
    def check_Ban(self,userid):
        try:
            userid.replace(" ","")
            self.Curs.execute("SELECT COUNT(*) from Ban where tweetuserid = '" + userid + "'OR tweetuserid = '" + userid + " '")
            res=self.Curs.fetchone()
            no_of_rows = res[0]
            if no_of_rows > 0:
                return True
            else:
                return False
        except Lite.Error as er:
            print("(Check Ban) Sqlite3 Error: " + str(er.__dict__))

    ##Admins list
    def add_Admin(self,userid, name, email):
        sql_query = "INSERT INTO Admins (name,tweetuserid,email) VALUES (?, ?, ?)"
        sql_data = (name, userid, email)
        try:
            self.Curs.execute(sql_query, sql_data)
            self.dbCon.commit()
        except Lite.Error as er:
            print("(Add Admin) Sqlite3 Error: " + str(er.__dict__))
    def remove_Admin(self,userid):
        try:
            self.dbCon.execute("DELETE FROM Admins WHERE tweetuserid = '" + userid + "'")
        except Lite.Error as er:
            print("(Remove Admin) Sqlite3 Error: " + str(er.__dict__))
    def check_Admin(self,userid):
        try:
            userid.replace(" ","")
            self.Curs.execute("SELECT COUNT(*) from Admins where tweetuserid = '" + userid + "'")
            res=self.Curs.fetchone()
            no_of_rows = res[0]
            if no_of_rows > 0:
                return True
            else:
                return False
        except Lite.Error as er:
            print("(Check Admin) Sqlite3 Error: " + str(er.__dict__))
    ##Mentions
    def add_Mention(self,tweetid,userid, command):
        sql_query = "INSERT INTO Mentions (tweetid,tweetuserid,command) VALUES (?, ?, ?)"
        sql_data = (tweetid, userid, command)
        try:
            self.Curs.execute(sql_query, sql_data)
            self.dbCon.commit()
        except Lite.Error as er:
            print("(Add Mention) Sqlite3 Error: " + str(er.__dict__))
    def remove_Mention(self,tweetid):
        try:
            self.dbCon.execute("DELETE FROM Mentions WHERE tweetid = '" + tweetid + "'")
        except Lite.Error as er:
            print("(Remove Mention) Sqlite3 Error: " + str(er.__dict__))
    def check_Mention(self,tweetid):
        try:
            tweetid.replace(" ","")
            self.Curs.execute("SELECT COUNT(*) from Mentions where tweetid = '" + tweetid + "' OR tweetid = '" + tweetid + " '")
            res=self.Curs.fetchone()
            no_of_rows = res[0]
            if no_of_rows > 0:
                return True
            else:
                return False
        except Lite.Error as er:
            print("(Check Mention) Sqlite3 Error: " + str(er.__dict__))

    def get_stats(self):
        stats_str = ""
        try:
            self.Curs.execute("SELECT COUNT(*) from Tweets")
            res=self.Curs.fetchone()
            no_of_rows = res[0]
            stats_str = str(no_of_rows) + " processed tweets | "
            self.Curs.execute("SELECT COUNT(*) from Ban")
            res2=self.Curs.fetchone()
            no_of_rows2 = res2[0]
            stats_str += str(no_of_rows2) + " banned users | "
            self.Curs.execute("SELECT COUNT(*) from Mentions")
            res3=self.Curs.fetchone()
            no_of_rows3 = res3[0]
            stats_str += str(no_of_rows3) + " mentions"

            return stats_str
        except Lite.Error as er:
            print("(Check Mention) Sqlite3 Error: " + str(er.__dict__))



#Using text files (.txt)
class BotText:
    """This class helps keeping all the ids saved in a txt file"""
    def __init__(self, fileName):
        cFilename = self.Check_fileName(fileName)
        self.fileName = fileName
        if os.path.isfile(self.fileName) == False:
            file = open(self.fileName, 'w')
            file.write("*_INI FILE_*\n")
    def is_stored_b(self, id_string):
        Found = False
        if os.path.isfile(self.fileName) == False:
            return Found
        with open(self.fileName, 'rb', 0) as file, \
             mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(bytes(id_string, 'UTF-8')) != -1:
                Found = True
        return Found
    def is_stored(self, id_string):
        Found = False
        if os.path.isfile(self.fileName) == False:
            return Found
        if id_string in open(self.fileName).read():
            Found = True
        return Found;
    def add_id(self, id_string):
        if os.path.isfile(self.fileName) == False:
            file = open(self.fileName, 'w')
        else:
            file = open(self.fileName, 'a')
        if not self.is_stored_b(id_string):
            file.write(id_string + "\n")
            file.close()
        return
    def remove_id(self, id_string):
        if os.path.isfile(self.fileName) == True:
            file = open(self.fileName,"r")
            fileData = file.readlines()
            file.close()
            file = open(self.fileName,"w")
            for line in fileData:
                if line!=id_string+"\n":
                    file.write(line)
            file.close()
        return
    def set_fileName(self, name):
        self.fileName = name
        return
    def check_fileName(self, name):
        newName = name
        if ".txt" in name:
            narr = name.split('.')
            if not narr[(len(narr) - 1)] == "txt":
                newName = newName + ".txt"
        return newName
