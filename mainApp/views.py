from django.shortcuts import render
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm

def index(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a8fba400b7bbf3e101a2da97298ff827'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            # Clear the form after successful submission
            form = CityForm()
    else:
        # If it's a GET request, create a new form
        form = CityForm()

    weather_data = []

    for city in cities:
        try:
            city_weather = requests.get(url.format(city)).json()

            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
                'humidity': city_weather['main']['humidity'],
                'pressure': city_weather['main']['pressure'],
                'windspeed': city_weather['wind']['speed'],
                'feelslike': city_weather['main']['feels_like']
            }
            weather_data.append(weather)
        except KeyError as e:
            # Add a message to the Django messages framework
            messages.warning(request, f"KeyError: {e}. Skipping city: {city}")

    context = {'weather_data': weather_data, 'form': form}
    
    # If it's a GET request, delete all data from the City model
    if request.method == 'GET':
        City.objects.all().delete()

    return render(request, 'index.html', context)