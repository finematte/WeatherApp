from django.shortcuts import render
import requests
import datetime
import environ


def index(request):
    env = environ.Env()

    placeholder = "Enter city"

    if 'temp' in request.POST:
        if str(request.POST['temp']) == 'on':
            units = 'imperial'
            temp_convert = "checked"
            temp_symbol = '&#8457;'
    else:
        units = 'metric'
        temp_convert = ""
        temp_symbol = '&#8451;'

    if 'city' in request.POST:
        if not str(request.POST['city']).replace(' ', '').isalpha():
            city = 'Amsterdam'
            placeholder = 'Please enter valid city!'
        else:
            city = request.POST['city']
    else:
        city = 'Amsterdam'

    appid = env('APPID')
    URL = 'https://api.openweathermap.org/data/2.5/weather'

    try:
        PARAMS = {'q': city, 'appid': appid, 'units': units}
        r = requests.get(url=URL, params=PARAMS)
        r.raise_for_status()
    except requests.HTTPError:
        units = 'metric'
        temp_convert = ""
        temp_symbol = '&#8451;'
        city = 'Amsterdam'
        placeholder = 'Please enter valid city!'
        PARAMS = {'q': city, 'appid': appid, 'units': units}
        r = requests.get(url=URL, params=PARAMS)

    res = r.json()
    description = str(res['weather'][0]['description']).capitalize
    icon = res['weather'][0]['icon']
    temp = res['main']['temp']
    feels_like = res['main']['feels_like']
    temp_min = res['main']['temp_min']
    temp_max = res['main']['temp_max']

    day = datetime.date.today()

    HTML_PARAMS = {'city': city, 'description': description, 'icon': icon, 'temp': temp, 'feels_like': feels_like,
                   'temp_min': temp_min, 'temp_max': temp_max, 'day': day, 'placeholder': placeholder,
                   'temp_convert': temp_convert, "temp_symbol": temp_symbol}

    return render(request, 'weatherapp/index.html', HTML_PARAMS)
