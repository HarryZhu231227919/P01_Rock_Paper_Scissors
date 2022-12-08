from flask import Flask, render_template, request
from flask import session, redirect, url_for #not sure why this is not working
import requests

app = Flask(__name__)
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
        requests.get(url, params={'type':'public', 'app_id':e_id, 'app_key':e_key, 'q': request.form[], }) 

if __name__ == "__main__":
    app.debug = True
    app.run()