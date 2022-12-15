import sqlite3

DB_FILE = "SITE.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# User Table==========================================================================================
c.execute("CREATE TABLE if not Exists users(user_id INTEGER primary key, username TEXT, password TEXT)")
c.execute("CREATE TABLE if not exists allergies(user_id int primary key, crustacean int, dairy int, egg int, fish int, gluten int, peanut int, sesame int, shellfish int, soy int, treenut int, wheat int)") #sqlite stores booleans as ints with 0 as false and 1 as true

def checkuser(username, password): #checks if user's login is correct
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username = ?;', (username,))
    correct_password = c.fetchone() #fetches correct password from tuple
    c.close()
    if correct_password is None:
        return False
    else:
        return password == correct_password[0]

def user_exists(username): #checks if a user exists
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute('SELECT user_Id FROM users WHERE username =?;',(username,))
    id = c.fetchone()
    if id is None:
        return False
    c.execute('SELECT username FROM users WHERE user_id =?;', (id[0],))
    user = c.fetchone()
    c.close()
    if user is None:
        return False
    else:
        return True


def get_userid(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute('SELECT user_Id FROM users WHERE username =?;',(username,))
    id = c.fetchone()
    c.close()
    if id is None:
        return False
    return id[0]

  
        
#returns False if another account exists with user, otherwise creates acc
def create_acc(username, password): 
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("select max(user_id) from users")
    id = c.fetchone()[0]
    if id == None:
        id = 0
    else:
        id += 1
    if not user_exists(username): #user with username doesn't exist/ is made
        c.execute('INSERT INTO users VALUES (?, ?, ?);', (id, username, password))
        c.execute('INSERT INTO allergies VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (id,0,0,0,0,0,0,0,0,0,0,0))
        db.commit()
        c.close()
        return True
    else:
        return False

#print(create_acc("selena127", "pass"))
#id = get_userid("selena127")
#print(user_exists("selena127"))
#print(id)
#print(create_acc("selena", "passs"))
#print(checkuser("selena127", "pas")) #should return false because the password is missing a s

# Allergies Table===============================================================================
#method to insert into the allergies table
def update_allergy(allergy): 
    #allergy is a tuple that holds the int value (0 is false and 1 is true) and matches with the category of the table above
    c = db.cursor()
    c.execute('''UPDATE allergies 
    SET crustacean = ?,
    dairy = ?,
    egg = ?,
    fish = ?, 
    gluten = ?, 
    peanut = ? ,
    sesame = ? ,
    shellfish = ?, 
    soy = ? ,
    treenut = ?, 
    wheat = ?
    WHERE user_id = ?;''', 
    (allergy[1], allergy[2], allergy[3], allergy[4], allergy[5], allergy[6], allergy[7], allergy[8], allergy[9], allergy[10], allergy[11], allergy[0]))
    db.commit()
    c.close()


#also need method to update the allergies table with the users changes
def get_allergy(user_id):
    c = db.cursor()
    c.execute('SELECT * FROM allergies WHERE user_id = ?;', (user_id,))
    columns=["crustacean", "dairy", "egg", "fish", "gluten", "peanut", "sesame", "shellfish", "soy", "treenut", "wheat"]
    allergy_info = c.fetchone()
    a_string = ""
    #for loop to iterate through 1 to 11 check if allergy_info(i) == 0 or 1 and if allergy_info(i)==1 then add columns[i] to a_string
    c.close()
    if allergy_info is None:
        return ""
    else:
        return allergy_info

get_allergy(0)
#Test cases for both methods
#create_acc("marc","vicky")
#id = get_userid("marc")
#test = (id,1,1,True,False,0,0,1,0,1,0,1)
#update_allergy(test)
#c.execute('SELECT * FROM allergies WHERE user_id = ?;',(id,))
#print(get_allergy(id))

# Cuisine Table(using Spoonacular API  ==============================================================================
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

def get_lang1(cursine_type):
    c = db.cursor()
    c.execute('SELECT language FROM spoonacular_cuisines WHERE cursine_type = ?;', (cursine_type,))
    lang = c.fetchone()[0]
    c.close()
    if lang is None:
        return ""
    else:
        return lang

#print(get_lang1("African"))    

# Cuisine Table (using EDAMAM Recipe API)=====================================================
c.execute("CREATE TABLE if not Exists edamam_cuisines(cursine_type text primary key, language text)")
try: 
    c.executescript("""
    INSERT INTO edamam_cuisines VALUES("american", "en");
    INSERT INTO edamam_cuisines VALUES("asian", "zh-CN"); 
    INSERT INTO edamam_cuisines VALUES("british", "en"); 
    INSERT INTO edamam_cuisines VALUES("carribean", "en"); 
    INSERT INTO edamam_cuisines VALUES("central europe", "de"); 
    INSERT INTO edamam_cuisines VALUES("chinese", "zh-CN"); 
    INSERT INTO edamam_cuisines VALUES("eastern European", "bg");   
    INSERT INTO edamam_cuisines VALUES("french", "fr");
    INSERT INTO edamam_cuisines VALUES("greek", "el"); 
    INSERT INTO edamam_cuisines VALUES("indian", "hi"); 
    INSERT INTO edamam_cuisines VALUES("italian", "it"); 
    INSERT INTO edamam_cuisines VALUES("japanese", "ja"); 
    INSERT INTO edamam_cuisines VALUES("korean", "ko"); 
    INSERT INTO edamam_cuisines VALUES("mediterranean", "ar"); 
    INSERT INTO edamam_cuisines VALUES("mexican", "es"); 
    INSERT INTO edamam_cuisines VALUES("middle eastern", "fa"); 
    INSERT INTO edamam_cuisines VALUES("nordic", "da"); 
    INSERT INTO edamam_cuisines VALUES("south american", "es"); 
    INSERT INTO edamam_cuisines VALUES("south east asian", "th"); 
    INSERT INTO edamam_cuisines VALUES("world", ""); 
    """)
except:
    pass


def get_lang2(cursine_type):
    c = db.cursor()
    c.execute('SELECT language FROM edamam_cuisines WHERE cursine_type = ?;', (cursine_type,))
    lang = c.fetchone()[0]
    c.close()
    if lang is None:
        return ""
    else:
        return lang


#print(get_lang2("asian")) 

db.commit()

