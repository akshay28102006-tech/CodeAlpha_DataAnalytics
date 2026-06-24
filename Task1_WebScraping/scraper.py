# Task 1 - Web Scraping
# Source: IMDB Top 250
# Data: Rank, Title, Year, Rating, Votes, Genre, Director, Description

import requests
import pandas as pd
import json

print("IMDB Top 250 scraping shuru...")

url = "https://raw.githubusercontent.com/theapache64/top250/master/top250.json"
response = requests.get(url)
data = json.loads(response.text)

movies = []

for i, movie in enumerate(data):
    
    # Rating aur Votes
    rating_info = movie.get("aggregateRating", {})
    rating      = rating_info.get("ratingValue", None)
    votes       = rating_info.get("ratingCount", None)
    
    # Year — datePublished se pehle 4 characters
    date = movie.get("datePublished", "")
    year = date[:4] if date else None
    
    # Genre — list hai, string banao
    genre = movie.get("genre", [])
    genre = ", ".join(genre) if isinstance(genre, list) else genre
    
    # Director
    directors = movie.get("director", [])
    director  = directors[0].get("name", "") if directors else ""
    
    # Title
    title = movie.get("name", "")
    
    # Description
    description = movie.get("description", "")
    
    # Content Rating
    content_rating = movie.get("contentRating", "")

    movies.append({
        "Rank"          : i + 1,
        "Title"         : title,
        "Year"          : year,
        "Rating"        : rating,
        "Votes"         : votes,
        "Genre"         : genre,
        "Director"      : director,
        "Description"   : description,
        "Content_Rating": content_rating
    })

# DataFrame banao
df = pd.DataFrame(movies)

# Types fix karo
df["Year"]   = pd.to_numeric(df["Year"],   errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Votes"]  = pd.to_numeric(df["Votes"],  errors="coerce")

# CSV save karo
df.to_csv("imdb_top250.csv", index=False)

print(f"✅ Task 1 Complete! {len(df)} movies scrape ho gayi")
print("\nPehli 5 movies:")
print(df.head())
print("\nData Info:")
print(df.info())