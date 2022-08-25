#! /usr/bin/python3

import requests, sys
from geopy.geocoders import Nominatim


def get_loc(zip):
    geolocator = Nominatim(user_agent="weather-terminals")
    location = geolocator.geocode(zip)
    lat = location.raw['lat']
    lon = location.raw['lon']
    return (lat,lon)
    

def main():
    zip_code = '92691'
    #zip_code = sys.argv[1]
    loc = get_loc(zip_code)
    
    url = 'https://forecast.weather.gov/MapClick.php?lat='+loc[0]+'&lon='+loc[1]
    print(url)
    

if __name__ == '__main__':
    main()
