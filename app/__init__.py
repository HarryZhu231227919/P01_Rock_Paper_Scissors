from flask import Flask, render_template, request, session, redirect, url_for
import requests
from app_db import *

app = Flask(__name__)
app.secret_key = "fsa932nds02ks3ld93nfjs02ns29rj"

f = open('app/keys/key_edamam.txt', 'r') #accesses the file
e_key = f.read() #edamam key
f = open('app/keys/key_spoonacular.txt', 'r')
s_key = f.read() #spoonacular key
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
    url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
    #print(url)
    res = requests.get(url).json() #request to get random recipe
    title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
    image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
    recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
    while recipe_url.__contains__(title.lower().replace(" ", "-")) != True: #double checks if the link is valid
        res = requests.get(url).json()
        title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
        image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
        recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
    return render_template("home.html", img_src = image_url, recipe_title = title, url = recipe_url)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template("register.html")
    else:
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
            if request.form.get("Seasame"):
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
    if (request.method == 'GET'):
        # add invocation to get allergy method
        allergies = get_allergy(get_userid(session.get("username")))
        #print(allergies)
        return render_template("userprofile.html", name = session.get("username"), allergies = allergies)
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
        if request.form.get("Seasame"):
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
        print(allergies)
        # return the profile page with updated info
        return render_template("userprofile.html", name = session.get("username"), allergies = allergies)

@app.route("/randRecipe", methods=['GET', 'POST'])
def randRecipe():
    if (request.method == 'GET'): #just displaying the random recipe page
        url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
        res = requests.get(url).json() #request to get random recipe
        title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
        image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
        recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
        cuisine = res.get('recipes')[0].get('cuisine') #gets the recipe cuisine type
        while recipe_url.__contains__(title.lower().replace(" ", "-")) != True: #double checks if the link is valid
            res = requests.get(url).json()
            title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
            image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
            recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
            cuisine = res.get('recipes')[0].get('cuisine') #gets the recipe cuisine type
        #print(res.get('recipes')[0])
        return render_template("randrecipe.html", img_src=image_url, recipe_title=title, recipe_url = recipe_url, cuisine = cuisine, clicked = False)
    else:
        url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
        res = requests.get(url).json() #request to get random recipe
        title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
        image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
        recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
        cuisine = res.get('recipes')[0].get('cuisines') #gets the recipe cuisine type
        while recipe_url.__contains__(title.lower().replace(" ", "-")) != True: #double checks if the link is valid
            res = requests.get(url).json()
            title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
            image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
            recipe_url = res.get('recipes')[0].get('sourceUrl') #gets the recipe link of that random recipe
            cuisine = res.get('recipes')[0].get('cuisine') #gets the recipe cuisine type
        return render_template("randrecipe.html", img_src = image_url, recipe_title = title, recipe_url = recipe_url, cuisine = cuisine, clicked = False)


@app.route("/randRecipe/translate/<string:title>/<path:cuisine>/<path:recipe_url>/<path:image_url>", methods = ['GET'])    
#@app.route("/randRecipe/translate/<image_url>/<title>/<recipe_url>/<cuisine>", methods=['GET'])  
def translate(image_url, title, recipe_url, cuisine):
    path = request.path
    index1= (path.index("http")) #index of the first time http shows up which is for the recipe url
    index2 = (path.index("http", path.index("http")+1)) #index of the second time http shows up which is for the image url
    recipe = path[index1:index2]
    image = path[index2:]
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    if cuisine == "None":
        target_lan = "ja"
    else:
        target_lan = get_lang(cuisine)
    payload = f"source=en&target={target_lan}&q={title}" 
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": str(g_key),
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    # {"data":{"translations":[{"translatedText":"スコッチエッグ"}]}}
    # print(response.json().get("data").get("translations")[0].get("translatedText"))
    translation = response.json().get("data").get("translations")[0].get("translatedText")
    # print(translation)
    return render_template("randrecipe.html", img_src = image, recipe_title = title, recipe_url = recipe, translation = translation, clicked = True)


@app.route("/specificRecipe", methods=['GET', 'POST'])
def specificRecipe():
    if (request.method == 'GET'): #just shows the specific recipe form
        return render_template("specificrecipe.html")
    else:
        q_string = request.form.get("ingredients")
        allergies = get_allergy(get_userid(session["username"]))
        # a_string=""
        # for i in allergies:
        #     if (i == 1):
        #         a_string += 
        # url = "https://api.edamam.com/api/recipes/v2"
        res = requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'q': q_string, 'healthLabels': allergies})
        # titles = []
        # urls = []
        # img_urls = []
        # cuisines = []
        # ingredients = []
        # for i in range(20):
        #     try:
        #         titles[i] = res.json()['hits'][i]['recipe']['label']
        #         urls[i] = res.json()['hits'][i]['recipe']['url'] 
        #         img_urls = res.json()['hits'][i]['recipe']['url']
        #         cuisines[i] = res.json()['hits'][i]['recipe']['label']
        #         ingredients[i] = res.json()['hits'][0]['recipe']['ingredientLines']


@app.route("/cocktail", methods = ["GET"])
def cocktail():
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