from flask import Flask, render_template, request, session, redirect, url_for
import requests, random
from app_db import *

app = Flask(__name__)
app.secret_key = "fsa932nds02ks3ld93nfjs02ns29rj"

f = open('app/keys/key_edamam.txt', 'r') #accesses the file
e_key = f.read() #edamam key
f = open('app/keys/key_googleTranslate.txt')
g_key = f.read() #google translate key
f = open('app/keys/id_edamam.txt')
e_id = f.read()

@app.route("/", methods=['GET', 'POST'])
def login_page():
    if( ("username" in session) and (user_exists(session.get("username"))) ): # checks to see if the user was already logged in
        return redirect(url_for("homePage"))
    if (request.method == 'GET'): #just displaying the login page
        return render_template("login.html")
    else: #POST request made - user attempted to log in
        if(user_exists(request.form.get("username"))):
            if(checkuser(request.form.get("username"),request.form.get("password"))): #username matches the password
                session["username"] = request.form.get("username")
                return redirect(url_for("homePage"))
            return render_template("login.html", error = "Username and password don't match.")
        return render_template("login.html", error = "User does not exist.")

@app.route("/home", methods=['GET', 'POST'])
def homePage():
    if 'username' not in session:    # checks if the user is logged in
        return redirect(url_for("login_page"))

    url = "https://api.edamam.com/api/recipes/v2"
    res = requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'diet': "balanced", 'dishType': "Main course"})
    list_len = len(res.json()['hits'])
    magic_num = random.randint(0, list_len-1)
    title = res.json()['hits'][magic_num]['recipe']['label']
    recipe_url = res.json()['hits'][magic_num]['recipe']['url'] 
    image_url = res.json()['hits'][magic_num]['recipe']['images']['REGULAR']['url']
    cuisine = res.json()['hits'][magic_num]['recipe']['cuisineType'][0]
    ingredients = res.json()['hits'][magic_num]['recipe']['ingredientLines']
    return render_template("home.html", img_src = image_url, recipe_title = title, url = recipe_url)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template("register.html")
    else:
        if request.form['password1'] != request.form['password2']:
            return render_template("register.html", error="Passwords do not match.")
        if (create_acc(request.form.get("username"), request.form.get("password"))):
            allergies = [get_userid(request.form.get("username"))]
            if request.form.get("Crustacean"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Dairy"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Egg"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Fish"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Gluten"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Peanut"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Sesame"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Shellfish"):
                allergies.append(True)
            else:
                allergies.append(False) 
            if request.form.get("Soy"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Treenut"):
                allergies.append(True)
            else:
                allergies.append(False)
            if request.form.get("Wheat"):
                allergies.append(True)
            else:
                allergies.append(False)
            #print(allergies)
            update_allergy(allergies)
            return redirect(url_for("login_page"))
        else:
            return render_template("register.html", error="User already exists.")
         

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' not in session:    # checks if the user is logged in
        return redirect(url_for("login_page"))

    if (request.method == 'GET'):
        # add invocation to get allergy method
        allergies = get_allergy(get_userid(session.get("username")))
        a_string = ""
        for i in allergies:
            a_string += i + ", "
        a_string = a_string[:len(a_string)-2]
        #print(allergies)
        return render_template("userprofile.html", name = session.get("username"), allergies = a_string)
    else: # when user makes an edit to their allergies
        allergies = [get_userid(session.get("username"))]
        if request.form.get("Crustacean"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Dairy"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Egg"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Fish"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Gluten"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Peanut"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Sesame"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Shellfish"):
            allergies.append(True)
        else:
            allergies.append(False)        
        if request.form.get("Soy"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Treenut"):
            allergies.append(True)
        else:
            allergies.append(False)
        if request.form.get("Wheat"):
            allergies.append(True)
        else:
            allergies.append(False)
        update_allergy(allergies)
        allergies = get_allergy(get_userid(session.get("username")))
        a_string = ""
        for i in allergies:
            a_string += i + ", "
        a_string = a_string[:len(a_string)-2]
        #print(allergies)
        # return the profile page with updated info
        return render_template("userprofile.html", name = session.get("username"), allergies = a_string)

@app.route("/randRecipe", methods=['GET', 'POST'])
def randRecipe():
    if 'username' not in session:    # checks if the user is logged in
        return redirect(url_for("login_page"))
    
    if (request.method == 'GET'): 
        return render_template("randrecipe.html")
    else:
        if "option1" in request.form:
            if request.form['option1'] == 'Option 1':
                allergies = get_allergy(get_userid(session["username"]))
                url = "https://api.edamam.com/api/recipes/v2"
                res = requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'health': allergies, 'dishType': "Main course"})
                # print(res.json()['hits'])
                list_len = len(res.json()['hits'])
                magic_num = random.randint(0, list_len-1)
                # print(magic_num)
                title = res.json()['hits'][magic_num]['recipe']['label']
                recipe_url = res.json()['hits'][magic_num]['recipe']['url'] 
                image_url = res.json()['hits'][magic_num]['recipe']['images']['REGULAR']['url']
                cuisine = res.json()['hits'][magic_num]['recipe']['cuisineType'][0]
                ingredients = res.json()['hits'][magic_num]['recipe']['ingredientLines']
                if str(cuisine).__contains__("["):
                    cuisine = str(cuisine)[2:-2]
                #print(cuisine)
                target_lan = get_lang2(cuisine)
                # print(target_lan)

                if target_lan == "" or target_lan == "en":
                    # print("it's going this way----------------")
                    try:
                        magic_num = random.randint(0, len(res.json()['hits']))
                        title = res.json()['hits'][magic_num]['recipe']['label']
                        recipe_url = res.json()['hits'][magic_num]['recipe']['url'] 
                        image_url = res.json()['hits'][magic_num]['recipe']['images']['REGULAR']['url']
                        cuisine = res.json()['hits'][magic_num]['recipe']['cuisineType'][0]
                        ingredients = res.json()['hits'][magic_num]['recipe']['ingredientLines']
                        if str(cuisine).__contains__("["):
                            cuisine = str(cuisine)[2:-2]
                        #print(cuisine)
                        target_lan = get_lang2(cuisine)
                    except:
                        pass # to ensure that the recipe's orgin language is not English
                # print(target_lan)
                # print(title)
                url = "https://google-translate1.p.rapidapi.com/language/translate/v2"               
                payload = f"source=en&target={target_lan}&q={title}" 
                # print(payload)
                headers = {
                    "content-type": "application/x-www-form-urlencoded",
                    "Accept-Encoding": "application/gzip",
                    "X-RapidAPI-Key": str(g_key),
                    "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
                }
                # print(headers)
                response = requests.request("POST", url, data=payload, headers=headers)
                # print(response.json().get("data"))
                translation = response.json().get("data").get("translations")[0].get("translatedText")
                # print(translation)
                # translation = "testingdfd;slkgmsdfmfvafs;dkdj;alsnv;lsdmcfas"
                return render_template("randrecipe.html", img_src = image_url, recipe_title = title, recipe_url = recipe_url, translation = translation, cuisine = cuisine)
        else: # option 2
            allergies = get_allergy(get_userid(session["username"]))
            url = "https://api.edamam.com/api/recipes/v2"
            res = requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'health': allergies, 'dishType': "Main course"})
            list_len = len(res.json()['hits'])
            magic_num = random.randint(0, list_len-1)
            # print(magic_num)
            title = res.json()['hits'][magic_num]['recipe']['label']
            recipe_url = res.json()['hits'][magic_num]['recipe']['url'] 
            image_url = res.json()['hits'][magic_num]['recipe']['images']['REGULAR']['url']
            cuisine = res.json()['hits'][magic_num]['recipe']['cuisineType'][0]
            return render_template("randrecipe.html", img_src = image_url, recipe_title = title, recipe_url = recipe_url, cuisine = cuisine)

@app.route("/specificRecipe", methods=['GET', 'POST'])
def specificRecipe():
    if 'username' not in session:    # checks if the user is logged in
        return redirect(url_for("login_page"))

    if (request.method == 'GET'): #just shows the specific recipe form
        return render_template("specificrecipe.html", submitted = False )
    else:
        q_string = request.form["ingredients"]
        # print(q_string)
        allergies = get_allergy(get_userid(session["username"]))
        # print(allergies)
        url = "https://api.edamam.com/api/recipes/v2"
        res = requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'q': q_string, 'health': allergies})
        # print(res.json()['hits'][0]['recipe']['label'])
        # print(len(res.json()['hits']))
        titles = []
        urls = []
        img_urls = []
        cuisines = []
        ingredients = []
        list_len = len(res.json()['hits'])
        for i in range(list_len):
            # print(i)
            # print(res.json()['hits'][i]['recipe']['label'])
            try: 
                titles.append(res.json()['hits'][i]['recipe']['label'])
                urls.append(res.json()['hits'][i]['recipe']['url']) 
                img_urls.append(res.json()['hits'][i]['recipe']['images']['REGULAR']['url'])
                cuisines.append(res.json()['hits'][i]['recipe']['cuisineType'])
                ingredients.append(res.json()['hits'][i]['recipe']['ingredientLines'])
            except:
                return render_template("specificrecipe.html", error = "Invalid ingredient!", submitted = False )
        # print(titles)
        return render_template("specificrecipe.html", list_len= list_len, recipe_title = titles, recipe_url = urls, img_urls = img_urls, cuisines = cuisines, ingts = ingredients, submitted = True )


@app.route("/cocktail", methods = ["GET"])
def cocktail():
    if 'username' not in session:    # checks if the user is logged in
        return redirect(url_for("login_page"))
        
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    res = requests.get(url).json() #request to get random recipe
    title = res.get('drinks')[0].get("strDrink") #gets the recipe title of that random recipe
    image_url = res.get('drinks')[0].get('strDrinkThumb') #gets the recipe image of that random recipe
    instruction = res.get('drinks')[0].get('strInstructions')
    ingredients = []
    num = 1
    while res.get('drinks')[0].get(f'strIngredient{num}') != None:
        ingredients.append(res.get('drinks')[0].get(f'strIngredient{num}'))
        num += 1
    return render_template("cocktail.html", recipe_title = title, img_src = image_url, instr = instruction, ingr = ingredients)

@app.route("/logout")
def logout():
    session.pop("username", None) # removes session info
    return redirect(url_for("login_page")) 

if __name__ == "__main__":
    app.debug = True
    app.run()