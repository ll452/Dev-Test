"""
YELP_API_KEY = "C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx"
WEATHER_API_KEY = "5d4ff4f2e99e0cce15a54a4f247fcc58"
"""
from flask import Flask, render_template, request
import requests
from yelpapi import YelpAPI

app = Flask(__name__)

# Replace with your API keys
YELP_API_KEY = "C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx"
WEATHER_API_KEY = "5d4ff4f2e99e0cce15a54a4f247fcc58"

yelp_api = YelpAPI(YELP_API_KEY)

def get_weather_data(location, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def get_yelp_data(location, term, preferences):
    activity_mapping = {
        'food': 'restaurants',
        'outdoors': 'outdoor, hiking, park, trails',
        'arts': 'arts, museums, galleries',
        'entertainment': 'entertainment, movies, theater'
    }
    activity_term = activity_mapping.get(term, term)
    if term == 'food' and preferences != 'any':
        activity_term = f"{activity_term}, {preferences}"

    response = yelp_api.search_query(term=activity_term, location=location, sort_by='best_match', limit=10)
    return response.get('businesses', [])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    weather = request.form.get('weather')
    time_of_day = request.form.get('time_of_day')
    activity = request.form.get('activity')
    preferences = request.form.get('preferences')
    budget = request.form.get('budget')
    location = request.form.get('location')

    weather_data = get_weather_data(location, WEATHER_API_KEY)
    if not weather_data:
        error_message = f"Invalid location: {location}. Please try again with a valid location."
        return render_template('error.html', error_message=error_message)

    yelp_data = get_yelp_data(location, activity, preferences)
    if not yelp_data:
        error_message = f"No recommendations found for the given location and activity. Please try again with different inputs."
        return render_template('error.html', error_message=error_message)

    # Use yelp_data as a list of recommendations
    recommendations = yelp_data

    # Check if current weather matches the user's preferred weather
    current_weather = weather_data.get("weather", [{}])[0].get("main", "").lower()
    weather_warning = None
    if weather == "sunny" and "clear" not in current_weather:
        weather_warning = "The current weather does not match your preferred sunny weather."
    elif weather == "rainy" and "rain" not in current_weather:
        weather_warning = "The current weather does not match your preferred rainy weather."
    elif weather == "cloudy" and "clouds" not in current_weather:
        weather_warning = "The current weather does not match your preferred cloudy weather."

    return render_template('recommendation.html', recommendations=recommendations, warning=weather_warning)

if __name__ == '__main__':
    app.run(debug=True)

