import pandas as pd
import json
import re

# Function to parse coordinates from the string format
def parse_coordinates(coord_str):
    if pd.isna(coord_str):
        return None

    # Extract coordinates using regex
    match = re.search(r'\(([^,]+),\s*([^)]+)\)', coord_str)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return [lat, lon]
    return None

YEAR = 1951

# Load the file
df = pd.read_csv(f'inputs/geocoded_table_{YEAR}_clf.csv', quotechar='"', skipinitialspace=True)

# Create intensity data format
intensity_data = []

# Normalize salaries for intensity values (between 0 and 1)
if not df['salaire'].empty:
    min_salary = df['salaire'].min()
    max_salary = df['salaire'].max()

    salary_range = max_salary - min_salary


    # Process each row
    for _, row in df.iterrows():
        coords = parse_coordinates(row['COOR'])
        salary = row['salaire']

        # Only include entries with valid coordinates and salary
        if coords is not None:
            # Normalize salary to get intensity (0 to 1)
            intensity = (salary - min_salary) / salary_range
            intensity_data.append([float(intensity), coords])

with open(f'out/intensity_data_{YEAR}.json', 'w') as f:
    f.write(json.dumps(intensity_data, indent=1))

print(f"Converted {len(intensity_data)} data points to intensity_data.json")
