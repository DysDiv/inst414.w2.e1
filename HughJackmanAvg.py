"""This script checks for the average of Hugh Jackman movie scores."""
import json

with open ("imdb_movies_1985to2022.json", "r") as in_file:
    num_movies = 0
    total_score = 0
    for line in in_file:
        this_movie = json.loads(line)
    
        actors = this_movie["actors"]
        for actor in actors:
            actor_name = actor[1]
            if "Hugh Jackman" in actor_name:
                num_movies += 1
                total_score += this_movie["rating"]["avg"]
    avg_score = total_score / num_movies
    print(avg_score)