from flask import Flask, render_template, request
from flask import session, redirect, url_for #not sure why this is not working
import requests
from app_db import *

app = Flask(__name__)
app.secret_key = "fsa932nds02ks3ld93nfjs02ns29rj"

f=open('keys/key_edamam.txt', 'r') #accesses the file
e_key=f.read() #edamam key
f=open('keys/key_spoonacular.txt', 'r')
s_key = f.read() #spoonacular key
f=open('keys/id_edamam.txt')
e_id = f.read()

@app.route("/home", methods=['GET', 'POST'])
def homePage():
    url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
    #print(url)
    res = requests.get(url).json() #request to get random recipe
    title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
    image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
    recipe_url = res.get('recipes')[0].get('sourceUrl')
    return render_template("home.html", img_src=image_url, recipe_title=title, url = recipe_url)

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
            return render_template("login.html", error="Username and password don't match.")
        return render_template("login.html", error="User does not exist.")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template("register.html")
    #else:
        #do the registering checks

@app.route("/randRecipe", methods=['GET', 'POST'])
def randRecipe():
    if (request.method == 'GET'): #just displaying the random recipe page
        return render_template("randrecipe.html") #need to send in the recipe title, image, and ingredients
    else:
        url = f"https://api.spoonacular.com/recipes/random?apiKey={s_key}"
        #print(url)
        res = requests.get(url).json() #request to get random recipe
        title = res.get('recipes')[0].get('title') #gets the recipe title of that random recipe
        image_url = res.get('recipes')[0].get('image') #gets the recipe image of that random recipe
        recipe_url = res.get('recipes')[0].get('sourceUrl')
        return render_template("randrecipe.html", img_src=image_url, recipe_title=title, url = recipe_url)
    

@app.route("/specificRecipe", methods=['GET', 'POST'])
def specificRecipe():
    if (request.method == 'GET'): #just shows the specific recipe form
        return render_template("specificrecipe.html")
    else:
        url = "https://api.edamam.com/api/recipes/v2"
        #requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'q': request.form[], }) 

@app.route("/logout")
def logout():
    session.pop("username",None) # removes session info
    return redirect(url_for("login_page")) 

if __name__ == "__main__":
    app.debug = True
    app.run()