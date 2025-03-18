import requests

endpoint = "https://api.inaturalist.org/v1/observations"
endpoint_species = "https://api.inaturalist.org/v1/observations/species_counts"

params = {
    'place_id': 34,
    'taxon_id': 47126,
    'quality_grade': 'research',
    'per_page': 0,
}

response = requests.get(endpoint, params=params)

data = response.json()
total_count = data.get('total_results', 0)
print(f"{total_count} high quality observations for Colorado")

response = requests.get(endpoint_species, params=params)

data = response.json()
total_count = data.get('total_results', 0)
print(f"{total_count} species observed in Colorado")
