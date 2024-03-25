import requests
from django.shortcuts import render
from django.conf import settings
from .models import City
from .forms import CityForm


def index(request):
    api_key = settings.WEATHER_KEY
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    all_cities = []
    cities = City.objects.all()
    for city in cities:
        url = (f'https://api.openweathermap.org/data/2.5/weather?q={city.name}'
               f'&units=metric&appid={api_key}')
        response = requests.get(url).json()
        city_info = {
            'city': city.name,
            'temp': response['main']['temp'],
            'icon': response['weather'][0]['icon'],
            'description': response['weather'][0]['description']
            }
        all_cities.append(city_info)
    context = {
        'all_info': all_cities,
        'form': form
    }
    return render(request, 'weather/weather.html', context)