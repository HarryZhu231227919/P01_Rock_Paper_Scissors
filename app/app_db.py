import sqlite3

DB_FILE = "SITE.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# User Table==========================================================================================
c.execute("CREATE TABLE if not Exists users(user_id int primary key, username TEXT, password TEXT)")
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
    c.execute("select max(user_id) from users")
    id = c.fetchone()[0]
    if id == None:
        id = 0
    else:
        id += 1
    if not user_exists(username): #user with username doesn't exist
        c.execute('INSERT INTO users VALUES (?, ?, ?);', (id, str(username), str(password)) )
        c.close()
        db.commit()
        return False
    else:
        c.close()
        return True

# print(create_acc("user", "pass"))
# print(checkuser("user", "pas"))
print(create_acc("selena", "pass"))

# Allergies Table===============================================================================
c.execute("CREATE TABLE if not exists allergies(user_id int primary key, crustacean int, dairy int, egg int, fish int, gluten int, peanut int, sesame int, shellfish int, soy int, treenut int, wheat int)") #sqlite stores booleans as ints with 0 as false and 1 as true
#method to insert into the allergies table
def insert_allergy(id, allergy): #allergy is a tuple that holds the int value (0 is false and 1 is true) and matches with the category of the table above
    c = db.cursor()
    c.execute('INSERT INTO allergies VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (id, allergy[0], allergy[1], allergy[2], allergy[3], allergy[4], allergy[5], allergy[6], allergy[7], allergy[8], allergy[9], allergy[10]))
    c.close()
    db.commit()

#also need method to update the allergies table with the users changes

#need to make test cases for both methods

# Cuisine Table===========================================================================================
c.execute("CREATE TABLE if not Exists spoonacular_cuisines(cursine_type text primary key, language text)")
try: 
    c.executescript("""
    INSERT INTO spoonacular_cuisines VALUES("African", "sw");
    INSERT INTO spoonacular_cuisines VALUES("American", "en"); 
    INSERT INTO spoonacular_cuisines VALUES("British", "en"); 
    INSERT INTO spoonacular_cuisines VALUES("Cajun", ""); 
    INSERT INTO spoonacular_cuisines VALUES("Caribbean", "en"); 
    INSERT INTO spoonacular_cuisines VALUES("Chinese", "zh-CN"); 
    INSERT INTO spoonacular_cuisines VALUES("Eastern European", "bg");   
    INSERT INTO spoonacular_cuisines VALUES("European", "en");
    INSERT INTO spoonacular_cuisines VALUES("French", "fr"); 
    INSERT INTO spoonacular_cuisines VALUES("German", "de"); 
    INSERT INTO spoonacular_cuisines VALUES("Greek", "el"); 
    INSERT INTO spoonacular_cuisines VALUES("Indian", "hi"); 
    INSERT INTO spoonacular_cuisines VALUES("Irish", "ga"); 
    INSERT INTO spoonacular_cuisines VALUES("Italian", "it"); 
    INSERT INTO spoonacular_cuisines VALUES("Japanese", "ja"); 
    INSERT INTO spoonacular_cuisines VALUES("Jewish", "he"); 
    INSERT INTO spoonacular_cuisines VALUES("Korean", "ko"); 
    INSERT INTO spoonacular_cuisines VALUES("Latin American", "pt");
    """)
except:
    pass #we don't need anything to be done when there's an error so we use pass

def get_lang(cursine_type):
    c = db.cursor()
    c.execute('SELECT language FROM spoonacular_cuisines WHERE cursine_type = ?;', [str(cursine_type)])
    lang = c.fetchone()[0]
    if lang is None:
        c.close()
        return ""
    else:
        c.close()
        return lang

#print(get_lang("African"))    

db.commit()

