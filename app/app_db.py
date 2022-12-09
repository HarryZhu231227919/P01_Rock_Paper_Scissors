import sqlite3

DB_FILE = "SITE.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# User Table
c.execute("CREATE TABLE if not Exists users(username TEXT, password TEXT);")
#c.close()

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

# Allergies Table
# Cuisine Table
c.execute("CREATE TABLE if not Exists spoonacular_cuisines(cursine_type text, language text);")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("African", "sw")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("American", "en")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("British", "en")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Cajun", "")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Caribbean", "en")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Chinese", "zh-CN")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Eastern European", "bg")""")  #bulgaria
c.execute("""INSERT INTO spoonacular_cuisines VALUES("European", "en")""") #english
c.execute("""INSERT INTO spoonacular_cuisines VALUES("French", "fr")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("German", "de")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Greek", "el")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Indian", "")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Irish", "ga")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Italian", "it")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Japanese", "ja")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Jewish", "he")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Korean", "ko")""")
c.execute("""INSERT INTO spoonacular_cuisines VALUES("Latin American", "pt")""") #portuguese

def get_lang(cursine_type):
    c = db.cursor()
    c.execute('SELECT language FROM spoonacular_cuisines WHERE cursine_type = ?;', [str(cursine_type)])
    lang = c.fetchone()[0]
    if lang is None:
        return ""
    else:
        c.close()
        return lang

#print(get_lang("African"))    

db.commit()