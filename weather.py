#! python3

import sys, requests, bs4
from geopy.geocoders import Nominatim


def get_loc(zip):
    """
    Determines latitude, longitude, and address
    based on zip code
    """
    geolocator = Nominatim(user_agent="weather-terminals")
    location = geolocator.geocode(zip)
    lat = str(location.latitude)
    lon = str(location.longitude)
    address = location.address
    return lat, lon, address


def get_weather(url):
    """
    Creates a weather report based on date from weather.gov
    Report includes day, temperature, and description
    """
    # set report line length
    line_len = 16

    # get weather data
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    names = soup.find_all("p", {"class": "period-name"})
    descs = soup.find_all("p", {"class": "short-desc"})
    temp_highs = soup.find_all("p", {"class": "temp temp-high"})
    temp_lows = soup.find_all("p", {"class": "temp temp-low"})

    report = [''] * 8
    # format name lines
    for n in names:
        text = n.get_text(separator="\n").split('\n')
        if len(text) == 1:
            text = text + ['']
        report[0] = report[0] + text[0].center(line_len)
        report[1] = report[1] + text[1].center(line_len)
    report[2] = ''

    # combine temperatures into single list
    temps = [None] * (len(temp_highs) + len(temp_lows))
    if len(temp_highs) > len(temp_lows):
        temps[0::2] = temp_highs
        temps[1::2] = temp_lows
    else:
        temps[0::2] = temp_lows
        temps[1::2] = temp_highs

    # format temperature lines
    for t in temps:
        text = t.get_text(separator="\n").split('\n')
        report[3] = report[3] + text[0].center(line_len)
    report[4] = ''

    # format description lines
    for d in descs:
        text = d.get_text(separator="\n").split('\n')
        if len(text) == 1:
            text.append('')
        if len(text) == 2:
            text.append('')
        report[5] = report[5] + text[0].center(line_len)
        report[6] = report[6] + text[1].center(line_len)
        report[7] = report[7] + text[2].center(line_len)

    # combine into single report
    report_str = '\n'.join(report)
    return report_str
    

def main():
    # get location
    zip_code = sys.argv[1]
    loc = get_loc(zip_code)

    # get weather report
    url = 'https://forecast.weather.gov/MapClick.php?lat='+loc[0]+'&lon='+loc[1]
    weather_report = get_weather(url)

    # output weather report
    print(loc[2] + '\n')
    print(weather_report)


if __name__ == '__main__':
    main()
