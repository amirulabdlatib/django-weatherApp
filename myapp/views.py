from django.shortcuts import render
import json
import urllib.request
from urllib.error import HTTPError  # Import HTTPError for error handling

# Create your views here.
def index(request):
    data = {}  # Initialize the data dictionary

    if request.method == 'POST':
        city = request.POST.get('city-name')
        if city:
            
            # Clean the city name by removing leading and trailing spaces
            city = city.strip()
            # Replace internal spaces with "%20" for URL encoding
            city_encoded = city.replace(' ', '%20')
            try:
                source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' + city_encoded + '&appid=647e15e32015c439dd1d88c89f2a9130').read()
                list_of_data = json.loads(source)
                data = {
                    "city": city,
                    "country_code": str(list_of_data['sys']['country']),
                    "temperature": str(list_of_data['main']['temp']),
                    'description': str(list_of_data['weather'][0]['description'])
                }
            except HTTPError as e:
                # Handle API request error here (e.g., invalid city name)
                data['error'] = f"Error: {e}"
        else:
            data['error'] = "Please enter a city name."

    return render(request, 'myapp/index.html', context=data)