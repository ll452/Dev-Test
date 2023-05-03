# Step 1: Set up your environment
# Install Flask, Requests and YelpAPI using pip:
# pip install Flask requests yelpapi

# Step 2: Create a Flask app
from flask import Flask, render_template, request
import requests
from yelpapi import YelpAPI

app = Flask(__name__)

# Add your API keys
YELP_API_KEY = "C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx"
WEATHER_API_KEY = "5d4ff4f2e99e0cce15a54a4f247fcc58"

yelp_api = YelpAPI(YELP_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    # Step 3: Design the questionnaire
    weather = request.form.get('weather')
    time_of_day = request.form.get('time_of_day')
    mood = request.form.get('mood')
    location = request.form.get('location')

    # Step 4: Use APIs to gather information
    weather_data = get_weather_data(location, WEATHER_API_KEY)
    yelp_data = get_yelp_data(location, mood)

    # Step 5: Implement the recommendation logic
    recommended_idea = generate_recommendation(weather, time_of_day, mood, weather_data, yelp_data)

    return render_template('recommendation.html', recommendation=recommended_idea)

def get_weather_data(location, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    return response.json()

def get_yelp_data(location, term):
    response = yelp_api.search_query(term=term, location=location, sort_by='best_match', limit=10)
    return response['businesses']

def generate_recommendation(weather, time_of_day, mood, weather_data, yelp_data):
    # Add your recommendation logic based on the weather, time of day, mood, and API data
    # For simplicity, we return a random idea from the Yelp data
    import random
    return random.choice(yelp_data)

if __name__ == '__main__':
    app.run(debug=True)
