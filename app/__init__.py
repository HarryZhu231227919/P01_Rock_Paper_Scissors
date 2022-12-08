from flask import Flask, render_template, request
from flask import session, redirect, url_for #not sure why this is not working
import requests

app = Flask(__name__)

@app.route("/home", methods=['GET', 'POST'])
def homePage():
    # can not figure out how to get a random recipes
    url =  "https://api.edamam.com/api/recipes/v2"
    res = requests.get(url, params={'type':'public', 'app_id':"97c8bd4c", 'app_key':"99402c4f99681503751e94b03de8db33", 'q': "biscuits and gravy"}) # 'diet': "balanced"
    return render_template("home.html", img_src=res.json()['hits'][0]['recipe']['images']['REGULAR']['url'], recipe_title=res.json()['hits'][0]['recipe']['label'])

@app.route("/", methods=['GET', 'POST'])
def login_page():
    if (request.method == 'GET'): #just displayingthe login page
        return render_template("login.html")
    else:
        return render_template("home.html") #placeholder until we get database methods
        #check if user exists in database
            #if user exists, check that password matches password in database
                #if password does not match render_template for login.html with error message
                #if password matches redirect to home page
            #if user doesn't exist, render_template for login.html with error message

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
    #else: #user requested to see another random recipe

@app.route("/specificRecipe", methods=['GET', 'POST'])
def specificRecipe():
    return render_template("specificrecipe.html")

if __name__ == "__main__":
    app.debug = True
    app.run()