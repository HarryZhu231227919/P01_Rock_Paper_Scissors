import requests

url =  "https://api.edamam.com/api/recipes/v2"

res = requests.get(url, params={'type':'public', 'app_id':"97c8bd4c", 'app_key':"99402c4f99681503751e94b03de8db33", 'q': "chicken and beef"})

#print(res.json()['hits'][0]['recipe']['label']) # prints the name of the first chicken recipe 
print(res.json()['hits'][0]['recipe']['uri']) 
print(res.json()['hits'][0]['recipe']['label']) 
print(res.json()['hits'][0]['recipe']['cuisineType']) 