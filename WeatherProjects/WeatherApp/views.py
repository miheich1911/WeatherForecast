from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views import View
from .forms import CityForm
from .models import City, User


def index(request):
    cities = City.objects.all().order_by('-id')

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        form = CityForm()
        city = City.objects.all().last()
        coord_url = 'https://geocoding-api.open-meteo.com/v1/search?name={}&count=10&language=ru&format=json'
        r = requests.get(coord_url.format(city)).json()

        city_coord = {
                        'name': city.name,
                        'latitude': r['results'][0]['latitude'],
                        'longitude': r['results'][0]['longitude']
                    }

        weather_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m"

        res = requests.get(weather_url.format(city_coord['latitude'], city_coord['longitude'])).json()

        city_info = {
                        'city': city_coord['name'],
                        'temp': f'{res['current']['temperature_2m']}°C'
                }

        context = {'info': city_info, 'form': form, 'cearch_city': cities[:10]}

    else:
        form = CityForm()
        context = {'form': form, 'cearch_city': cities[:10]}
    return render(request, 'weather/index.html', context)


class CityAutocomplete(View):
    def get(self, request):
        query = request.GET.get('term', '')
        all_cities = []
        cities = City.objects.filter(name__icontains=query)
        for city in cities:
            if city not in all_cities:
                all_cities.append(city)
        results = list(set(city.name for city in all_cities))
        return JsonResponse(results, safe=False)



