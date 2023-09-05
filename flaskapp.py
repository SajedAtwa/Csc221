
# A very simple Flask Hello World app for you to get started with...
import requests
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def header():
    return '<h2>CSC 221 - Final Challenge<h2> \n <p>24022289<br />Sajed Atwa</p>'

@app.route('/id')
def info():
    return '24022289_Atwa'

@app.route('/hot_and_new/<ZIPCODE>')
def hot_new(ZIPCODE):
    url = f'https://api.yelp.com/v3/businesses/search?location={ZIPCODE}&radius=5000&attributes=hot_and_new&sort_by=best_match&limit=10'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer dmlJJURxaMxoBZm-9-2degXs1mPzVnYDUTTiaSIo1oIPnXDpHc6sQfM3KdsWGDNrkPCDNxixVpTjwyy4TBcLD22B817wdXu9Z2vPU-IvWecueh5_v70mVvCpPFpJZHYx"
    }
    response = requests.get(url, headers=headers)
    yelp= response.json()['businesses']
    result = []
    for A in yelp:
        info = {
            'name': A['name'],
            'url': A['url'],
            'categories': [D['title'] for D in A['categories']],
            'location': A['location']['display_address'],
            'phone': A['display_phone'],
            'distance': f"{A['distance'] * 0.000621371:.1f} mi"
            }
        result.append(info)
    return jsonify(result)


@app.route('/hot_and_new_html/<ZIPCODE>')
def hot_new_html(ZIPCODE):
    url = f'https://api.yelp.com/v3/businesses/search?location={ZIPCODE}&radius=5000&attributes=hot_and_new&sort_by=best_match&limit=10'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer dmlJJURxaMxoBZm-9-2degXs1mPzVnYDUTTiaSIo1oIPnXDpHc6sQfM3KdsWGDNrkPCDNxixVpTjwyy4TBcLD22B817wdXu9Z2vPU-IvWecueh5_v70mVvCpPFpJZHYx"
    }
    response = requests.get(url, headers=headers)
    data = response.json()['businesses']
    # Format the result into HTML
    html = f'<h2>New and Hot businesses near {ZIPCODE}</h2>'
    for yelp in data:
        name = yelp['name']
        url = yelp['url']
        categories = '/'.join([category['title'] for category in yelp['categories']])
        location = '<br />'.join(yelp['location']['display_address'])
        phone = yelp['display_phone']
        distance = f"{yelp['distance'] / 1609.34:.1f}"
        html += f'<h3><a href="{url}" target="_blank">{name}</a> ({distance} miles away)</h3>'
        html += f'{categories}<br /><b>{location}</b><br />{phone}<br /><br />'
    return html
