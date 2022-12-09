#testing the edamam API here
import requests

url =  "https://api.edamam.com/api/recipes/v2"

res = requests.get(url, params={'type':'public', 'app_id':"97c8bd4c", 'app_key':"99402c4f99681503751e94b03de8db33", 'q': "rice and beef", 'healthLabels': "No-oil-added"})

print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
print()
# print(res.json())
#print(res.json()['hits'][0]['recipe']['url']) 
print(res.json()['hits'][0]['recipe']['healthLabels'])
print()
print(res.json()['hits'][0]['recipe']['dietLabels'])  
print()
print(res.json()['hits'][0]['recipe']['cautions']) 
print()
print(res.json()['hits'][0]['recipe']['ingredientLines'])
# print(res.json()['hits'][0]['recipe']['label']) 
# print(res.json()['hits'][0]['recipe']['cuisineType']) 

#testing the spoonacular API here: 
# import requests
# res = requests.get("https://api.spoonacular.com/recipes/random?apiKey=12643cbc7c944fc18030685f17426c85").json() #request to get random recipe
# print(res.get('recipes')[0].get('title')) #gets the recipe title of that random recipe
# print(res.get('recipes')[0].get('image')) #gets the recipe image of that random recipe
