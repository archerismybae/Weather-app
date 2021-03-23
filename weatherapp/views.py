import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0af7ce75bda96328fb9cd8d2e8061b3f'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    return HttpResponse('City does not exist in the world') 
            else:
                return HttpResponse('City already exists in the database!') 
        else:
            return HttpResponse('Form not valid')
    else:
        form = CityForm()

    cities = City.objects.all()
    if cities.count() == 0:
        context = {'form': form}
    else:
        weather_data = []

        for city in cities:

            del_obj = City.objects.get(id=city.id)
            
            r = requests.get(url.format(city)).json()

            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'del_obj': del_obj,
            }
            weather_data.append(city_weather)
        context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weatherapp/home.html', context)

def delete_city(request, item):
    del_city = City.objects.get(id=item)
    print(del_city)
    del_city.delete()
    return HttpResponseRedirect('/')