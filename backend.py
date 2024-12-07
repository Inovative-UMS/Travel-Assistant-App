from io import BytesIO
from fastapi import FastAPI
from pydantic import BaseModel
from neo4j import GraphDatabase
import folium

app = FastAPI()

# Neo4j Database Connection
class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def save_preferences(self, user, preferences):
        with self.driver.session() as session:
            session.run("MERGE (u:User {name: $user}) "
                        "SET u.preferences = $preferences", user=user, preferences=preferences)

    def get_preferences(self, user):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {name: $user}) RETURN u.preferences as preferences", user=user)
            return result.single()["preferences"]


# rYQzhRPyMJ1K1XMgVzarXKTWsYntM4ybi4TC2pvhA4g
db = Database("neo4j+s://3e89ecb2.databases.neo4j.io:7687", "neo4j", "rYQzhRPyMJ1K1XMgVzarXKTWsYntM4ybi4TC2pvhA4g")  # Replace with your credentials

# Models
class Preferences(BaseModel):
    user: str
    city: str
    budget: int
    interests: list
    timings: dict


@app.post("/save_preferences/")
def save_preferences(prefs: Preferences):
    db.save_preferences(prefs.user, prefs.dict())
    return {"status": "Preferences saved successfully!"}


@app.get("/get_preferences/{user}")
def get_preferences(user: str):
    return {"preferences": db.get_preferences(user)}

@app.post("/generate_map/")
def generate_map(attractions: list):
    map_ = folium.Map(location=attractions[0]["location"], zoom_start=12)  # Use the first attraction's location
    for attraction in attractions:
        folium.Marker(
            location=attraction["location"],
            popup=attraction["name"]
        ).add_to(map_)
    
    # Save the map to a file-like object
    map_io = BytesIO()
    map_.save(map_io, close_file=False)
    return {"map": map_io.getvalue()}


# Weather API
WEATHER_API_KEY = "your_openweather_api_key"  # Replace with your key

@app.get("/get_weather/{city}")
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    response = requests.get(url).json()
    weather = {
        "description": response["weather"][0]["description"],
        "temperature": response["main"]["temp"] - 273.15,  # Convert Kelvin to Celsius
        "humidity": response["main"]["humidity"]
    }
    return weather
