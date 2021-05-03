# API to get weather data

import requests

def get_weather(getVar):
    api_key = ''
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(getVar, api_key)
    r = requests.get(url)
    global data_w
    data_w = r.json()
    # with open('test_file.json', 'w') as myfile: # json Datei schreiben
    # json.dump(r.json(), myfile)

get_weather()
print(data_w)
