import pandas as pd
import os
import re
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from tqdm import tqdm
import pickle

# Config
ANNUAIRE_PATH = "data"
CACHE_PATH = "cache"
ERRORS_PATH = "errors"
OUTPUT_PATH = "out"

CSV_FILES = ["table_1885_clf.csv", "table_1901_clf.csv", "table_1923_clf.csv", "table_1951_clf.csv"]
TARGET_FILE = CSV_FILES[0]

print("Which file would you like to process ?")
for i, f in enumerate(CSV_FILES):
    print(f"{f} -> {i}")

TARGET_FILE = CSV_FILES[int(input("Enter a number: "))]

CACHE_FILE = os.path.join(CACHE_PATH, "geocode_cache.pkl")
ERRORS_FILE = os.path.join(ERRORS_PATH, "geocode_errors.csv")
OUTPUT_FILE = os.path.join(OUTPUT_PATH, "geocoded_" + os.path.basename(TARGET_FILE))

# Load data
file_path = os.path.join(ANNUAIRE_PATH, TARGET_FILE)
df = pd.read_csv(file_path, index_col=0)[:2000]

# Geocoder setup
geolocator = Nominatim(user_agent="fun_machine", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Load or initialize cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        cache = pickle.load(f)
else:
    cache = {}

# Clean and format address
def clean_address(raw):
    raw = str(raw)
    # print(f"Address was {raw}")
    raw = re.sub(r"[,.'’]+", " ", raw)        # Remove problematic punctuation
    raw = re.sub(r"\s+", " ", raw).strip()    # Normalize whitespace
    return f"{raw}, Lausanne, Switzerland"

# Process
positions = []
errors = []

for i, loc in enumerate(tqdm(df['LOC'], desc="Geocoding")):
    cleaned = clean_address(loc)

    if cleaned in cache:
        result = cache[cleaned]
    else:
        attempt = 0
        result = None
        while attempt < 3:
            try:
                # print(f"Trying to geocode {cleaned}")
                result = geocode(cleaned)
                break
            except GeocoderUnavailable:
                attempt += 1
                time.sleep(2)
            except Exception as e:
                errors.append({'LOC': loc, 'ERROR': str(e)})
                break
        
        cache[cleaned] = result

    if result is None:
        errors.append({'LOC': loc, 'ERROR': 'No result or retry failed'})

    positions.append(result)

    if i % 500 == 0 and i != 0:
        # Save cache every 500 iterations
        print("[+] UPDATING CACHE")
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)


# Save cache at the end
print("[+] UPDATING CACHE")
with open(CACHE_FILE, 'wb') as f:
    pickle.dump(cache, f)

# Save results
df['POS'] = positions
df['COOR'] = df['POS'].apply(lambda loc: (loc.latitude, loc.longitude) if loc else None)
df.to_csv(OUTPUT_NAME, index=False)

# Log errors if any
if errors:
    pd.DataFrame(errors).to_csv(ERRORS_FILE, index=False)
