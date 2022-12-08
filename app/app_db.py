import sqlite3

DB_FILE = "SITE.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

c.execute("CREATE TABLE if not Exists users(username TEXT, password TEXT);")
c.close()

def checkuser(username, password): #checks if user's login is correct
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username = ?;', [str(username)])
    correct_password = c.fetchone() #fetches correct password from tuple
    if correct_password is None:
        c.close()
        return False
    else:
        c.close()
        return password == correct_password[0]

def user_exists(username): #checks if a user exists
    c = db.cursor()
    result = c.execute("select username from users where username = ?", (str(username),))
    try:
        c.fetchone()[0] == username
        c.close()
        return True
    except:
        c.close()
        return False
        
#returns TRUE if another account exists with user, otherwise creates acc
def create_acc(username, password): 
    c = db.cursor()
    c.execute('SELECT username FROM users WHERE username = ?;', [str(username)])
    check_user = c.fetchone()
    if check_user is None:
        c.execute('INSERT INTO users VALUES (?, ?);', (str(username), str(password)) )
        c.close()
        db.commit()
        return False
    else:
        c.close()
        return True

#print(create_acc("user", "pass"))
#print(checkuser("user", "pas"))

db.commit()