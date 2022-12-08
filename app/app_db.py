import sqlite3

DB_FILE = "SITE.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE if not Exists users(username TEXT, password TEXT);")


db.commit()
db.close()

def checkuser(username, password): #checks if user's login is correct
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username = ?;', [username])
    correct_password = c.fetchone() #fetches correct password from tuple
    if correct_password is None:
        return False
    else:
        return password == correct_password[0]

        
#returns TRUE if another account exists with user, otherwise creates acc
def create_acc(username, password): 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT username FROM users WHERE username = ?;', [username])
    check_user = c.fetchone();
    if check_user is None:
        c.execute('INSERT INTO users VALUES (?, ?);', (username, password) )
        db.commit()
        return False
    else:
        return True