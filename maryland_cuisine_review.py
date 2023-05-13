import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Set up the API endpoint and parameters
url = 'https://api.yelp.com/v3/businesses/search'
headers = {
    'Authorization': 'Bearer 2vsyhAeRh_p7nwaroxihHPqi6RVIq3ehkKv35aSEObjkFDLmh80pL4JCj5mr5x9HM-haPBjVQNmupDKmK0hEWjEd9naGDmdTS4MLVNnbJc0C1YEIqNo6rzjEoJ9eZHYx',
}
categories = ['thai', 'italian', 'mexican', 'chinese', 'japanese', 'greek', 'indian', 'american', 'french', 'vietnamese', 'mediterranean', 'korean', 'pizza', 'vegetarian', 'vegan', 'bbq', 'cajun']

# Make the API calls and get the ratings for each category
category_ratings = {}
for category in categories:
    params = {
        'term': 'restaurants',
        'location': 'College Park, MD',
        'categories': category,
    }
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    cumulative_score = 0
    num_restaurants = 0
    
    for restaurant in data['businesses']:
        if 'rating' in restaurant:
            cumulative_score += restaurant['rating']
            num_restaurants += 1
            
    avg_score = cumulative_score / num_restaurants
    
    #store variables in dictionary
    category_ratings[category] = avg_score

sorted_dict = sorted(category_ratings.items(), key=lambda x:x[1])
final_dict = dict(sorted_dict)

#construct the seaborn plot using sorted dict
keys = list(final_dict.keys())
vals = list(final_dict.values())
sns.barplot(x=keys, y=vals)
plt.show()
