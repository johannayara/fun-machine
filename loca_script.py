import pandas as pd
import os 
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from tqdm import tqdm
import time

tqdm.pandas()

ANNUAIRE_PATH = "data"
# Ensure directory exists
if not os.path.exists(ANNUAIRE_PATH):
    raise FileNotFoundError(f"Directory {ANNUAIRE_PATH} does not exist.")

# List CSV files in directory
csv_files = [os.path.join(ANNUAIRE_PATH, f) for f in os.listdir(ANNUAIRE_PATH) if f.endswith(".csv")]
csv_files = ["table_1885.csv", "table_1901.csv", "table_1923.csv", "table_1951.csv"]
# Testing with 1885
test_file = os.path.join(ANNUAIRE_PATH, csv_files[0])
df = pd.read_csv(test_file, index_col=0)
df = df.reset_index()

# Geolocator with longer timeout
geolocator = Nominatim(user_agent="fun_machine", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Create dataframe with all the unfound locations 
df_error = pd.DataFrame(columns=['LOC', 'ERROR'])
error_records = []  # Store dicts of errors
positions = []

for location in tqdm(df['LOC'], desc="Geocoding"):
    attempt = 0
    max_retries = 3
    pos = None

    while attempt < max_retries:
        try:
            pos = geocode(location)
            break
        except GeocoderUnavailable:
            attempt += 1
            time.sleep(2)
        except Exception as e:
            error_records.append({'LOC': location, 'ERROR': str(e)})
            break

    if pos is None:
        error_records.append({'LOC': location, 'ERROR': 'No result or retry failed'})

    positions.append(pos)

df['POS'] = positions
df['COOR'] = df['POS'].apply(lambda loc: (loc.latitude, loc.longitude) if loc else None)


filename = "final_"+os.path.basename(test_file)

df.to_csv(filename, index=False)  
