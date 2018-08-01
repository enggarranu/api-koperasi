import MySQLdb

def get_db():
    # Open database connection
    db = MySQLdb.connect("localhost","root","Password@1","db_koperasi" )
    return db

