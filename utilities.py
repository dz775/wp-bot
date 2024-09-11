import requests
from googletrans import Translator


translator = Translator()
GOOGLE_MAPS_API = ''

def translate_text(text, lang):
    print(text)
    return translator.translate(text, dest=lang).text

def get_coordinates(pincode):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    address = f'{pincode}, India'
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

def get_nearest_police_station(location, radius=5000, keyword='police station near me'):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'key': GOOGLE_MAPS_API,
        'location': location,
        'radius': radius,
        'keyword': keyword
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = ''
    for station in data['results']:
        results += f"{station['name']} - {station['vicinity']} \n\n "
    return results
