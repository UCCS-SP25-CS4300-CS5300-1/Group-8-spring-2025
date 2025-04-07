##
## This script uses iNaturalist API to create folders for each species & download images per species
## Ensure that you set DOWNLOAD_DIR within a parent folder for the species folders
##

import requests
import os
import time

PLACE_ID = 34              # Colorado's place_id
TAXON_ID = 47126           # Plants
QUALITY_GRADE = 'research' # Only research-grade observations
MIN_OBSERVATIONS = 250     # Minimum number of observations per species
SPECIES_PER_PAGE = 200     # For species_counts endpoint
OBS_PER_PAGE = 200         # For observations endpoint
MAX_OBSERVATION_PAGES = 3  # Limit to a few pages per species (adjust as needed)
DOWNLOAD_DIR = "C:\LeafQuest_Dataset"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

species_counts = []
species_counts_endpoint = "https://api.inaturalist.org/v1/observations/species_counts"
page = 1

while True:
    params = {
        'place_id': PLACE_ID,
        'taxon_id': TAXON_ID,
        'quality_grade': QUALITY_GRADE,
        'per_page': SPECIES_PER_PAGE,
        'page': page
    }
    response = requests.get(species_counts_endpoint, params=params)
    if not response.ok:
        break

    data = response.json()
    results = data.get('results', [])
    if not results:
        break

    for sp in results:
        species_name = sp['taxon']['name']
        taxon_id = sp['taxon']['id']
        count = sp['count']
        if count >= MIN_OBSERVATIONS:
            species_counts.append((species_name, taxon_id, count))
    page += 1
    time.sleep(1)

observations_endpoint = "https://api.inaturalist.org/v1/observations"

for species_name, taxon_id, count in species_counts:
    
    safe_species_name = species_name.replace(" ", "_").replace("/", "_")
    species_dir = os.path.join(DOWNLOAD_DIR, safe_species_name)
    os.makedirs(species_dir, exist_ok=True)    
    print(f"\nProcessing species: {species_name} (Taxon ID: {taxon_id})")
    # % of species processed so far
    percent_processed = (species_counts.index((species_name, taxon_id, count)) + 1) / len(species_counts) * 100
    print(f"{percent_processed:.2f}%")

    for page in range(1, MAX_OBSERVATION_PAGES + 1):
        params = {
            'place_id': PLACE_ID,
            'taxon_id': taxon_id,
            'quality_grade': QUALITY_GRADE,
            'per_page': OBS_PER_PAGE,
            'page': page
        }
        response = requests.get(observations_endpoint, params=params)
        if not response.ok:
            print(f"Error fetching observations for {species_name}")
            break
        
        data = response.json()
        observations = data.get('results', [])
        if not observations:
            break
        
        for obs in observations:
            
            if 'photos' not in obs or len(obs['photos']) == 0:
                continue
            photo = obs['photos'][0]
            photo_url = photo.get('url')
            if not photo_url:
                continue
            
            photo_url = photo_url.replace('square', 'small')
            photo_id = photo.get('id')
            img_path = os.path.join(species_dir, f"{photo_id}.jpg")
            
            if os.path.exists(img_path):
                continue

            try:
                img_response = requests.get(photo_url)
                if img_response.ok:
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)
                else:
                    print(f"Failed to download image {photo_id} for {species_name}")
            except Exception as e:
                print(f"Error downloading image {photo_id} for {species_name}: {e}")
        
        # To not overload API
        time.sleep(1)
