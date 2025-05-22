import pandas as pd
import json
import re

job_to_sector = {
    "Produits alimentaires": "Secteur secondaire",
    "Vêtem., lingerie, chauss., literie": "Secteur secondaire",
    "Industrie textile": "Secteur secondaire",
    "Industrie du papier": "Secteur secondaire",
    "Arts graphiques": "Secteur secondaire",
    "Industrie chimique": "Secteur secondaire",
    "Bois, liège, meubles": "Secteur secondaire",
    "Pierre et terre": "Secteur secondaire",
    "Industrie d. métaux(2)": "Secteur secondaire",
    "Horlogerie": "Secteur secondaire",
    "Bijouterie, gravure, frappe": "Secteur secondaire",
    "Construct., charpenterie": "Secteur secondaire",
    "Gaz, eau, éléctricité": "Secteur secondaire",
    "Commerce de gros": "Secteur tertiaire",
    "Commerce de détail": "Secteur tertiaire",
    "Banques, établissments financ. ": "Secteur tertiaire",
    "Assurances privées": "Secteur tertiaire",
    "Agences, location, consultation": "Secteur tertiaire",
    "Affaires immobilières, location ": "Secteur tertiaire",
    "Bureaux de consultation": "Secteur tertiaire",
    "Hôtellerie, restaurants": "Secteur tertiaire",
    "Transports": "Secteur tertiaire",
    "Administration publique": "Secteur tertiaire",
    "Réparations": "Secteur tertiaire",
    "Vachers célibataires": "Secteur primaire",
    "Employés pour tous travaux, célibataire": "Secteur primaire",
    "Employées pour le ménage et la ferme": "Secteur primaire",
    "Journaliers; dans la salaire y compris l'entretien": "Secteur primaire",
    "Journalières dans la salaire y compris l'entretien": "Secteur primaire"
}

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

        # add the job and the sector
        job = row['job']
        cat = row['job_clf']
        
        # Lookup the sector, or return None if the job isn't found
        sector = job_to_sector.get(cat)

        # Only include entries with valid coordinates and salary
        if coords is not None:
            # Normalize salary to get intensity (0 to 1)
            intensity = (salary - min_salary) / salary_range
            intensity_data.append([float(intensity), coords, job, cat, sector])

with open(f'out/intensity_data_with_sector_{YEAR}.json', 'w') as f:
    f.write(json.dumps(intensity_data, indent=1))

print(f"Converted {len(intensity_data)} data points to intensity_data_sector.json")
