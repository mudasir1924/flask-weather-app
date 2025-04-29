from flask import Flask, render_template, request
import requests  # Import requests to call the weather API

app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = "8ebcc6bb8235174ed859cf577dcef61b"  

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None # Will hold weather info to show on page
    error = None # Will hold error message if any

    if request.method == 'POST':
        city = request.form.get('city')  # Get city name from form
        if city:
            # Build API URL with city name and API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)  # Make API request
            if response.status_code == 200:      
                data = response.json()  # Convert response to Python dictionary
                # Extract required weather details
                weather_data = {
                    'city': city.title(),
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                error = "City not found. Please try again."
    # Render HTML template with weather or error info
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
