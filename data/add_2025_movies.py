"""
Adds 2025 upcoming and released blockbuster cinema titles to movies_clean.csv
"""
import os
import sys
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

m_path = "data/cleaned/movies_clean.csv"
df = pd.read_csv(m_path)
existing = set(df["title"].str.lower())

movies_2025 = [
    # Hollywood 2025
    {
        "movieId": 300050,
        "title": "Superman (2025)",
        "genres": "Action|Adventure|Sci-Fi",
        "industry": "Hollywood",
        "tag": "dc universe dcu clark kent lois lane james gunn david corenswet rachel brosnahan superhero 2025 release",
        "avg_rating": 4.8,
        "rating_count": 150.0
    },
    {
        "movieId": 300051,
        "title": "The Fantastic Four: First Steps (2025)",
        "genres": "Action|Adventure|Sci-Fi",
        "industry": "Hollywood",
        "tag": "marvel marvel studios mcu reed richards sue storm retro futuristic 1960s pedro pascal vanessa kirby",
        "avg_rating": 4.7,
        "rating_count": 140.0
    },
    {
        "movieId": 300052,
        "title": "Avatar: Fire and Ash (2025)",
        "genres": "Action|Adventure|Sci-Fi",
        "industry": "Hollywood",
        "tag": "pandora na vi ash people fire tribe james cameron sam worthington zoe saldana visually stunning sci-fi",
        "avg_rating": 4.9,
        "rating_count": 220.0
    },
    {
        "movieId": 300053,
        "title": "Jurassic World Rebirth (2025)",
        "genres": "Action|Adventure|Sci-Fi",
        "industry": "Hollywood",
        "tag": "dinosaurs jurassic park covert extraction dna research scarlett johansson jonathan bailey gareth edwards",
        "avg_rating": 4.6,
        "rating_count": 130.0
    },
    {
        "movieId": 300054,
        "title": "A Minecraft Movie (2025)",
        "genres": "Action|Adventure|Comedy",
        "industry": "Hollywood",
        "tag": "minecraft overworld crafting jack black steve jason momoa video game live-action family comedy",
        "avg_rating": 4.4,
        "rating_count": 180.0
    },
    {
        "movieId": 300055,
        "title": "The Naked Gun (2025)",
        "genres": "Action|Comedy|Crime",
        "industry": "Hollywood",
        "tag": "frank drebin jr police squad slapstick spoof comedy liam neeson pamela anderson akiva schaffer",
        "avg_rating": 4.5,
        "rating_count": 120.0
    },
    {
        "movieId": 300056,
        "title": "Mickey 17 (2025)",
        "genres": "Adventure|Comedy|Sci-Fi",
        "industry": "Hollywood",
        "tag": "expendable human clone ice planet colonization bong joon ho robert pattinson mark ruffalo dark sci-fi comedy",
        "avg_rating": 4.7,
        "rating_count": 160.0
    },
    {
        "movieId": 300057,
        "title": "Bridget Jones: Mad About the Boy (2025)",
        "genres": "Comedy|Drama|Romance",
        "industry": "Hollywood",
        "tag": "bridget jones widow modern dating family renee zellweger hugh grant chiwetel ejiofor rom-com comedy",
        "avg_rating": 4.3,
        "rating_count": 110.0
    },
    {
        "movieId": 300058,
        "title": "Mission: Impossible – The Final Reckoning (2025)",
        "genres": "Action|Adventure|Thriller",
        "industry": "Hollywood",
        "tag": "ethan hunt impossible missions force the entity submarine sevastopol tom cruise christopher mcquarrie",
        "avg_rating": 4.9,
        "rating_count": 240.0
    },
    # Bollywood 2025
    {
        "movieId": 90050,
        "title": "Housefull 5 (2025)",
        "genres": "Comedy",
        "industry": "Bollywood",
        "tag": "cruise ship confusion hilarious comedy tarun mansukhani akshay kumar riteish deshmukh abhishek bachchan",
        "avg_rating": 4.4,
        "rating_count": 170.0
    },
    {
        "movieId": 90051,
        "title": "Jolly LLB 3 (2025)",
        "genres": "Comedy|Drama",
        "industry": "Bollywood",
        "tag": "courtroom drama clash of the jollies satire corruption legal fight akshay kumar arshad warsi saurabh shukla",
        "avg_rating": 4.8,
        "rating_count": 210.0
    },
    {
        "movieId": 90052,
        "title": "Welcome to the Jungle (2025)",
        "genres": "Action|Adventure|Comedy",
        "industry": "Bollywood",
        "tag": "jungle expedition madness multi-starrer comedy akshay kumar sanjay dutt suniel shetty ahmed khan",
        "avg_rating": 4.3,
        "rating_count": 140.0
    },
    {
        "movieId": 90053,
        "title": "War 2 (2025)",
        "genres": "Action|Adventure|Thriller",
        "industry": "Bollywood",
        "tag": "spy universe major kabir high-octane action raw agent showdown hrithik roshan jr ntr ayan mukerji",
        "avg_rating": 4.9,
        "rating_count": 260.0
    },
    {
        "movieId": 90054,
        "title": "De De Pyaar De 2 (2025)",
        "genres": "Comedy|Romance",
        "industry": "Bollywood",
        "tag": "age gap relationship family drama romance comedy ajay devgn rakul preet singh r madhavan",
        "avg_rating": 4.3,
        "rating_count": 130.0
    },
    {
        "movieId": 90055,
        "title": "Sikandar (2025)",
        "genres": "Action|Drama",
        "industry": "Bollywood",
        "tag": "mass action social justice grand commercial entertainer a.r. murugadoss salman khan rashmika mandanna",
        "avg_rating": 4.6,
        "rating_count": 220.0
    },
    # Tollywood 2025
    {
        "movieId": 100050,
        "title": "The Raja Saab (2025)",
        "genres": "Comedy|Horror|Romance",
        "industry": "Tollywood",
        "tag": "ancestral palace supernatural romance romantic horror comedy maruthi prabhas malavika mohanan",
        "avg_rating": 4.6,
        "rating_count": 190.0
    },
    {
        "movieId": 100051,
        "title": "Game Changer (2025)",
        "genres": "Action|Drama|Thriller",
        "industry": "Tollywood",
        "tag": "ias officer fair elections political corruption game changer s. shankar ram charan kiara advani",
        "avg_rating": 4.7,
        "rating_count": 200.0
    }
]

appended = []
for m in movies_2025:
    if m["title"].lower() in existing:
        continue
    g_clean = m["genres"].replace("|", " ")
    c_features = f"{m['industry']} {g_clean} {m['tag']} {m['title']}"
    appended.append({
        "movieId": m["movieId"],
        "title": m["title"],
        "genres": m["genres"],
        "industry": m["industry"],
        "tag": m["tag"],
        "avg_rating": m["avg_rating"],
        "rating_count": m["rating_count"],
        "genres_clean": g_clean,
        "content_features": c_features
    })

if appended:
    new_df = pd.concat([df, pd.DataFrame(appended)], ignore_index=True)
    new_df.to_csv(m_path, index=False)
    print(f"🎬 Successfully added {len(appended)} 2025 titles! Total count: {len(new_df)}")
else:
    print("🎬 2025 movies already in catalog.")
