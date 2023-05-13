import requests
import networkx as nx
#URL and params
endpoint = 'https://shakespeare.folger.edu/shakespeare/api/works/Rom/witScript'
params = {'format': 'text'}

#API request
response = requests.get(endpoint, params=params)

def count_lines(response, character1, character2):
    for line in response:
        play = f.read()
    character1_lines = 0
    character2_present = False
    for line in play.splitlines():
        if character1 in line:
            character1_lines += 1
            if character2 in line:
                character2_present = True
        elif character2 in line:
            if character2_present:
                character1_lines += 1
            character2_present = True
        else:
            character2_present = False
    return character1_lines

g = nx.Graph()
count_lines(response, endpoint, params)
