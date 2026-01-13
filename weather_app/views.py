from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import JsonResponse
from .models import City
from django.contrib import messages 
# Create your views here.
def home(request):

    # city = 'hanoi'

    # define api key and the base url for openweathermap
    API_KEY = '0ef7e65ba3f223c9f73e91e693f9b0ca'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    #check if the request is a POST (when adding the new CITY)

    if request.method == 'POST':
        city_name = request.POST.get('city') #get city name from the form

        #Feth weather data for the city from the data 
        response = requests.get(url.format(city_name, API_KEY)).json()

        #check if the city exists in the API
        if response['cod'] == 200:
            if not City.objects.filter(name=city_name).exists():
                #save the new city to the database
                City.objects.create(name=city_name)
                messages.success(request, f'{city_name} have been add successfully!')

            else:
                messages.info(request, f'{city_name} already exist!')    

        else:
            messages.error(request, f'City {city_name} not found!')
                     
        return redirect('home')

    weather_data=[]
    # Feth weather data for all save cities
    try:
        citeis = City.objects.all() #Get all citeis from database
        for city in citeis:
            response = requests.get(url.format(city.name, API_KEY))
            data = response.json()

            if data['cod'] == 200:
                city_weather = {
                    'city': city.name,
                    'temperature': data['main']['temp'],
                    'descrition': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                weather_data.append(city_weather)
            else:
                City.objects.filter(name=city.name).delete()

    except requests.RequestException as e:
        print('Error conecting to weather server. pls try again letter')    
    
    context = {'weather_data' : weather_data}

    return render(request, 'index.html', context)