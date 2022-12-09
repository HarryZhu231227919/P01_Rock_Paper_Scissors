from flask import Flask, render_template, request, session, redirect, url_for
import requests
from app_db import *

app = Flask(__name__)
app.secret_key = "fsa932nds02ks3ld93nfjs02ns29rj"

# f = open('keys/key_edamam.txt', 'r') #accesses the file
# e_key = f.read() #edamam key
# f = open('keys/key_spoonacular.txt', 'r')
# s_key = f.read() #spoonacular key
# f = open('keys/id_edamam.txt')
# e_id = f.read()
f = open('app/keys/key_edamam.txt', 'r') #accesses the file
e_key = f.read() #edamam key
f = open('app/keys/key_spoonacular.txt', 'r')
s_key = f.read() #spoonacular key
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
    # print(title.lower().replace(" ", "-"))
    # print(recipe_url.strip('-'))
    # print(recipe_url.__contains__(title.lower().replace(" ", "-")))
    # if title.replace(" ", "-") in recipe_url:
    #     print("TRUEEEEEEEEEEE")
    # else: 
    #     print("FALSEEEEE")
    return render_template("home.html", img_src = image_url, recipe_title = title, url = recipe_url)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template("register.html")
    #else:
        #do the registering checks
        #store user's allergies

@app.route("/profile", methods=['GET', 'POST'])
# def profile():
#     if (request.method == 'GET'):
#         return render_template("profile.html")
#     else: # when user makes an edit to their allergies
#         # return the profile page with updated info

@app.route("/randRecipe", methods=['GET', 'POST'])
def randRecipe():
    if (request.method == 'GET'): #just displaying the random recipe page
        return render_template("randrecipe.html") #need to send in the recipe title, image, and ingredients
    else:
        url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
        #print(url)
        print()
        res = requests.get(url).json() #request to get random recipe
        title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
        image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
        recipe_url = res.get('recipes')[0].get('sourceUrl')
        print(recipe_url.__contains__(title))
        return render_template("randrecipe.html", img_src=image_url, recipe_title=title, url = recipe_url)

# @app.route("/randRecipe/translatedTitle", methods=['GET'])    
# def translate(image_url, title, recipe_url):
#     # a method to get a corssponding language to the curisne type from db
#     # get the translation through google translate api
#     # # translation = 
#     return render_template("randrecipe.html", img_src=image_url, recipe_title=title, url = recipe_url, translation = translation)

@app.route("/specificRecipe", methods=['GET', 'POST'])
def specificRecipe():
    if (request.method == 'GET'): #just shows the specific recipe form
        return render_template("specificrecipe.html")
    else:
        url = "https://api.edamam.com/api/recipes/v2"
        # # to prepare query string to search in api
        # ingredient_qstring = ""
        # for i in range(5):
        #     name = 'ingr' + i
        #     if requests.form[name] != "":
        #         ingredient_qstring += requests.form[name]
        # # allergies string
        #requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'q': ingredient_qstring, }) 

@app.route("/logout")
def logout():
    session.pop("username", None) # removes session info
    return redirect(url_for("login_page")) 

if __name__ == "__main__":
    app.debug = True
    app.run()