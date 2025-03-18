import requests

endpoint = "https://api.inaturalist.org/v1/observations"

params = {
    'place_id': 34,
    'taxon_id': 47126,
    'quality_grade': 'research',
    'per_page': 20,
    'page': 1
}

response = requests.get(endpoint, params=params)

data = response.json()
observations = data.get('results', [])

for x in observations:
    species = x['taxon']['name']
    img_url = x['photos'][0]['url'].replace('square', 'large')
    print(f"{species}: {img_url}")
