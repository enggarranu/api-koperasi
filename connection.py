import MySQLdb

def get_db():
    # Open database connection
    db = MySQLdb.connect("localhost","root","toor","db_koperasi" )
    return db

